import os
# import MySQLdb
import pymongo
import re, uuid
import time
import subprocess
from subprocess import Popen, PIPE

HOST = "192.168.254.100"

'''
USER = "test"
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
            print "Error %d: %s" % (e.args[0], e.args[1])

'''


class GetDataFromMongo(object):
    def __init__(self):
        pass

    def getvminfo(self, vmmacc):
        try:
            client = pymongo.MongoClient("mongodb://{}:27017/".format(HOST))
            mydb = client["test"]
            mycoll = mydb["vminfo"]
            mydict = {"vmmacc": vmmacc}
            vmname = mycoll.find_one(mydict)["vmname"]
            return vmname

        except Exception as e:
            print("Error is %s" % e)



def isIPAlive():
    p = subprocess.Popen("nslookup qa.webex.com", stdin=PIPE, stdout=PIPE, shell=True)
    ret = p.stdout.readline()
    try:
        ret = re.match('Server', ret).group()
        return True
    except:
        return False


gdfm = GetDataFromMongo()

timeout = 0
while timeout <= 30:
    if isIPAlive():
        print("IP is Alive")
        break
    else:
        time.sleep(3)
        timeout += 3

# cmd='netdom renamecomputer %COMPUTERNAME% /Newname "{}" /Force /REBoot:1'.format(newname)

if not os.path.exists(r"C:\tools\agent\.changedhostname.flag"):
    time.sleep(60)
    vmmacc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    newname = gdfm.getvminfo(vmmacc)
    cmd = '''wmic computersystem where caption='Win7-Image' rename "{}" '''.format(newname)
    print(cmd)
    if newname:
        os.system(cmd)
        with open(r"C:\tools\agent\.changedhostname.flag", 'w+') as f:
            f.write("Changed hostname {0} macc {1} done!".format(newname, vmmacc))
        os.system("shutdown -r -t 0")
