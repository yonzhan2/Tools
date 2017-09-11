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
import ConfigParser
import requests
import telnetlib
import re

base_dir = '/www/htdocs/'
new_html = base_dir + 'versionlist.html'
old_html = base_dir + 'versionlist_old.html'
diff_html = base_dir + '/diff.html'
json_file = '/tmp/pkgdict.json'
base_jsonfile = '/tmp/pkgdict_base.json'
base_jsonfile_tmp = '/tmp/pkgdict_base_tmp.json'
report_date = time.strftime('%m/%d/%Y %H:%M:%S GMT', time.localtime(time.time()))
backup_date = time.strftime('%Y%m%d%H', time.localtime(time.time()))
backup_file = base_dir + '/history/versionlist_{0}.html'.format(backup_date)
cur_hour = time.localtime().tm_hour
_lock = '/tmp/.lock'

PkgDict = {}
status = {}
rpmcmd = {}


cf = ConfigParser.ConfigParser()
cf.read(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'hckconfig.properties')
secs = cf.sections()


#print secs


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


def GetpkgInfo(type, server):
    'Get Package info via the input paramter server type and server ip, return Package Info Dict'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hostname = ""
    ipaddr = ""
    for user, pwd in zip(['wbxbuilds'], ['P0w3rSupply!']):  # ['logs', 'wbxbuilds'], ['wbx@Aalogs', 'P0w3rSupply!'
        #print user, pwd
        try:
            ssh.connect(server, username=user, password=pwd, timeout=30)
            stdin, stdout, stderr = ssh.exec_command(rpmcmd[type])
            hostname = socket.gethostbyaddr(server)[0]
            ipaddr = socket.gethostbyname(hostname)
            print hostname, ipaddr
            break
        except:
            pass


    p1 = re.compile(r"Name : (.+?) Relocations:(.+?) Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")
    p2 = re.compile(r"Build Date: (.+?) Install Date:")  ##Build Date
    p3 = re.compile(r"Install Date: (.+?) Build Host:")  ##Install Date
    with open('/tmp/stdout', 'w+') as f:
        f.write(stdout.read())
    with open('/tmp/stdout') as fh:
        f = fh.read()
    # print "content of f:", f
    #print re.findall(p1, f)
    p1_ret = re.findall(p1, f)

    buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[2].strip(), build[3].strip()) for build in p1_ret]
    # print re.findall(p2, f)
    #print re.findall(p3, f)
    rpmdata = zip(buildsinfo, re.findall(p2, f), re.findall(p3, f))
    print rpmdata


    PkgDict[type] = {"build": [line for line in sorted(rpmdata)], "hostname": hostname, "ipaddr": ipaddr}
    print PkgDict


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
        timestruct = time.strptime(s, "%a %b %d %H:%M:%S %Y")
    except:
        timestruct = time.strptime(s, "%a %d %b %Y %H:%M:%S %p GMT")
    timeformat = time.strftime("%Y-%m-%d %H:%M:%S", timestruct)
    timestamp = time.mktime(timestruct)
    return timeformat, timestamp


def writeHtmlHeader():

    if os.path.isfile(new_html):
        try:
            shutil.copy(new_html, backup_file)
            os.rename(new_html, old_html)
            d = os.popen('find /www/htdocs/history -mtime +5 -exec rm -f {} \;')
        except:
            pass

    with open(new_html, 'a+') as html:
        html.write(
            r'''<!DOCTYPE html>
            <html>
            </style>
            <head>
            <title>Package Version Check List</title>
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

        #print "old_build is", old_build, "new build is" ,build
        if build not in old_build:
            return color[1]
        else:
            return color[0]

    def isRunning(type):
        if status.get(type, '') == 'OKOKOK' or status.get(type, '')  == '' :
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
    cnvt = [{'buildDate': timeConvert(b[1])[1], 'deployDate': timeConvert(b[2])[1], 'name': b[0]} for i in data.values()
            for b in i['build']]
    ret = json.dumps(cnvt, sort_keys=True, indent=4, separators=(',', ': '))
    # print 'Transfer content:',ret

    url = 'http://webexci.cisco.com/backend/data/v1/buildDeployHistory/QA/packageList?appKey=qapvc&appSecret=6o6Rh1Nvvow3HRWodrBX2uGa57XtaoZrhF0ecCCMB7g'
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    try:
        r = requests.post(url, headers=headers, data=ret)
        print 'response staus is', r.status_code
        print 'response content is',r.content
    except:
        print 'call api failed'

if __name__ == "__main__":
    for type in secs:
        hck = HealthCheck (type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print type, hck.ip, hck.getStatus ()
    # print 'url status is %s' % status

    for type in 'AppDBPatch', 'DPL', 'RA', 'TahoeTS', 'WebACD', 'TSP':
        hck = HealthCheck (type)
        # print hck.ip,hck.rpmcmd,hck.hckurl
        print type, hck.ip, hck.Telnet ()
    print 'status is %s' % status



    for type in secs:
        server = cf.get(type, 'ip')
        # print server
        GetpkgInfo(type, server)

    PkgDict_json = json.dumps(PkgDict, sort_keys=True, indent=4, separators=(',', ': '))
    # print PkgDict_json

    with open(json_file, 'w+') as f:
        f.write(PkgDict_json)

    if os.path.isfile(json_file) and not os.path.isfile(base_jsonfile) and not os.path.isfile(base_jsonfile_tmp):
        shutil.copy(json_file, base_jsonfile)
        shutil.copy(json_file, base_jsonfile_tmp)


    def copyfile(source, destination):
        if not os.path.isfile(_lock) :
            try:
                shutil.copy(source, destination)
                os.system('touch ' + _lock)
            except:
                pass


    if cur_hour == 0:
        copyfile(base_jsonfile_tmp, base_jsonfile)
    elif cur_hour == 5:
        copyfile(json_file, base_jsonfile_tmp)
    else:
        os.system('rm -f ' + _lock)



    ###writehtml
    writeHtml()

    diffHtml(new_html,old_html)


    transferToCI()
