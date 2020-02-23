#!/usr/local/bin/python

from __future__ import print_function
import paramiko
import requests
import threading
import re
import pymongo

cmcurl = "sjcmc.dmz.webex.com"
headers = {'Authorization': 'Basic Q01DQVBJX0RNWjo5M2IyOGNiNzQ4NjM0YmJmYTI4YWZkNWVhODQ2NGY3Mg=='}

##current_dir = os.path.dirname(__file__)

pool_lists = []
ip_lists = []
gLock = threading.Lock()


class SaveRecord:
    def __init__(self, MONGODB="173.37.49.29"):
        self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(MONGODB))
        self.mydb = self.client["changepasswd"]
        self.mycoll = self.mydb["wbxroot"]

    def save_data(self, server, issuccess, why=None):

        try:
            myquery = {"server": server}
            mydict = {"server": server, "issuccess": issuccess, "why": why}

            self.mycoll.replace_one(myquery, mydict, upsert=True)
        except Exception as e:
            raise e


sr = SaveRecord()


def get_pool_lists():
    # url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    session = requests.Session()
    session.headers = headers
    req = session.get(url)

    ret = req.json()[0].get('children')
    global pool_lists
    pool_lists = [cld['name'] for child in ret for cld in child['children']]
    ### filter TA pool_lists
    pool_lists = [pool for pool in pool_lists if not re.search("ta|pj|pf|px|py|bala|fd", pool)]
    print("pools", pool_lists)
    return pool_lists


get_pool_lists()


def get_ip():
    while True:
        gLock.acquire()
        if len(pool_lists) == 0:
            gLock.release()
            break
        else:
            pool = pool_lists.pop()
            gLock.release()
            url = 'https://%s/cmc/api/sitBoxList/logstashagent/?pool=%s&ignore_owner=yes' % (cmcurl, pool)
            req = requests.get(url, headers=headers)
            res = req.json()
            # print(res)
            rows = res.get("rows")
            # print(rows)
            ip_lists.extend([rec.get('ip') for rec in rows])


def sync_time_with_gateway():
    '''Sync time with Gateway'''
    while True:
        gLock.acquire()
        if len(ip_lists) == 0:
            gLock.release()
            break
        else:
            print(ip_lists)
            server = ip_lists.pop()
            gLock.release()
            print("Update Server %s" % server)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            batch_job_cmd = """
sudo useradd shuqli >/dev/null 2>&1
sudo umount /mnt   >/dev/null 2>&1
sudo useradd -g wbxbuilds -G wbxbuilds wbxroot >/dev/null 2>&1
sudo echo -e "echo '<slim svc="'"data"'"  jrepath="'"/opt/slim/daemon/jre"'" logsize="'"1048576"'" loglevel="'"5"'" logdir="'"/tmp/slimlog/"'" sid="'"1"'" >' > /opt/slim/daemon/slimdm.ini" > changepwd.sh
sudo echo "echo '                               <logserverip>192.168.165.101</logserverip> '  >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
sudo echo "echo '                               <logserverip>192.168.165.102</logserverip> '   >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
sudo echo "echo '               <allowedip>173.36.202.1-173.36.202.255,173.36.203.1-173.36.203.255,192.168.165.1-192.168.165.255</allowedip>'  >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
sudo echo "echo '</slim>' >>  /opt/slim/daemon/slimdm.ini" >> changepwd.sh
sudo echo 'echo "wbx@Aa\$hfe02"|passwd --stdin wbxroot' >> changepwd.sh
sudo echo 'echo "wbx@Aa\$hfcm"|passwd --stdin shuqli' >> changepwd.sh
sudo echo 'echo "Hard2GuessMe"|passwd --stdin wbxbuilds' >> changepwd.sh
sudo echo 'echo "Hard2GuessMe"|passwd --stdin root' >> changepwd.sh
sudo echo 'rm -f /opt/slim/daemon/auto_register.xml' >> changepwd.sh
sudo echo 'rm -f /opt/slim/daemon/slimdm.log*' >> changepwd.sh
sudo echo "sed -i '/wbxbuilds/d' /etc/sudoers " >> changepwd.sh
sudo echo "sed -i '/wbxroot/d' /etc/sudoers " >> changepwd.sh
sudo echo "sed -i '/shuqli/d' /etc/sudoers " >> changepwd.sh
sudo echo 'echo \"wbxbuilds            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
sudo echo 'echo \"wbxroot            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
sudo echo 'echo \"shuqli            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
sudo echo 'echo "before kill: slimdm process is `ps -ef|grep slimdm|grep daemon|cut -c 9-15`"' >> changepwd.sh
sudo echo "ps -ef|grep slimdm|grep daemon|cut -c 9-15|xargs kill -9 ">> changepwd.sh
sudo echo "/opt/slim/daemon/slimdm start" >> changepwd.sh
sudo echo "/opt/slim/daemon/slimdm start" >> changepwd.sh
sudo echo 'echo "after kill: slimdm process is `ps -ef|grep slimdm|grep daemon|cut -c 9-15`"' >> changepwd.sh
sudo echo "echo current dir is \`pwd\`"  >> changepwd.sh
sudo chmod 755 changepwd.sh
sudo sed -i 's/relayhost = cnlabmda.qa.webex.com/relayhost = sjdmzmda.dmz.webex.com/g' /etc/postfix/main.cf
sudo sed -i 's/relayhost = mda.webex.com/relayhost = sjdmzmda.dmz.webex.com/g' /etc/postfix/main.cf
sudo service postfix restart  >/dev/null 2>&1
sudo sed -i 's/maxskew=100$/maxskew=100000000/g' /usr/local/bin/ntpchk.sh >/dev/null 2>&1
sudo sed -i '/IP/d' /var/webex/version/build_info.txt
sudo service ntpd stop  >/dev/null 2>&1
sudo ntpdate `sudo route -n | grep ^0.0.0.0 | awk '{print $2}'` > /dev/null 2>&1
sudo service ntpd start  >/dev/null 2>&1
sudo sh changepwd.sh
sudo find /home -name changepwd.sh -exec rm -f {} \;
if [ $? -eq 0 ];then
    echo "Batch job is successful on `hostname -i`"
else
    echo "Batch job is failure on `hostname -i`"
fi
"""

            count = 1
            issuccess = False
            for user, pwd in zip(['wbxroot', 'wbxbuilds', 'wbxbuilds', 'shuqli'],
                                 ['wbx@Aa$hfe02', 'P0w3rSupply!', 'Ch4ll3ng3M3!', 'wbx@Aa$hfcm']):
                print("try the %s times with user %s password %s" % (count, user, pwd))
                try:
                    ssh.connect(server, username=user, password=pwd, timeout=5)
                    stdin, stdout, stderr = ssh.exec_command(batch_job_cmd)
                    ret = stdout.read().decode('utf-8')
                    err = stderr.read()
                    print("result is %s" % ret)
                    if err:
                        print("error is %s" % err)
                    if re.search("successful", ret):
                        issuccess = True
                        sr.save_data(server, issuccess)
                        stdin, stdout, stderr = ssh.exec_command('sudo rm -f changepwd.sh && echo "success"')
                        output = stdout.read()
                        print("output is %s " % output)
                        break
                except Exception as e:
                    print("error is %s with user %s password %s pws on server %s." % (e, user, pwd, server))
                    count += 1

            print("issuccess-> ", issuccess)

            if not issuccess:
                sr.save_data(server, issuccess, why=err)


if __name__ == '__main__':

    ###Producer
    for i in range(4):
        th = threading.Thread(target=get_ip)
        # th.setDaemon(True)
        th.start()
        th.join()

    ###Consumer
    for i in range(5):
        th = threading.Thread(target=sync_time_with_gateway)
        # th.setDaemon(True)
        th.start()
        th.join()
