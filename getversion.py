#!/usr/local/bin/python3

__author__ = 'YongZhang'
__version__ = '2.0.0'
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
import pickle as pickle
import pymongo

requests.packages.urllib3.disable_warnings()

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
failure = os.path.join(base_dir, 'failure')
cur_hour = time.localtime().tm_hour
_lock = os.path.join(base_dir, '.lock')

MONGODB = "173.36.203.62"

PkgDict = {}
status = {}
rpmcmd = {}
failure_dict = {}
max_failure = 3
env = "QA-hf3wd"

cf = configparser.ConfigParser()
cf.read(os.path.join(base_dir, 'hckconfig.properties'))
secs = cf.sections()


# print secs

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
            if build and ipaddr:
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
            data = requests.get(self.hckurl, verify=False, timeout=5)
            # print(f"data is {data.content.decode('utf-8')}")
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


def GetpkgInfo(type, server):
    'Get Package info via the input paramter server type and server ip, return Package Info Dict'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hostname = ""
    ipaddr = ""
    for user, pwd in list(zip(['wbxbuilds', 'wbxroot'],
                              ['P0w3rSupply!', 'wbx@AaR00t'])):  # ['logs', 'wbxbuilds'], ['wbx@Aalogs', 'P0w3rSupply!'
        print(user, pwd)
        try:
            ssh.connect(server, username=user, password=pwd, timeout=5)
            stdin, stdout, stderr = ssh.exec_command(rpmcmd[type])
            hostname = socket.gethostbyaddr(server)[0]
            ipaddr = socket.gethostbyname(hostname)
            print(hostname, ipaddr)
            break
        except Exception as e:
            print("error is ", e)

    output = stdout.read().decode('utf-8')
    package = re.findall("Name : (.*?)\s", output)
    release = re.findall("Version : (.*?)\s", output)
    version = re.findall("Release : (.*?)\s", output)

    p1 = list(zip(package, release, version))
    p2 = re.compile(r"Build Date\s*: (.*?\d{4})")
    p3 = re.compile(r"Install Date\s*: (.*?\d{4})")

    if type in ('AppDBPatch',):
        p2 = re.compile(r"Build Date\s*: (.+?\d{2}:\d{2}:\d{2})")
        p3 = re.compile(r"Install Date\s*: (.+?\d{2}:\d{2}:\d{2})")

    print("#1.content of output:", output)

    buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[1].strip(), build[2].strip()) for build in p1]
    build_data = re.findall(p2, output)
    install_data = re.findall(p3, output)
    print("build_data is {}, install_data is {}".format(build_data, install_data))
    rpmdata = list(zip(buildsinfo, build_data, install_data))
    rpmdata_format = list(zip(buildsinfo, [timeConvert(build)[0] for build in build_data],
                              [timeConvert(install)[0] for install in install_data]))
    print("rpmdata is ", rpmdata)

    build = [line for line in sorted(rpmdata, key=lambda x: x[0].lower())]
    PkgDict[type] = {"build": build, "hostname": hostname, "ipaddr": ipaddr}

    build = [line for line in sorted(rpmdata_format, key=lambda x: x[0].lower())]
    if not build:
        build = [('N/A', 'N/A', 'N/A')]
    if not m.querydata(ipaddr):
        m.insertdata(env, type, build, hostname, ipaddr)
    else:
        if not os.path.exists(_lock) and cur_hour in (4, 22):
            m.updatelastbuild(ipaddr)
        m.updatedata(env, type, build, hostname, ipaddr)


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

        return rows, hostname, ipaddr, build


def SendMsgToSparkRoom(msg=None):
    sparkapi = 'https://api.ciscospark.com/v1/messages'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
    headers['User-Agent'] = useragent
    roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
    # roomId = 'ac617a80-24cb-11e7-a0ed-cf98f532c071' ##this is T32 Firedrill Room
    data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
    data = json.dumps(data)
    # print data
    try:
        r = requests.post(sparkapi, headers=headers, data=data)
        if r.status_code == 200:
            print("send msg successfully")
        print(r.status_code)

    except Exception as e:
        print('send msg failed', e)
        pass


def timeConvert(s):
    try:
        timestruct = time.strptime(s, "%a %b %d %H:%M:%S %Y")
    except:
        timestruct = time.strptime(s, "%a %d %b %Y %H:%M:%S")
    timeformat = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    timestamp = time.mktime(timestruct)
    return timeformat, timestamp


def writeHtmlHeader():
    if os.path.isfile(new_html):
        try:
            shutil.move(new_html, backup_file)
            # os.rename(new_html, old_html)
            # d = os.popen('find {}/history -mtime +5 -exec rm -f {} \;'.format(base_dir))
            d = os.popen('find %s/history -mtime +5 -exec rm -f {} \;' % base_dir)
        except:
            pass

    with open(new_html, 'a+') as html:
        html.write(
            r'''<!DOCTYPE html>
            <html>
            <head>
            <title>Package Version Check List</title>
            <meta http-equiv="X-UA-Compatible" content="IE=Edge">
            <meta name="format-detection" content="telephone=no">
            <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
            <meta name="slack-app-id" content="A5P5FDK33">
            </head>
            <body>
              <h1 style="font-style:italic">Package Version Check List on hf3wd</h1>
              <li>Current Location: {0} </li>
              <li>Report Date: {1} </li>
              <br>
               <a href="http://pvc.qa.webex.com/diff.html" target="_blank">Package Diff</a>
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
    rows, hostname, ipaddr, builds = getDataFromJson(type)
    color = {0: '''bgcolor=""''', 1: '''bgcolor="#50D050"''', 2: '''bgcolor="#FF0000"'''}

    def isChanged(build):
        old_build = (build[0] for build in getDataFromJson(type, base_jsonfile)[3])

        # print "old_build is", old_build, "new build is" ,build
        if build not in old_build:
            return color[1]
        else:
            return color[0]

    def isRunning(type):
        if status.get(type, '') == 'OKOKOK' or status.get(type, '') == '':
            return color[0]
        else:
            return color[2]

    'if not get the build version, return empty list'

    try:
        firstbuild = builds[0][0]
        # print "firstbuild is ",firstbuild
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

            '''.format(rows, type, hostname, ipaddr, isChanged(firstbuild), firstbuild, isRunning(type),
                       status.get(type, ''),
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

    if status.get(type, '') != 'OKOKOK':
        # print getFailure(type)
        failure = getFailure(type)['failure']
        issend = getFailure(type)['issend']
        if time.localtime().tm_hour not in (0, 4):
            if issend != 'Y':
                if failure < max_failure:
                    SendMsgToSparkRoom(
                        "[NONONO]{0}-{1} on QA hf3wd, Please Be Noticed! [link](http://pvc.qa.webex.com/versionlist.html)".format(
                            type, ipaddr))
                    saveFailure(type)
                else:
                    SendMsgToSparkRoom(
                        'Exceeded the Maximum limit of Failure Notifications for {0}-{1}'.format(type, ipaddr))
                    saveFailure(type, issend='Y')
    else:
        saveSuccess(type)


def saveSuccess(type, issend='N'):
    try:
        pkobj = pickle.load(open(failure, 'rb'))
        pkobj[type] = {'failure': 0, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open(failure, 'wb', True))
    except Exception as e:
        # print 'saveSuccess Failed ',e
        pkobj = {}
        pkobj[type] = {'failure': 0, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open(failure, 'wb', True))


def saveFailure(type, issend='N'):
    try:
        pkobj = pickle.load(open(failure, 'rb'))
        pkobj[type] = {'failure': pkobj[type].get('failure', 0) + 1, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open(failure, 'wb', True))
    except Exception as e:
        # print 'saveFailure failed ',e
        pkobj = {}
        pkobj[type] = {'failure': 1, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open(failure, 'wb', True))


def getFailure(type, issend='N'):
    try:
        pkobj = pickle.load(open(failure, 'rb'))
        return pkobj[type]
    except Exception as e:
        # print 'getFailure failed',e
        return {'failure': 0, 'issend': issend}


def writeHtmlTail():
    with open(new_html, 'a+') as html:
        html.write(
            '''
            </table>
            </body>
            </html>
            ''')


def diffHtml(new, old):
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
    writeHtmlHeader()
    for type in secs:
        writeHtmlBody(type)
    writeHtmlTail()


def transferToCI():
    f = open(json_file)
    data = json.load(f)
    cnvt = [{'buildDate': timeConvert(b[1])[1], 'deployDate': timeConvert(b[2])[1], 'name': b[0]} for i in
            list(data.values())
            for b in i['build']]
    ret = json.dumps(cnvt, sort_keys=True, indent=4, separators=(',', ': '))
    # print 'Transfer content:',ret

    url = 'https://webexci.cisco.com/backend/data/v1/buildDeployHistory/QA/packageList?appKey=qapvc&appSecret=6o6Rh1Nvvow3HRWodrBX2uGa57XtaoZrhF0ecCCMB7g'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    try:
        r = requests.post(url, headers=headers, data=ret)
        print('response staus is', r.status_code)
        print('response content is', r.content)
    except:
        print('call api failed')


if __name__ == "__main__":
    for type in secs:
        hck = HealthCheck(type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print(type, hck.ip, hck.getStatus())
    # print 'url status is %s' % status

    for type in 'AppDBPatch', 'DPL', 'RA', 'WebACD', 'TSP':
        hck = HealthCheck(type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print(type, hck.ip, hck.Telnet())
    # print 'status is %s' % status

    for type in secs:
        server = cf.get(type, 'ip')
        print(server)
        GetpkgInfo(type, server)

    PkgDict_json = json.dumps(PkgDict, sort_keys=True, indent=4, separators=(',', ': '))
    # print PkgDict_json

    with open(json_file, 'w+') as f:
        f.write(PkgDict_json)

    if os.path.isfile(json_file) and not os.path.isfile(base_jsonfile) and not os.path.isfile(base_jsonfile_tmp):
        shutil.copy(json_file, base_jsonfile)
        shutil.copy(json_file, base_jsonfile_tmp)

    if os.path.isfile(new_html) and not os.path.isfile(old_html) and not os.path.isfile(tmp_hmtl):
        shutil.copy(new_html, old_html)
        shutil.copy(new_html, tmp_hmtl)


    def copyfile(source, destination):
        if not os.path.isfile(_lock):
            try:
                shutil.copy(source, destination)
                # os.system('touch ' + _lock)
            except:
                pass


    if cur_hour == 0:
        copyfile(base_jsonfile_tmp, base_jsonfile)
        copyfile(json_file, base_jsonfile_tmp)
        copyfile(tmp_hmtl, old_html)
        os.system('touch ' + _lock)
    elif cur_hour == 5:
        copyfile(base_jsonfile_tmp, base_jsonfile)
        copyfile(json_file, base_jsonfile_tmp)
        copyfile(tmp_hmtl, old_html)
        copyfile(new_html, tmp_hmtl)
        os.system('touch ' + _lock)
    elif cur_hour in (4, 22):
        copyfile(json_file, base_jsonfile_tmp)
        os.system('touch ' + _lock)
    else:
        os.system('rm -f ' + _lock)

    ###writehtml
    # writeHtml()

    try:
        diffHtml(new_html, old_html)
    except:
        pass

    transferToCI()
