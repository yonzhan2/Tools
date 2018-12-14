#!/usr/local/bin/python3
# coding:utf-8
'''
__author__ = 'YongZhang'
__version__ = '1.0.0'
'''
from __future__ import print_function
import OpenSSL
import ssl, socket
import requests
from datetime import datetime
import re
import json
import threading
import time

certlist = []
invalid = []


class CheckCertificate:
    def __init__(self):
        pass

    def getCetifcateList(self):
        url = 'http://labova.qa.webex.com/certs/lab-cisco-ca-certs.txt'
        r = requests.get(url)
        with open('certs.txt', 'w+') as f:
            f.write(r.content.decode('utf-8'))

        with open('certs.txt') as f:
            for line in f:
                if not line.startswith('#'):
                    p = re.compile(r"./sslcli submit generate local --cn (.+?) --privkey")
                    res = re.findall(p, line)
                    if res:
                        certlist.append(res[0])

        return certlist

    def checkExpiredDate(self, dns, lock=None):

        try:
            cert = ssl.get_server_certificate((dns, 443))
            # print('get ssl failed',e)

            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            ret = x509.get_notAfter().decode('utf-8')
            expiredate = datetime.strptime(ret, r"%Y%m%d%H%M%SZ")

            today = datetime.today()
            diff = (expiredate - today).days

            if diff > 31:
                pass
                print("[OKOKOK] %s,%d" % (dns, diff))
            elif 0 < diff <= 31:
                print("[NONONO] %s will be expired on %s" % (dns, expiredate))
                msg = "[NONONO] %s will be expired on %s" % (dns, expiredate)
                self.SendMsgToSparkRoom(msg)
                invalid.append(dns)
            else:
                print("[NONONO] %s expired on %s" % (dns, expiredate))
                msg = "[NONONO] %s expired on %s" % (dns, expiredate)
                self.SendMsgToSparkRoom(msg)
                invalid.append(dns)
        except Exception as e:
            print(dns, e)
            invalid.append(dns)
            print(invalid)
            msg = "%s %s" % (dns, e)
            self.SendMsgToSparkRoom(msg)

    def SendMsgToSparkRoom(self, msg=None):
        sparkapi = 'https://api.ciscospark.com/v1/messages'
        useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/61.0.3163.79 Safari/537.36'
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi',
                   'User-Agent': useragent}
        # headers['User-Agent'] = useragent
        roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
        # roomId = 'f5db8c60-ccd7-11e6-9531-cb44111e9102'    # this is CM Team ROOM
        data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
        data = json.dumps(data)
        # print data
        try:
            r = requests.post(sparkapi, headers=headers, data=data)
            if r.status_code == 200:
                pass
                # print("send msg successfully")
            # print(r.status_code)

        except Exception as e:
            print('send msg failed', e)
            pass


class MyThread(threading.Thread):
    def __init__(self, dns):
        threading.Thread.__init__(self)
        self.dns = dns
        self.cc = CheckCertificate()

    def run(self):
        self.cc.checkExpiredDate(self.dns)


if __name__ == '__main__':

    cc = CheckCertificate()
    cc.SendMsgToSparkRoom(
        "Checking Certificate Expired Date [link](http://labova.qa.webex.com/certs/lab-cisco-ca-certs.txt) ...")
    # manager = Manager()
    # q = manager.Queue()
    # lock = manager.RLock()
    # p = Pool()
    # for dns in cc.getCetifcateList():
    #     p.apply_async(cc.checkExpiredDate,args=(dns,lock))
    # p.close()
    # p.join()
    # for dns in cc.getCetifcateList():
    #     cc.checkExpiredDate(dns)
    # print('main',cc.invalid)
    threads = []
    for dns in cc.getCetifcateList():
        threads.append(MyThread(dns))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # time.sleep(60)
    if len(invalid) == 0:
        cc.SendMsgToSparkRoom("Perfect, No Issue Found!")
    elif len(invalid) == 1:
        cc.SendMsgToSparkRoom("Oops, %s Issue Found!" % len(invalid))
    else:
        cc.SendMsgToSparkRoom("Oops, %s Issues Found!" % len(invalid))
