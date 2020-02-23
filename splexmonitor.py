import cx_Oracle
import time
from threading import Thread
from pprint import pprint
import logging
import pymongo
from pathlib import Path
import argparse
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import json
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig()
start = time.time()
timestamp_str = str(int(start))
logger.debug(timestamp_str)
BASE_DIR = Path(__file__).parent
logger.debug(BASE_DIR)
from_addr = 'splexmonitor@cisco.com'


def setEnvironment():
    if sys.platform == 'linux':
        os.environ["ORACLE_HOME"] = '/home/oracle/OraHome1'
        os.environ["LD_LIBRARY_PATH"] = '$LD_LIBRARY_PATH:$ORACLE_HOME/lib'


setEnvironment()


def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to mongodb')

    parser.add_argument('-e', '--env',
                        required=True,
                        action='store',
                        help='env name, eg. SZHF')

    parser.add_argument('-f', '--config_file',
                        required=True,
                        action='store',
                        help='config file of splex monitor')

    parser.add_argument('-t', '--email_to',
                        required=False,
                        action='store',
                        help='email list for alter email')

    args = parser.parse_args()
    return args


def now():
    start_format = time.strftime('%Y-%m-%d %H:%M:%S GMT', time.localtime(time.time()))
    return start_format


def sendmail(check_env, alert_msg, from_addr, to_addr):
    msg = MIMEText(alert_msg, 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr)
    msg['Subject'] = Header(u'SharePlex Monitor Alter on %s' % check_env, 'utf-8').encode()
    # server = smtplib.SMTP('localhost')
    server = smtplib.SMTP('mda.webex.com')
    server.set_debuglevel(0)
    server.sendmail(from_addr, to_addr, msg.as_string())


class ManipulateDataToMongo:
    def __init__(self, MONGODB="173.36.203.62"):
        self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(MONGODB))
        self.mydb = self.client["splexmonitor"]
        self.mycoll = self.mydb["splex"]

    def query_failure_data(self, check_env):

        try:
            myquery = {"env": check_env, "SP_Status": "Failed"}
            ret = self.mycoll.count_documents(myquery)
            if ret:
                return ret
            return 0
        except Exception as e:
            logger.error(("Query data error at %d: %s" % (e.args[0], e.args[1])))

    def save_data(self, check_env, name, port_number, source_db, target_db, sp_status, server_info):

        try:
            myquery = {"env": check_env, "PortNumber": port_number, "Source_DB": source_db, "Target_DB": target_db}
            mydict = {"env": check_env, "Name": name, "PortNumber": port_number, "Source_DB": source_db,
                      "Target_DB": target_db, "SP_Status": sp_status, "Checking_Time": now(),
                      "Server_Info": server_info}
            if port_number and source_db and target_db:
                # replace_one is for insert/update
                self.mycoll.replace_one(myquery, mydict, upsert=True)
                logger.info(("Saved shareplex monitor data done for %s %s %s" % (port_number, source_db, target_db)))
        except Exception as e:
            raise e
            logger.error(("Saved shareplex monitor data failed at  %d: %s" % (e.args[0], e.args[1])))


class SplexMonitor(Thread):
    def __init__(self, check_env, replication_name, splex_port, source_db, target_db, server_info,
                 password="pass"):
        Thread.__init__(self)
        self.check_env = check_env
        self.replication_name = replication_name
        self.splex_port = splex_port
        self.username = "splex" + str(splex_port)
        self.source_db = source_db
        self.target_db = target_db
        self.sp_status = "Pass"
        self.checking_time = now()
        self.server_info = server_info
        self.password = password
        self.keyword = '_'.join(["PyMonitor", self.source_db, self.target_db])[:30]
        self.timestamp_string = timestamp_str
        self.monogdb = ManipulateDataToMongo()

    def insert_data(self):
        try:
            with cx_Oracle.connect(self.username, self.password, self.source_db, encoding="UTF-8") as connection:
                cursor = connection.cursor()
                cursor.execute("insert into DEMO_SRC values (:1, :2, :3)",
                               (self.keyword, self.source_db, self.timestamp_string))
                connection.commit()
        except Exception as e:
            print(f"Insert data failed on source db {self.source_db} due to {e}")
            self.monogdb.save_data(self.check_env, self.replication_name, self.splex_port, self.source_db,
                                   self.target_db, "Failed", self.server_info)

    def delete_data(self):
        try:
            with cx_Oracle.connect(self.username, self.password, self.source_db, encoding="UTF-8") as connection:
                cursor = connection.cursor()
                cursor.execute("delete from DEMO_SRC where name = :1 and phone# = :2",
                               (self.keyword, self.timestamp_string))
                connection.commit()
        except Exception as e:
            print(f"Delete data failed on target db {self.target_db} due to {e}")

    def query_data(self):
        time.sleep(30)
        try:
            with cx_Oracle.connect(self.username, self.password, self.target_db, encoding="UTF-8") as connection:
                cursor = connection.cursor()
                cursor.execute("select count(1) from DEMO_SRC where name = :1 and phone# = :2",
                               (self.keyword, self.timestamp_string))
                ret = cursor.fetchone()[0]
                if ret == 1:
                    self.delete_data()
                    self.monogdb.save_data(self.check_env, self.replication_name, self.splex_port, self.source_db,
                                           self.target_db, "Pass", self.server_info)
                    logger.debug(f"Splex Replication from {self.source_db} to {self.target_db} is Good at {now()}.")
                else:
                    self.monogdb.save_data(self.check_env, self.replication_name, self.splex_port, self.source_db,
                                           self.target_db, "Failed", self.server_info)
                    logger.debug(f"Splex Replication {self.source_db} to {self.target_db} is Bad at {now()}.")
        except Exception as e:
            logger.error(f"Query data failed on target db {self.target_db} due to {e}")

    def run(self):
        self.insert_data()
        self.query_data()


def get_alert_times(check_env):
    try:
        with open(BASE_DIR / f'email_alert_control_{check_env}.json') as fh:
            json_data = json.load(fh)
            return json_data.get(check_env, 'NA').get('alert_count', 0), json_data.get(check_env, 'NA').get(
                'last_modified_time', start)
    except Exception as e:
        return 0, start


def set_alert_times(check_env, alert_count, last_modified_time):
    with open(BASE_DIR / f'email_alert_control_{check_env}.json', 'w') as fh:
        json_data = {check_env: {"alert_count": alert_count, "last_modified_time": last_modified_time}}
        json.dump(json_data, fh)


args = get_args()
env = args.env
config_file = args.config_file

with open(BASE_DIR / config_file) as fh:
    lines = fh.readlines()
    # pprint(lines)
    data = [line.split() for line in lines if not line.startswith("#") and line.strip()]
    logger.debug(data)

threads = []
for entity in data:
    thread = SplexMonitor(env, *entity)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

mongodb = ManipulateDataToMongo()
failure_count = mongodb.query_failure_data(env)
logger.debug("failure count is %s" % failure_count)

alert_msg = """
Hi Team,

     There are %s replication channel(s) failed, please take a look ASAP!

     please see the link below to check detail info.

     http://splex.qa.webex.com/splex/?env=%s

Best Regards
-LabAdmin
""" % (failure_count, env)

duration = time.time() - get_alert_times(env)[1]
print(duration)

if failure_count >= 1:
    if get_alert_times(env)[0] < 2 and duration < 3600:
        set_alert_times(env, get_alert_times(env)[0] + 1, start)
        sendmail(env, alert_msg, from_addr, to_addr=["yonzhan2@cisco.com"])
    else:
        set_alert_times(env, get_alert_times(env)[0] + 1, get_alert_times(env)[1])
else:
    set_alert_times(env, 0, last_modified_time=start)

end = time.time()
logger.info("Time of multi-threading: %f " % (end - start))
logger.info("Exiting Main Thread.")
