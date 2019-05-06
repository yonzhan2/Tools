
import os
import pymongo
import re, uuid
import time
import subprocess
from subprocess import Popen, PIPE

HOST = "173.36.203.62"

class GetDataFromMongo(object):
    def __init__(self):
        pass

    def getvminfo(self, vmmacc):
        try:
            client = pymongo.MongoClient("mongodb://{0}:2701/".format(HOST), connectTimeoutMS=60000)
            mydb = client["test"]
            mycoll = mydb["vminfo"]
            mydict = {"vmmacc": vmmacc}
            vmname = mycoll.find_one(mydict)["vmname"]
            return vmname
        except Exception as e:
            print("Error is %s" % e)

    def getipinfo(self, ipaddr):
        try:
            client = pymongo.MongoClient("mongodb://{0}:2701/".format(HOST), connectTimeoutMS=60000)
            mydb = client["ipmgr"]
            mycoll = mydb["ippool"]
            mydict = {"ipaddr": ipaddr}
            ret = mycoll.find_one(mydict)
            return ret.get('netmask'), ret.get('gateway'), ret.get('vlanid')
        except Exception as e:
            print("Error is %s" % e)


def isipalive():
    p = subprocess.Popen("nslookup qa.webex.com", stdin=PIPE, stdout=PIPE, shell=True)
    ret = p.stdout.readline()
    try:
        ret = re.match('Server', ret).group()
        return True
    except Exception as e:
        return False


gdfm = GetDataFromMongo()

timeout = 0
while timeout <= 30:
    if isipalive():
        print("IP is Alive")
        break
    else:
        time.sleep(3)
        timeout += 3


if not os.path.exists(r"/vmconfig/.changedhostname"):
    time.sleep(3)
    vmmacc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print("vmmacc is ", vmmacc)
    vmname = gdfm.getvminfo(vmmacc)
    print("vmname is", vmname)
    hostname, ipaddr = vmname.split('-', 1)
    ipaddr = re.sub('-ct74', '', ipaddr)
    netmask, gateway, vlanid = gdfm.getipinfo(ipaddr.split('-', 1)[0])
    cmd = "sh /vmconfig/vmconfig.sh {0} {1} {2} {3} > /vmconfig/vmconfig.log 2>&1".format(hostname, ipaddr, netmask,
                                                                                          gateway)

    if hostname:
        print(cmd)
        os.system(cmd)
        with open(r"/vmconfig/.changedhostname", 'w+') as f:
            f.write("Changed hostname {0} macc {1} done!".format(hostname, vmmacc))
        time.sleep(3)
        os.system("reboot")
