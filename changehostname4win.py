import os
import MySQLdb
import re, uuid
import time
import subprocess
from subprocess import Popen, PIPE

HOST = "192.168.254.100"
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


def isIPAlive():
    p = subprocess.Popen("nslookup client9.webex.com", stdin=PIPE, stdout=PIPE, shell=True)
    ret = p.stdout.readline()
    try:
        ret = re.match('Server', ret).group()
        return True
    except:
        return False


gd = GetData()
timeout = 0
while timeout <= 90:
    if isIPAlive():
        print "IP is Alive"
        break
    else:
        time.sleep(3)
        timeout += 3

# cmd='netdom renamecomputer %COMPUTERNAME% /Newname "{}" /Force /REBoot:1'.format(newname)

if not os.path.exists(r"C:\changedhostname.flag"):
    time.sleep(60)
    vmmacc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    newname = gd.getvmname(vmmacc)
    cmd = '''wmic computersystem where caption='win7-spc900' rename "{}" '''.format(newname)
    print(cmd)
    if newname:
        os.system(cmd)
        with open(r"C:\changedhostname.flag", 'w+') as f:
            f.write("Changed hostname {0} macc {1} done!".format(newname, vmmacc))
        os.system("shutdown -r -t 0")
