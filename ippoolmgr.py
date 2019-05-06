import multiprocessing
from multiprocessing import Pool
import threading
import pymongo
from IPy import IP
import argparse
import time
import random

MONGODB = "173.36.203.62"
gLock = threading.RLock


def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to mongodb')

    parser.add_argument('-s', '--ip_segment',
                        required=True,
                        action='store',
                        help='Ip Segment, eg.173.37.49.128/26')

    parser.add_argument('-n', '--netmask',
                        required=True,
                        default="255.255.255.0",
                        action='store',
                        help='netmask')

    parser.add_argument('-g', '--gateway',
                        required=True,
                        action='store',
                        help='Gateway')

    parser.add_argument('-v', '--vlanid',
                        required=False,
                        action='store',
                        help='Vlan Id')

    args = parser.parse_args()
    return args


class ManipulateDataToMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(MONGODB))
        self.mydb = self.client["ipmgr"]
        self.mycoll = self.mydb["ippool"]

    def querydata(self, ipaddr):

        try:
            myquery = {"ipaddr": ipaddr}
            ret = self.mycoll.find_one(myquery)
            if ret:
                return True
            return
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def insertdata(self, ipaddr, netmask, gateway, vlanid):

        try:
            mydict = {"ipaddr": ipaddr, "netmask": netmask, "gateway": gateway, "vlanid": vlanid}
            if ipaddr:
                self.mycoll.insert_one(mydict)
            print(("inserted ipaddr done for %s" % ipaddr))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def updatedata(self, ipaddr, netmask, gateway, vlanid):

        try:
            myquery = {"ipaddr": ipaddr}
            newvalues = {"$set": {"ipaddr": ipaddr, "netmask": netmask, "gateway": gateway, "vlanid": vlanid}}
            self.mycoll.update_one(myquery, newvalues)
            print(("updated ipaddr info done for %s" % ipaddr))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))


def ip_pool_mgr(ip):
    # print(ip, netmask, gateway, vlan_id)

    if not mdtm.querydata(str(ip)):
        mdtm.insertdata(str(ip), netmask, gateway, vlan_id)
    else:
        mdtm.updatedata(str(ip), netmask, gateway, vlan_id)


if __name__ == '__main__':

    mdtm = ManipulateDataToMongo()
    args = get_args()
    ip_segment = args.ip_segment
    netmask = args.netmask
    gateway = args.gateway
    vlan_id = args.vlanid
    print(ip_segment, netmask, gateway, vlan_id)
    ips = IP(ip_segment)

    jobs = []
    for ip in ips:
        process = threading.Thread(target=ip_pool_mgr, args=(ip,))
        jobs.append(process)

    for j in jobs:
        j.start()

    for j in jobs:
        j.join()
