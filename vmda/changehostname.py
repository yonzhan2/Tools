import os
# import MySQLdb
import pymongo
import re, uuid
import time
import subprocess
from subprocess import Popen, PIPE

HOST = "172.24.66.158"
USER = "root"
PASS = "pass"
DBNAME = "vmdb"
PORT = "3306"


class GetData(object):
    def __init__(self):
        pass

    def getvmname(self, vmmacc):
        try:
            db = MySQLdb.connect(HOST, USER, PASS, DBNAME, charset='utf8')
            cursor = db.cursor()
            sql = "SELECT vmname FROM vminfo where vmmacc = '%s'" % (vmmacc)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            return result
            db.close()

        except MySQLdb.Error as e:
            print
            "Error %d: %s" % (e.args[0], e.args[1])


class GetDataFromMongo(object):
    def __init__(self):
        pass

    def getvminfo(self, vmmacc):
        try:
            client = pymongo.MongoClient("mongodb://{0}:27017/".format(HOST), connectTimeoutMS=60000)
            mydb = client["test"]
            mycoll = mydb["vminfo"]
            mydict = {"vmmacc": vmmacc}
            vmname = mycoll.find_one(mydict)["vmname"]
            return vmname

        except Exception as e:
            print
            "Error is %s" % e


def isIPAlive():
    p = subprocess.Popen("nslookup qa.webex.com", stdin=PIPE, stdout=PIPE, shell=True)
    ret = p.stdout.readline()
    try:
        ret = re.match('Server', ret).group()
        return True
    except:
        return False


"""
def getIP(vmname):
    with open('failure','r') as f:
        pattern = re.compile(r"{0} (.*)".format(vmname))
        res = re.findall(pattern,f.read())
        return res[0]

gd = GetData()
"""

gdfm = GetDataFromMongo()

timeout = 0
while timeout <= 30:
    if isIPAlive():
        print
        "IP is Alive"
        break
    else:
        time.sleep(3)
        timeout += 3

# cmd='netdom renamecomputer %COMPUTERNAME% /Newname "{}" /Force /REBoot:1'.format(newname)

if not os.path.exists(r"/vmconfig/.changedhostname"):
    time.sleep(3)
    vmmacc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print
    "vmmacc is ", vmmacc
    vmname = gdfm.getvminfo(vmmacc)
    print
    "vmname is", vmname
    hostname, ipaddr = vmname.split('-', 1)
    ipaddr = ipaddr.strip('-ct74')
    cmd = "sh /vmconfig/vmconfig.sh {0} {1}".format(hostname, ipaddr)

    if hostname:
        print
        cmd
        os.system(cmd)
        with open(r"/vmconfig/.changedhostname", 'w+') as f:
            f.write("Changed hostname {0} macc {1} done!".format(hostname, vmmacc))
        time.sleep(3)
        os.system("reboot")
