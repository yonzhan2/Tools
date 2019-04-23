#!/usr/bin/env python

__author__ = 'YongZhang'
__version__ = '1.0.0'
# coding:utf-8
import paramiko
import os
import socket
import time
import json
import difflib
import shutil
import configparser
import requests
import telnetlib
import re
import string
import random
import urllib3
import pymongo

base_dir = os.path.dirname(os.path.abspath(__file__))
print(base_dir)
new_html = os.path.join(base_dir, 'versionlist.html')
old_html = os.path.join(base_dir, 'versionlist_old.html')
tmp_hmtl = os.path.join(base_dir, 'versionlist_tmp.html')
diff_html = os.path.join(base_dir, 'diff.html')
json_file = os.path.join(base_dir, 'pkgdict.json')
base_jsonfile = os.path.join(base_dir, 'pkgdict_base.json')
base_jsonfile_tmp = os.path.join(base_dir, 'pkgdict_base_tmp.json')
report_date = time.strftime('%m/%d/%Y %H:%M:%S GMT', time.localtime(time.time()))
backup_date = time.strftime('%Y%m%d%H', time.localtime(time.time()))
backup_file = os.path.join(base_dir, 'history/versionlist_{0}.html'.format(backup_date))
cur_hour = time.localtime().tm_hour
_lock = os.path.join(base_dir, '.lock')

MONGODB = "173.36.203.62"

PkgDict = {}
status = {}
rpmcmd = {}

env = "ATS"

cf = configparser.ConfigParser()
cf.read(os.path.join(base_dir, 'hckconfig.properties'))
secs = cf.sections()


def IsCT7():
    if os.uname()[2].startswith('3'):
        return True


def getCurrentTime():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))


class ManipulateDataToMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(MONGODB))
        self.mydb = self.client["build"]
        self.mycoll = self.mydb["buildinfo"]

    def querydata(self, ipaddr):

        try:
            myquery = {"ipaddr": ipaddr}
            ret = self.mycoll.find_one(myquery)
            if ret:
                return True
            return
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def insertdata(self, env, type, build, hostname, ipaddr):

        try:
            mydict = {"env": env, "type": type, "build": build, "hostname": hostname, "ipaddr": ipaddr,
                      "createtime": getCurrentTime()}
            self.mycoll.insert_one(mydict)
            print(("inserted done for %s" % hostname))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def updatedata(self, env, type, build, hostname, ipaddr):

        try:
            myquery = {"ipaddr": ipaddr}
            newvalues = {"$set": {"env": env, "type": type, "build": build, "hostname": hostname}}
            self.mycoll.update_one(myquery, newvalues)
            print(("updated build info done for %s" % ipaddr))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def updatestatus(self, ipaddr, status):

        try:
            myquery = {"ipaddr": ipaddr}
            newvalues = {"$set": {"status": status, "lastmodifiedtime": getCurrentTime()}}
            self.mycoll.update_one(myquery, newvalues)
            print(("updated status done for %s" % ipaddr))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def updatelastbuild(self, ipaddr):

        try:
            findone = self.mycoll.find_one({"ipaddr": ipaddr})
            currentbuild = findone.get("build")
            myquery = {"ipaddr": ipaddr}
            newvalues = {"$set": {"lastbuild": currentbuild}}
            self.mycoll.update_one(myquery, newvalues)
            print(("updated lastbuild done for %s" % ipaddr))
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))


##Initialize Class
m = ManipulateDataToMongo()

class HealthCheck:
    "get the server's health check status via the parameter input"

    def __init__(self, type):
        self.type = type
        self.ip, self.rpmcmd, self.hckurl = (cf.get(type, opt) for opt in cf.options(type))
        rpmcmd[type] = self.rpmcmd

    def getStatus(self):
        try:
            data = requests.get(self.hckurl, timeout=10)
            m_okokok = re.compile('OKOKOK', re.I)
            m_online = re.compile('online', re.I)
            if m_okokok.search(data.content.decode('utf-8')) or m_online.search(data.content.decode('utf-8')):
                status[self.type] = 'OKOKOK'
                m.updatestatus(self.ip, "OKOKOK")
                return "OKOKOK"
            else:
                status[self.type] = 'NONONO'
                m.updatestatus(self.ip, "NONONO")
                return 'NONONO'
        except:
            status[self.type] = 'NONONO'
            m.updatestatus(self.ip, "NONONO")
            return 'NONONO'


    def Telnet(self):
        try:
            tn = telnetlib.Telnet(self.ip, self.hckurl)
            tn.close()
            status[self.type] = 'OKOKOK'
            m.updatestatus(self.ip, "OKOKOK")
            return 'OKOKOK'
        except:
            status[self.type] = 'NONONO'
            m.updatestatus(self.ip, "NONONO")
            return 'NONONO'


class GetVersionList:

    def __init__(self, type, server):
        self.headers = {'Content-Type': 'application/json', 'trusted_username': 'atspvcapi',
                        'trusted_password': 'A09CD79673A777C70A0B307AA0B83866B6749BF1B380A815C4D5CDAE7E0F371D'}
        self.requesturl = 'https://slimg2bts.webex.com/slim/restservice/scriptwithep'
        self.checkurl = 'https://slimg2bts.webex.com/slim/restservice/routinesearch2'
        self.name = ''.join([random.choice(string.digits + string.ascii_letters) for _ in range(10)])
        self.type = type
        self.server = server

    def getExeId(self):
        data = '{script: {name:"%s", purpose:"SMT_INSTANT",scriptType:"Deployment",shareGroupId:0,content:"%s",scriptParameters:"",' \
               'comments:"testscript"},eps: [{name:"%s",purpose:"SMT_INSTANT",scheduleType:"INSTANT",targetType:"SERVER",targetOrder:"ALL_AT_ONCE",goOnCondition:"NULL",' \
               'startTime:"",endTime:"",targets:[{targetid:"","hostNameOrIP":"%s"}]}]}' % (
               self.name, rpmcmd[self.type], self.name, self.server)
        #print data
        try:
            req = requests.post(self.requesturl, headers=self.headers, data=data, verify=False)
            #print req.content
            ExeId = json.loads(req.content)['result']['result']['exeids'][0]
            return int(ExeId)
        except Exception as e:
            print(e)

    def getOutPut(self):

        data = '{exeId:%s,executionType:"script"}' % self.getExeId()
        time.sleep(10)
        try:
            urllib3.disable_warnings()
            req = requests.post(self.checkurl, headers=self.headers, data=data, verify=False)
            #print req.content
            screenout = json.loads(req.content)['result']['routineSearchResult'][0]['screenOut']
            return screenout
        except Exception as e:
            print(e)

    def getHostName(self, server):
        hostname = socket.gethostbyaddr(self.server)[0]
        ipaddr = socket.gethostbyname(hostname)
        return hostname, ipaddr

    def updateDict(self):

        if type not in ('HIPPO', 'FLAMINGO', 'OTTER', 'WebAppNG', 'AddIn', 'GlobalPageService', 'Notification'):
            p1 = re.compile(r"Name : (.+?) Relocations:.+? Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")
            p2 = re.compile(r"Build Date: (.+?) Install Date:")  ##Build Date
            p3 = re.compile(r"Install Date: (.+?) Build Host:")  ##Install Date
        else:
            p1 = re.compile(r"Name : (.+?) Version :(.+?) Release : (.+?) Architecture")
            p2 = re.compile(r"Build Date : (.+?) Build Host")  ##Build Date
            p3 = re.compile(r"Install Date: (.+?) Group")  ##Install Date

        f = self.getOutPut()
        print("content of f:", f)
        #print re.findall(p1, f)
        p1_ret = re.findall(p1, f)
        # print 'p1 :',p1_ret
        buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[1].strip(), build[2].strip()) for build in p1_ret]
        # print re.findall(p2, f)
        # print re.findall(p3, f)
        rpmdata = list(zip(buildsinfo, re.findall(p2, f), re.findall(p3, f)))
        rpmdata_format = list(zip(buildsinfo, [timeConvert(buildate)[0] for buildate in re.findall(p2, f)],
                                  [timeConvert(deploydate)[0] for deploydate in re.findall(p3, f)]))
        print(rpmdata)

        hostname = self.getHostName(self.server)[0]
        ipaddr = self.getHostName(self.server)[1]
        PkgDict[type] = {"build": [line for line in sorted(rpmdata)], "hostname": hostname, "ipaddr": ipaddr}
        build = [line for line in sorted(rpmdata_format)]

        if not m.querydata(ipaddr):
            m.insertdata(env, type, build, hostname, ipaddr)
        else:
            if not os.path.exists(_lock) and cur_hour in (2, 5):
                m.updatelastbuild(ipaddr)
            m.updatedata(env, type, build, hostname, ipaddr)
        # print PkgDict


def getDataFromJson(type, jsonfile=json_file):
    'Get data from jsonfile, return tuple'
    with open(jsonfile) as json_data:
        data = json.load(json_data)
        datadict = data[type]
        # print datadict
        rows = len(datadict["build"])
        hostname = datadict["hostname"]
        ipaddr = datadict["ipaddr"]
        build = datadict["build"]

        return rows, hostname, ipaddr,build


def timeConvert(s):
    try:
        timestruct = time.strptime(s, "%a %b %d %Y %H:%M:%S %p GMT")
    except:
        timestruct = time.strptime(s, "%a %d %b %Y %H:%M:%S %p GMT")

    timeformat = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    timestamp = time.mktime(timestruct)
    return timeformat, timestamp



def writeHtmlHeader():

    if os.path.isfile(new_html):
        try:
            shutil.move(new_html, backup_file)
            # os.rename(new_html, old_html)
            d = os.popen('find %s/history -mtime +31 -exec rm -f {} \;' % base_dir)
        except:
            pass

    os.system("touch {} && chmod 775 {}".format(new_html, new_html))
    with open(new_html, 'a+') as html:
        html.write(
            r'''<!DOCTYPE html>
            <html>
            </style>
            <head>
            <title>Package Version Check List</title>
                        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
                        <meta name="format-detection" content="telephone=no">
                        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
                        <meta name="slack-app-id" content="A5P5FDK33">
            
            </head>
            <body>
              <h1 style="font-style:italic">Package Version Check List on ATS</h1>
              <li>Current Location: {0} </li>
              <li>Report Date: {1} </li>
              <br>
               <a href="http://pvc.qa.webex.com/ats/diff.html" target="_blank">Package Diff</a>
              </br>
            <table border="1">
              <tr>
                <th>Server Type</th>
                <th>Hostname</th>
                <th>IP Address</th>
                <th>Build Date</th>
                <th>Deploy Date</th>
                <th>Build Version</th>
                <th>Service Status</th>
              </tr>
              '''.format('PRIMARY' if status.get('J2EE', 'NONONO') == 'OKOKOK' else 'GSB', report_date)
)


def writeHtmlBody(type):

    rows = getDataFromJson(type)[0]
    hostname = getDataFromJson(type)[1]
    ipaddr = getDataFromJson(type)[2]
    builds = getDataFromJson(type)[3]
    color = {0: '''bgcolor=""''', 1: '''bgcolor="#50D050"''', 2: '''bgcolor="#FF0000"'''}
    print('host,builds,t1', hostname, builds, timeConvert(builds[0][1])[0])
    print('host,t2', hostname, timeConvert(builds[0][2])[0])


    def isChanged(build):
        old_build = (build[0] for build in getDataFromJson(type, base_jsonfile)[3])
        # print "getdatafromjson is ",getDataFromJson (type, base_jsonfile)[3]
        #print "old_build is", old_build, "new build is" ,build
        if build not in old_build:
            return color[1]
        else:
            return color[0]

    def isRunning(type):
        if status.get(type, '') == 'OKOKOK' or status.get(type, '') == '' :
            return color[0]
        else:
            return color[2]

    'if not get the build version, return empty list'

    try:
        firstbuild = builds[0][0]
        #print "firstbuild is ",firstbuild
    except:
        firstbuild = []

    with open(new_html, 'a+') as html:
        html.write(
            '''
            <tr>
                <td rowspan="{0}" align="center">{1}</td>
                <td rowspan="{0}" align="center">{2}</td>
                <td rowspan="{0}" align="center">{3}</td>
                <td >{8}</td>
                <td >{9}</td>
                <td {4}>{5}</td>
                <td rowspan="{0}" align="center" {6}>{7}</td>
             </tr>
            
            '''.format(rows, type, hostname, ipaddr, isChanged(firstbuild), firstbuild, isRunning(type), status.get(type, ''),
           timeConvert(builds[0][1])[0], timeConvert(builds[0][2])[0])
)
    'If the length of build >1, write to file from the second entity'
    if len(builds) > 1:
        for build in builds[1:]:
            # print "build is" ,build
            with open(new_html, 'a+') as html:
                html.write(
                    '''
                      <tr>
                        <td >{0}</td>
                        <td >{1}</td>
                        <td {2} >{3}</td>
                      </tr>
                    '''.format(timeConvert(build[1])[0], timeConvert(build[2])[0], isChanged(build[0]), build[0])
)



def writeHtmlTail():
    with open(new_html, 'a+') as html:
        html.write(
            '''
            </table>
            </body>
            </html>
            ''')


def diffHtml(new,old):
    def readfile(filename):
        with open(filename, 'rb') as f:
            text = f.read().splitlines()
        return text

    text1_lines = readfile(new)
    text2_lines = readfile(old)

    d = difflib.HtmlDiff()
    diff = d.make_file(text1_lines, text2_lines)

    with open(diff_html, 'w+') as f:
        f.write(diff)

def writeHtml():
    writeHtmlHeader ()
    for type in secs:
        writeHtmlBody(type)
    writeHtmlTail ()

def transferToCI():
    f = open(json_file)
    data = json.load(f)
    cnvt = [{'buildDate': timeConvert(b[1])[1], 'deployDate': timeConvert(b[2])[1], 'name': b[0]} for i in
            list(data.values()) for b in i['build']]
    ret = json.dumps(cnvt, sort_keys=True, indent=4, separators=(',', ': '))
    # print 'Transfer content:',ret
    url = 'https://webexci.cisco.com/backend/data/v1/buildDeployHistory/ATS/packageList?appKey=qapvc&appSecret=6o6Rh1Nvvow3HRWodrBX2uGa57XtaoZrhF0ecCCMB7g'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    try:
        r = requests.post(url, headers=headers, data=ret)
        print('response staus is', r.status_code)
        print('response content is',r.content)
    except:
        print('call api failed')

if __name__ == "__main__":
    for type in secs:
        hck = HealthCheck (type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print(type, hck.ip, hck.getStatus ())
    # print 'url status is %s' % status

    for type in 'AppDBPatch', 'DPL', 'RA', 'TahoeTS-97', 'TahoeTS-99', 'WebACD', 'TSP', 'Notification':
        hck = HealthCheck(type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print(type, hck.ip, hck.Telnet())
    print('status is %s' % status)



    for type in secs:
        server = cf.get(type, 'ip')
        print(server)
        gv = GetVersionList(type,server)
        gv.updateDict()

    PkgDict_json = json.dumps(PkgDict, sort_keys=True, indent=4, separators=(',', ': '))
    # print PkgDict_json

    with open(json_file, 'w+') as f:
        f.write(PkgDict_json)

    if os.path.isfile(json_file) and not os.path.isfile(base_jsonfile) and not os.path.isfile(base_jsonfile_tmp):
        shutil.copy(json_file, base_jsonfile)
        shutil.copy(json_file, base_jsonfile_tmp)

    if os.path.isfile(new_html) and not os.path.isfile(old_html) and not os.path.isfile(tmp_hmtl):
        shutil.copy(new_html, old_html)
        shutil.copy(new_html,tmp_hmtl)

    def copyfile(source, destination):
        if not os.path.isfile(_lock) :
            try:
                shutil.copy(source, destination)
                #os.system('touch ' + _lock)
            except:
                pass


    if cur_hour == 0:
        copyfile(base_jsonfile_tmp, base_jsonfile)
        copyfile(tmp_hmtl, old_html)
        os.system('touch ' + _lock)
    elif cur_hour == 5:
        copyfile(base_jsonfile_tmp, base_jsonfile)
        copyfile(json_file, base_jsonfile_tmp)
        copyfile(tmp_hmtl, old_html)
        copyfile(new_html, tmp_hmtl)
        os.system('touch ' + _lock)
    else:
        os.system('rm -f ' + _lock)

    ###writehtml
    writeHtml()

    diffHtml(new_html, old_html)

    transferToCI()
