#!/usr/bin/env python

__author__ = 'YongZhang'
__version__ = '1.0.0'
#coding:utf-8
import paramiko
import os
import socket
import time
import json
import difflib
import shutil

serverlists = {'J2ee': ['10.224.89.100'],'DPL':['10.224.89.211'],'MJS':['10.224.89.77'],'MRS':['10.224.89.186'],'Reminder':['10.224.89.101'],'AS':['10.224.89.39'],
               \
               'Superadmin': ['10.224.82.69'], 'CB': ['10.224.89.243'],  'WWP':['10.224.89.224'], 'RA':['10.224.89.240'],
               \
               'MMPMCC':['10.224.82.96'],'MMPMCS':['10.224.82.98'],'NBRDPS':['10.224.82.73'],'NBRVSS':['10.224.82.74'],'NBRWES':['10.224.82.72'],
               \
               'NBRWSS':['10.224.82.242'],'NBRMSC':['10.224.82.85'],'NBRMSS':['10.224.82.87'],'TSP':['10.224.54.164'],
               \
               'TahoeTS':['10.224.82.77'],'TahoeTAS':['10.224.82.79'],'TahoeMACC':['10.224.82.83'],'TPGW':['10.224.89.241'],'CMS':['10.224.82.40'],
               \
               'XMLAPI':['10.224.89.225'],'GLA':['10.224.82.70'],'WebACD':['10.224.82.100'],'ACDBRE':['10.224.82.101']
               }
servertypes = ['J2ee','DPL','MJS','MRS','Reminder','AS', 'Superadmin', 'CB','WWP','RA','MMPMCC','MMPMCS','NBRDPS','NBRVSS','NBRWES','NBRMSC','NBRMSS','NBRWSS',
               \
               'TahoeTS','TahoeMACC','TahoeTAS' ,'TPGW','CMS','TSP','XMLAPI','GLA','WebACD','ACDBRE']

new_html = '/www/htdocs/versionlist.html'
old_html = '/www/htdocs/versionlist_old.html'
diff_html = '/www/htdocs/diff.html'
json_file = '/tmp/pkgdict.json'
old_json_file = '/tmp/pkgdict_old.json'
report_date = time.strftime('%m/%d/%Y %H:%M:%S GMT',time.localtime(time.time()))
backup_date = time.strftime('%Y%m%d%H',time.localtime(time.time()))
backup_file = '/www/htdocs/history/versionlist_{0}.html'.format(backup_date)

PkgDict={}

def GetpkgInfo(type,server):
    if type == 'J2ee':
        command = 'sudo rpm -qa | grep -e WBXpagecommon -e WBXpage -e WBXadmin'
    elif type == 'DPL':
        command = 'sudo rpm -qa | grep -e static -e WBXclient.T3 -e WBXmsi.T3 -e WBXptool -e mjs'
    elif type == 'MJS':
        command = 'sudo rpm -qa | grep mjs'
    elif type == 'MRS':
        command = 'sudo rpm -qa | grep -e mrs -e mbs'
    elif type == 'Reminder':
        command = 'sudo rpm -qa | grep -e WBXreminder -e pagecommon -e logadmin'
    elif type == 'AS':
        command = 'sudo rpm -qa | grep WBXauth'
    elif type == 'Superadmin':
        command = 'sudo rpm -qa | grep WBXsuper'
    elif type == 'CB':
        command = 'sudo rpm -qa | grep WBXerk'
    elif type == 'WWP':
        command = 'sudo rpm -qa | grep WBXerk'
    elif type == 'RA':
        command = 'sudo rpm -qa | grep WBXerk'
    elif type == 'MMPMCC':
        command = 'sudo rpm -qa | grep WBXmcc'
    elif type == 'MMPMCS':
        command = 'sudo rpm -qa | grep WBXmcs'
    elif type == 'NBRDPS':
        command = 'sudo rpm -qa | grep WBXnbr'
    elif type == 'NBRVSS':
        command = 'sudo rpm -qa | grep WBXnbr'
    elif type == 'NBRWES':
        command = 'sudo rpm -qa | grep WBXnbr'
    elif type == 'NBRMSC':
        command = 'sudo rpm -qa | grep WBXmsc'
    elif type == 'NBRMSS':
        command = 'sudo rpm -qa | grep WBXmss'
    elif type == 'NBRWSS':
        command = 'sudo rpm -qa | grep -e WBXnbrwss -e pagecommon'
    elif type == 'TahoeTS':
        command = 'sudo rpm -qa | grep -e WBXjtel -e WBXmacc -e WBXtahoeas'
    elif type == 'TahoeMACC':
        command = 'sudo rpm -qa | grep -e WBXjtel -e WBXmacc -e WBXtahoeas'
    elif type == 'TahoeTAS':
        command = 'sudo rpm -qa | grep -e WBXjtel -e WBXmacc -e WBXtahoeas'
    elif type == 'TPGW':
        command = 'sudo rpm -qa | grep WBXtpgw'
    elif type == 'CMS':
        command = 'sudo rpm -qa | grep -e WBXcms -e WBXaudioclips'
    elif type == 'TSP':
        command = 'sudo rpm -qa | grep -e WBXpai'
    elif type == 'XMLAPI':
        command = 'sudo rpm -qa | grep -e WBXsxa -e WBXxmlapi.11 -e WBXxmlproxy'
    elif type == 'GLA':
        command = 'sudo rpm -qa | grep -e WBXgloballookupapi'
    elif type == 'WebACD':
        command = 'sudo rpm -qa | grep -e WBXacd '
    elif type == 'ACDBRE':
        command = 'sudo rpm -qa | grep -e WBXacd '


    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    hostname = ""
    ipaddr = ""
    for user, pwd in zip(['wbxbuilds'], ['P0w3rSupply!']): #['logs', 'wbxbuilds'], ['wbx@Aalogs', 'P0w3rSupply!'
        #print user, pwd
        try:
            ssh.connect(server, username=user, password=pwd,timeout=30)
            stdin, stdout, stderr = ssh.exec_command(command)
            hostname = socket.gethostbyaddr(server)[0]
            ipaddr = socket.gethostbyname(hostname)
            print hostname, ipaddr
            break
        except:
            pass

    PkgDict[type]={"build":[line.strip() for line in sorted(stdout.readlines())],"hostname":hostname,"ipaddr":ipaddr}
    #print PkgDict





def getDataFromJson(type,jsonfile=json_file):
    with open (jsonfile) as json_data:
        data = json.load (json_data)
        datadict = data[type]
        #print datadict
        #print datadict["hostname"], datadict["ipaddr"], datadict["build"]
        #print "rows are ", len (datadict["build"])
        rows = len (datadict["build"])
        hostname = datadict["hostname"]
        ipaddr = datadict["ipaddr"]
        build = datadict["build"]
        return rows,hostname,ipaddr,build





def writeHtmlHeader():

    if os.path.isfile(new_html):
        shutil.copy(new_html,backup_file)
        os.rename(new_html,old_html)
        d=os.popen('find /www/htdocs/history -mtime +5 -exec rm -f {} \;')

    with open(new_html,'a+') as html:
        html.write(
'''<html>
</style>
<head>
<title>Package Version Check List</title>
</head>
<body>
  <h1 style="font-style:italic">Package Version Check List on hf3wd</h1>
  <tr>
    <td>Report Date: {0} </td>
  </tr>
  <br>
   <a href="http://pvc.qa.webex.com/diff.html" target="_blank">Package Diff</a>
  </br>
<table border="1">
  <tr>
    <th>Server Type</th>
    <th>Hostname</th>
    <th>IP Address</th>
    <th>Build Version</th>
  </tr>
  '''.format(report_date)
)


def writeHtmlBody(type):

    rows = getDataFromJson(type)[0]
    hostname = getDataFromJson(type)[1]
    ipaddr = getDataFromJson(type)[2]
    build = getDataFromJson(type)[3]
    color = {0:'''bgcolor=""''',1:'''bgcolor="#50D050"'''}

    def isChanged(build):
        old_build = getDataFromJson (type, old_json_file)[3]
        #print "old_build is", old_build
        if build not in old_build:
            return color[1]
        else:
            return color[0]


    try:
        firstbuild = build[0]
    except:
        firstbuild = []


    with open (new_html, 'a+') as html:
        html.write (
'''
<tr>
    <td rowspan="{0}" align="center">{1}</td>
    <td rowspan="{0}" align="center">{2}</td>
    <td rowspan="{0}" align="center">{3}</td>
    <td {4}>{5}</td>
 </tr>

'''.format(rows,type,hostname,ipaddr,isChanged(firstbuild),firstbuild)
)

    if len(build) > 1:
        for build in build[1:]:
            with open(new_html,'a+') as html:
                html.write(
'''
  <tr>
    <td {0} >{1}</td>
  </tr>
'''.format(isChanged(build),build)
)



def writeHtmlTail():

    with open(new_html,'a+') as html:
        html.write(
'''
</table>
</body>
</html>
''')


def diffHtml(new,old):
    def readfile(filename):
        with open(filename,'rb') as f:
            text = f.read().splitlines()
        return text

    text1_lines = readfile(new)
    text2_lines = readfile(old)

    d = difflib.HtmlDiff()
    diff = d.make_file(text1_lines,text2_lines)

    with open(diff_html,'w+') as f:
        f.write(diff)


if __name__ == "__main__":



    for type,serverlist in serverlists.iteritems():
        print type,serverlist[0]
        server=serverlist[0]
        GetpkgInfo (type, server)

    if os.path.isfile (json_file):
        os.rename (json_file, old_json_file)

    PkgDict_json = json.dumps(PkgDict,sort_keys=True, indent=4, separators=(',', ': '))
    print PkgDict_json

    with open (json_file, 'a+') as f:
        f.write(PkgDict_json)


    writeHtmlHeader ()
    for type in servertypes:
        writeHtmlBody (type)
    writeHtmlTail ()

    diffHtml(new_html,old_html)
