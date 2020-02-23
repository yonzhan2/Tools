import os
import pymongo
import re, uuid
import time
import subprocess
from subprocess import Popen, PIPE


class GetDataFromMongo(object):
    def __init__(self, host="173.37.49.29"):
        self.host = host

    def getvminfo(self, vmmacc):
        try:
            client = pymongo.MongoClient("mongodb://{0}:2701/".format(self.host), connectTimeoutMS=60000)
            mydb = client["vmdb"]
            mycoll = mydb["vminfo"]
            mydict = {"vmmacc": vmmacc}
            vmname = mycoll.find_one(mydict).get("vmname")
            server_type = mycoll.find_one(mydict).get("servertype")
            return vmname, server_type
        except Exception as e:
            print("Error is %s" % e)

    def getipinfo(self, ipaddr):
        try:
            client = pymongo.MongoClient("mongodb://{0}:2701/".format(self.host), connectTimeoutMS=60000)
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
    time.sleep(5)
    vmmacc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    print("vmmacc is ", vmmacc)
    try:
        vmname, server_type = gdfm.getvminfo(vmmacc)
    except Exception as e:
        print("Didn't get vmname from Cassandra vmdb.")
    print("vmname is %s, server type is %s" % (vmname, server_type))
    hostname, ipaddr = vmname.split('-', 1)
    ipaddr = re.sub('-ct76', '', ipaddr)
    try:
        netmask, gateway, vlanid = gdfm.getipinfo(ipaddr.split('-', 1)[0])
    except Exception as e:
        print("Didn't get ipaddr from Cassandra ipmgr db.")
    cmd = "sh /vmconfig/vmconfig.sh {0} {1} {2} {3} {4} > /vmconfig/vmconfig.log 2>&1".format(hostname, ipaddr, netmask,
                                                                                              gateway, server_type)

    if hostname and ipaddr:
        print(cmd)
        os.system(cmd)
        with open(r"/vmconfig/.changedhostname", 'w+') as f:
            f.write("Changed hostname {0} macc {1} done!".format(hostname, vmmacc))
        os.system("sed -i 's/^python/#python/g' /etc/rc.d/rc.local")
        os.system("sed -i 's/^sh/#sh/g' /etc/rc.d/rc.local")
        os.system("reboot")
