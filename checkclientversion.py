#!/usr/bin/env python

"Notify QA via spark room if the client version got changed!"

import os
import json
import urllib2

basedir = '/www/htdocs/client'
T33L = os.path.join(basedir, 'T33L')
versionfile = os.path.join(basedir, 'version.txt')


def SendMsgToSparkRoom(msg=None):
    sparkapi = 'https://api.ciscospark.com/v1/messages'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
    headers['User-Agent'] = useragent
    # roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
    # roomId = 'f5db8c60-ccd7-11e6-9531-cb44111e9102'  # CM Team room
    roomId = 'f9d8d2f0-d3d9-11e7-930f-29bf602b4e45'  ##this is Hardening Test Room
    data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
    data = json.dumps(data)
    # print data

    try:
        req = urllib2.Request(sparkapi, data=data, headers=headers)
        r = urllib2.urlopen(req)

        if r.code == 200:
            print "send msg successfully"
        # print r.code

    except Exception as e:
        print 'send msg failed', e
        pass


def GetCurrentClientVersion():
    if os.path.exists(basedir):
        rp = os.path.realpath(T33L)
        buildversion = os.path.basename(rp)
        currentversion = buildversion.split('-')[-1]
        print "Current Client Version is %s " % buildversion

    try:
        with open(versionfile, 'r') as f:
            data = json.load(f)
            preversion = data.get('T33L', 'N/A')
            isSend = data.get('isSend', 'False')
            if preversion != currentversion or not isSend:
                msg = "<@all>, Client Version Got Changed on hf3wd, Current Version is {0}".format(buildversion)
                SendMsgToSparkRoom(msg)
                with open(versionfile, 'w+') as f:
                    data['T33L'] = currentversion
                    data['isSend'] = True
                    f.write(json.dumps(data))
    except Exception as e:
        with open(versionfile, 'w+') as f:
            data = {'T33L': currentversion, 'isSend': False}
            print e, data
            f.write(json.dumps(data))


if __name__ == "__main__":
    GetCurrentClientVersion()
