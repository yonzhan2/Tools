#!/usr/local/bin/python

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
import ConfigParser
import requests
import telnetlib
import re
import cPickle as pickle
from subprocess import PIPE, Popen

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# base_dir = '/var/www/html'
base_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep
print base_dir
new_html = base_dir + 'versionlist.html'
old_html = base_dir + 'versionlist_old.html'
tmp_hmtl = base_dir + 'versionlist_tmp.html'
diff_html = base_dir + 'diff.html'
status_file = base_dir + 'status.json'
json_file = base_dir + 'pkgdict.json'
base_jsonfile = base_dir + 'pkgdict_base.json'
base_jsonfile_tmp = base_dir + 'pkgdict_base_tmp.json'
report_date = time.strftime('%m/%d/%Y %H:%M:%S GMT', time.localtime(time.time()))
backup_date = time.strftime('%Y%m%d%H', time.localtime(time.time()))
backup_file = base_dir + 'history/versionlist_{0}.html'.format(backup_date)
cur_hour = time.localtime().tm_hour
_lock = base_dir + '.lock'

PkgDict = {}
PkgDict_new = {}
status = {}
rpmcmd = {}
failure_dict = {}
max_failure = 3

cf = ConfigParser.ConfigParser()
cf.read(base_dir + 'hckconfig.properties')
secs = cf.sections()


# print secs


class HealthCheck:
    "get the server's health check status via the parameter input"

    def __init__(self, type):
        self.type = type
        self.ip, self.rpmcmd, self.hckurl = (cf.get(type, opt) for opt in cf.options(type))
        rpmcmd[type] = self.rpmcmd

    def getStatus(self):
        try:
            data = requests.get(self.hckurl, timeout=5)
            m_okokok = re.compile('OKOKOK', re.I)
            m_online = re.compile('online', re.I)
            if m_okokok.search(data.content) or m_online.search(data.content):
                status[self.type] = 'OKOKOK'
                return "OKOKOK"
            else:
                status[self.type] = 'NONONO'
                return 'NONONO'
        except:
            status[self.type] = 'NONONO'
            return 'NONONO'

    def Telnet(self):
        try:
            tn = telnetlib.Telnet(self.ip, self.hckurl)
            status[self.type] = 'OKOKOK'
            return 'OKOKOK'
        except:
            status[self.type] = 'NONONO'
            return 'NONONO'

    @classmethod
    def getCuspStatus(self, cusp, ip):

        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)

        # driver = webdriver.Firefox() # Instantiate a webdriver object
        driver.get('http://{}/admin/Common/HomePage.do'.format(ip))

        # print dir(driver)

        elem_user = driver.find_element_by_id("username")
        elem_user.send_keys("monitor")
        elem_pwd = driver.find_element_by_id("password")
        elem_pwd.send_keys("C!sco$cusp")
        elem_pwd.send_keys(Keys.RETURN)

        driver.switch_to.frame('contentiframe')
        ret = driver.find_element_by_xpath(".//*[@id='dash2']/fieldset/table/tbody/tr/td[2]").text

        if str(ret) == 'All Server Group Elements are up!':
            status[cusp] = str(ret)
            return True
        else:
            status[cusp] = str(ret)
            return False

        driver.close()
        driver.quit()


def GetpkgInfo(type, server):
    'Get Package info via the input paramter server type and server ip, return Package Info Dict'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hostname = ""
    ipaddr = ""
    for user, pwd in zip(['shuqli'], ['wbx@Aa$hfcm']):  # ['logs', 'wbxbuilds'], ['wbx@Aalogs', 'P0w3rSupply!'
        # print user, pwd
        try:
            ssh.connect(server, username=user, password=pwd, timeout=30)
            stdin, stdout, stderr = ssh.exec_command(rpmcmd[type])
            hostname = socket.gethostbyaddr(server)[0]
            ipaddr = socket.gethostbyname(hostname)
            print hostname, ipaddr
            break
        except:
            pass

    # p1 = re.compile(r"Source RPM: (.+?) Size :") ##Source RPM Name
    p1 = re.compile(r"Name : (.+?) Relocations:(.+?) Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")
    p2 = re.compile(r"Build Date: (.+?) Install Date:")  ##Build Date
    p3 = re.compile(r"Install Date: (.+?) Build Host:")  ##Install Date
    with open('/tmp/stdout', 'w+') as f:
        f.write(stdout.read())
    with open('/tmp/stdout') as fh:
        f = fh.read()
    # print "content of f:", f
    p1_ret = re.findall(p1, f)
    print 'p1 :', p1_ret
    buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[2].strip(), build[3].strip()) for build in p1_ret]
    # print re.findall(p2, f)
    # print re.findall(p3, f)
    rpmdata = zip(buildsinfo, re.findall(p2, f), re.findall(p3, f))
    print rpmdata

    # PkgDict[type]={"build":[line.strip() for line in sorted(stdout.readlines())],"hostname":hostname,"ipaddr":ipaddr}
    PkgDict[type] = {"build": [line for line in sorted(rpmdata)], "hostname": hostname, "ipaddr": ipaddr}
    # print PkgDict

    # PkgDict[type]={"build":[line.strip() for line in sorted(stdout.readlines())],"hostname":hostname,"ipaddr":ipaddr}
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
        return rows, hostname, ipaddr, build


def SendMsgToSparkRoom(msg=None):
    sparkapi = 'https://api.ciscospark.com/v1/messages'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
    headers['User-Agent'] = useragent
    # roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f' # test room
    roomId = '28e3c750-6908-11e6-a747-2b856e15b09b'  ##this is CMR Scrum Room
    data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
    data = json.dumps(data)
    # print data
    try:
        r = requests.post(sparkapi, headers=headers, data=data)
        if r.status_code == 200:
            print "send msg successfully"
        print r.status_code

    except Exception as e:
        print 'send msg failed', e
        pass


def writeHtmlHeader():
    if os.path.isfile(new_html):
        shutil.move(new_html, backup_file)
        # os.rename(new_html, old_html)
        d = os.popen('find {}history -mtime +5 -exec rm -f {} \;'.format(base_dir))

    with open(new_html, 'a+') as html:
        html.write(
            r'''<!DOCTYPE html>
            <html>
            </style>
            <head>
            <title>Package Version Check List</title>
            </head>
            <body>
              <h1 style="font-style:italic">Package Version Check List on DEV DMZ</h1>
                <li>iCUSP: {0} </li>
                <li>eCUSP: {1} </li>
                <li>Report Date: {2} </li>
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
              '''.format(status.get('iCUSP', 'Unknown'), status.get('eCUSP', 'Unknown'), report_date)
        )


def writeHtmlBody(type):
    rows = getDataFromJson(type)[0]
    hostname = getDataFromJson(type)[1]
    ipaddr = getDataFromJson(type)[2]
    builds = getDataFromJson(type)[3]
    color = {0: '''bgcolor=""''', 1: '''bgcolor="#50D050"''', 2: '''bgcolor="#FF0000"'''}

    def isChanged(build):
        # old_build = getDataFromJson (type, base_jsonfile)[3]
        old_build = (build[0] for build in getDataFromJson(type, base_jsonfile)[3])
        # print "old_build is", old_build
        if build not in old_build:
            return color[1]
        else:
            return color[0]

    def isRunning(type):
        if status.get(type, '') == 'OKOKOK' or status.get(type, '') == '':
            return color[0]
        else:
            return color[2]

    def timeConvert(s):
        try:
            timestruct = time.strptime(s, "%a %d %b %Y %I:%M:%S %p GMT")
        except:
            timestruct = time.strptime(s, "%a %b %d %H:%M:%S %Y")
        timeformat = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)

        timestamp = time.mktime(timestruct)
        # print 'timeformat',timeformat
        # print 'timestamp',timestamp
        return timeformat, timestamp

    'if not get the build version, return empty list'
    try:
        firstbuild = builds[0][0]
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
                        "[NONONO]{0}-{1} on DEV DMZ, Please Be Noticed! [link](http://pvc.dmz.webex.com/versionlist.html)".format(
                            type, ipaddr))
                    saveFailure(type)
                else:
                    SendMsgToSparkRoom(
                        'Exceeded the Maximum limit of Failure Notifications for  {0}-{1}'.format(type, ipaddr))
                    saveFailure(type, issend='Y')
    else:
        saveSuccess(type)


def saveSuccess(type, issend='N'):
    try:
        pkobj = pickle.load(open('failure', 'rb'))
        pkobj[type] = {'failure': 0, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open('failure', 'wb', True))
    except Exception as e:
        # print 'saveSuccess Failed ',e
        pkobj = {}
        pkobj[type] = {'failure': 0, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open('failure', 'wb', True))


def saveFailure(type, issend='N'):
    try:
        pkobj = pickle.load(open('failure', 'rb'))
        pkobj[type] = {'failure': pkobj[type].get('failure', 0) + 1, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open('failure', 'wb', True))
    except Exception as e:
        # print 'saveFailure failed ',e
        pkobj = {}
        pkobj[type] = {'failure': 1, 'issend': issend}
        failure_dict.update(pkobj)
        pd = pickle.dump(failure_dict, open('failure', 'wb', True))


def getFailure(type, issend='N'):
    try:
        pkobj = pickle.load(open('failure', 'rb'))
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


if __name__ == "__main__":
    for type in secs:
        hck = HealthCheck(type)
        print type, hck.ip, hck.getStatus()

    for type in 'DPL', 'TahoeTS-TSQ1', 'TahoeTS-TSQ2', 'TahoeTS-TSQ3':
        hck = HealthCheck(type)
        print type, hck.ip, hck.Telnet()

    cusps = {'iCUSP': '173.37.48.122', 'eCUSP': '173.37.48.124'}
    # cusps = {'iCUSP':'173.37.48.122'}
    for cusp, ip in cusps.items():
        print cusp, ip, HealthCheck.getCuspStatus(cusp, ip)
    print 'status is %s' % status

    for type in secs:
        server = cf.get(type, 'ip')
        # print server
        GetpkgInfo(type, server)
        time.sleep(2)

    PkgDict_json = json.dumps(PkgDict, sort_keys=True, indent=4, separators=(',', ': '))
    # print PkgDict_json

    status_json = json.dumps(status, sort_keys=True, indent=4, separators=(',', ': '))

    with open(json_file, 'w+') as f:
        f.write(PkgDict_json)

    with open(status_file, 'w+') as f:
        f.write(status_json)

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
                # os.system ('touch ' + _lock)
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
