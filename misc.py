# -*- coding:utf-8 -*-
# # html_doc = """
# # <html><head><title>The Dormouse's story</title></head>
# # <body>
# # <p class="title"><b>The Dormouse's story</b></p>
# #
# # <p class="story">Once upon a time there were three little sisters; and their names were
# # <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# # <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# # <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# # and they lived at the bottom of a well.</p>
# #
# # <p class="story">...</p>
# # """
# #
# # from bs4 import BeautifulSoup
# # soup = BeautifulSoup(html_doc, 'html.parser')
# #
# # #print(soup.prettify())
# #
# # print soup.title.string
# #
# # print soup.find_all('a')[0]['id']
# # print soup.get_text()
#
#
# # coding=utf-8
# # from selenium import webdriver
# # import unittest, time
# # class TestLogin(unittest.TestCase):
# #     def setUp(self):
# #         self.driver = webdriver.Firefox()
# #         self.driver.maximize_window()
# #         self.driver.implicitly_wait(5)
# #         self.base_url = "http://mail.qa.webex.com"
# #         self.verificationErrors = []
# #         self.accept_next_alert = True
# #     def test_login(self):
# #         driver = self.driver
# #         driver.get(self.base_url)
# #
# #         driver.find_element_by_id("usernameshow").clear()
# #         driver.find_element_by_id("usernameshow").send_keys("yonzhan2@qa.webex.com")
# #         driver.find_element_by_id("pwshow").clear()
# #         driver.find_element_by_id("pwshow").send_keys("Aa1234")
# #         driver.find_element_by_class_name("Bsbttn").click()
# #         print driver.find_elements_by_tag_name('frame')
# #         driver.switch_to.frame('f1')
# #         driver.find_element_by_xpath('html/body/a[2]').click()
# #         driver.implicitly_wait(2)
# #         print driver.window_handles
# #         #driver.switch_to.window(driver.window_handles[0])
# #         print driver.find_elements_by_tag_name('frame')
# #         #driver.switch_to.parent_frame(driver.switch_to.frame('f1'))
# #         driver.switch_to.default_content()
# #         driver.switch_to.frame('f2')
# #         driver.switch_to.frame('f3')
# #         driver.find_element_by_xpath('html/body/form/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/input').send_keys('yonzhan2@qa.webex.com')
# #         driver.find_element_by_xpath('html/body/form/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/input').send_keys('test by yong' + '_'  +  str(time.time()))
# #         driver.find_element_by_xpath(".//*[@id='EasyMail_Text']").send_keys('test')
# #         #upload file
# #         driver.switch_to.default_content()
# #         #driver.switch_to.frame('f1')
# #         driver.switch_to.frame('f2')
# #         #driver.switch_to.frame('f3')
# #         driver.switch_to.frame('f4')
# #         upload = driver.find_element_by_class_name('textbox')
# #         upload.send_keys('/tmp/progress.log')
# #         print upload.get_attribute('value')
# #         driver.find_element_by_xpath('html/body/form/table/tbody/tr/td/input[3]').click()
# #         driver.switch_to.default_content()
# #         driver.switch_to.frame('f2')
# #         driver.switch_to.frame('f3')
# #         time.sleep(5)
# #         driver.find_element_by_xpath('html/body/form/table/tbody/tr[1]/td/input[1]').click()
# #         driver.implicitly_wait(5)
# #         driver.switch_to.default_content()
# #         #driver.switch_to.parent_frame()
# #         #driver.switch_to.frame('f1')
# #         #driver.switch_to.frame('f2')
# #         #driver.find_element_by_xpath('html/body/table/tbody/tr/td[2]/form/table/tbody/tr[4]/td/input').click()
# #         #driver.find_element_by_class_name('Bsbttn').click()
# #     def tearDown(self):
# #         self.driver.quit()
# #         self.assertEqual([], self.verificationErrors)
# # if __name__ == "__main__":
# #     unittest.main()
#
#
# # def timeConvert(s, isGMT8=True):
# #     if isGMT8:
# #         return s[-4:] + '-' + s[4:7] + '-' + s[8:10] + ' ' + s[11:-5] + ' GMT+08:00'
# #     else:
# #         return s[-4:] + '-' + s[4:7] + '-' + s[8:10] + ' ' + s[11:-5] + ' GMT-07:00'
# # print timeConvert(rpmdata[0][1])
# #
# #
# #
# # builds = [('WBXsuper-32.5.0-679.src.rpm', 'Wed Jul 26 08:48:54 2017', 'Wed Jul 26 23:38:00 2017'), ('WBXsuperui-32.5.0-679.src.rpm', 'Wed Jul 26 08:49:09 2017', 'Wed Jul 26 23:37:33 2017')]
# #
# # for build in builds:
# #     print build[0],
# # if 'WBXsuper-32.5.0-679.src.rpm' in (build[0],):
# #     print True
# # else:
# #     print False
# #
# # from datetime import datetime,timedelta,tzinfo
# # import time
# # class GMT8(tzinfo):
# #     delta=timedelta(hours=8)
# #     def utcoffset(self,dt):
# #         return self.delta
# #     def tzname(self,dt):
# #         return "GMT+8"
# #     def dst(self,dt):
# #         return self.delta
# #
# # class GMT(tzinfo):
# #     delta=timedelta(0)
# #     def utcoffset(self,dt):
# #         return self.delta
# #     def tzname(self,dt):
# #         return "GMT+0"
# #     def dst(self,dt):
# #         return self.delta
# # from_tzinfo=GMT()#GMT tz +0
# # local_tzinfo=GMT8()#Local tz,+8
# # gmt_time = datetime.strptime('2011-08-15 21:17:14', '%Y-%m-%d %H:%M:%S')
# # gmt_time = gmt_time.replace(tzinfo=from_tzinfo)
# # local_time = gmt_time.astimezone(local_tzinfo)
# #
# # print gmt_time,local_time
# #
#
#
#
# #
# # import paramiko,re,socket
# # ssh = paramiko.SSHClient()
# # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #
# # p1 = re.compile(r"Name : (.+?) Relocations:(.+?) Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")  #(.+?)Release :  Build Date:
# # p2 = re.compile(r"Build Date: (.+?) Install Date:")
# # p3 = re.compile(r"Install Date: (.+?) Build Host:")
# # PkgDict = {}
# # #server="10.224.89."
# # #rpmcmd= "for i in `sudo rpm -qa|grep WBXpage`; do echo `sudo rpm -qi $i` ;done"
# # type='Superadmin'
# # server = "10.224.82.69"
# # rpmcmd = "for i in `sudo rpm -qa|grep WBXsuper`; do echo `sudo rpm -qi $i` ;done"
# # for user, pwd in zip(['wbxbuilds'], ['P0w3rSupply!']):
# #     try:
# #         ssh.connect(server, username=user, password=pwd,timeout=30)
# #         stdin, stdout, stderr = ssh.exec_command(rpmcmd)
# #         break
# #     except:
# #         pass
# # with open('/tmp/stdout','w+') as f:
# #     f.write(stdout.read())
# # with open('/tmp/stdout') as fh:
# #     f = fh.read()
# # print "content of f:" ,f
# # p1_ret = re.findall(p1, f)
# # print 'p1 :',p1_ret
# # buildsinfo = [ '{0}-{1}-{2}'.format(build[0].strip(),build[2].strip(),build[3].strip()) for build in p1_ret]
# #
# # print buildsinfo
# #
# # print 'p2', re.findall(p2,f)
# # print 'p3', re.findall(p3,f)
# # rpmdata = zip(buildsinfo, re.findall(p2, f), re.findall(p3, f))
# # print rpmdata
# # PkgDict[type] = {"builds": [line for line in sorted(rpmdata)]}
# # print 'it is' , PkgDict
# #
# #
# # import time,datetime
# # # print time.strftime("%Y-%m-%d %H:%M:%S",time.strptime("Thu Nov 08 17:15:30 +0800 2012", "%a %b %d %H:%M:%S +0800 %Y"))
# # #
# # print time.strftime("%Y-%m-%d %H:%M:%S", time.strptime("Fri 30 Jun 2017 07:49:46 PM GMT", "%a %d %b %Y %H:%M:%S %p GMT"))
# #
# # t1 = time.mktime(time.strptime("Fri 28 Jul 2017 02:00:01 PM GMT", "%a %d %b %Y %I:%M:%S %p GMT"))
# # #t2 = time.mktime(time.strptime("Fri 30 Jun 2017 07:49:45 PM GMT", "%a %d %b %Y %H:%M:%S %p GMT"))
# #
# # #print time.mktime(time.localtime())
# # print 't1',t1
#
# #
# # print time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(t1))
# # print time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(t2))
# # 1501250401
# #
# # def timeConvert(s):
# #     timestruct = time.strptime(s, "%a %d %b %Y %I:%M:%S %p GMT")
# #     timeformat = time.strftime("%Y-%m-%d %H:%M:%S",timestruct)
# #     timestamp = time.mktime(timestruct)
# #     return timeformat,timestamp
# #
# # #print timeConvert(p2[0])[0]
# #
# #
# # import requests
# # url = 'http://10.224.57.21:8090/data/v1/buildDeployHistory/QA/packageList?appKey=qatest&appSecret=CntbrbG-aSTCHdYe3Pa8NrT7XtlMGEKV2NSlD9B_Xmk'
# # headers= {'Content-Type':'application/json;charset=UTF-8'}
# # try:
# #     r = requests.post(url,headers=headers,data=("name"))
# #     print 'response staus is', r.status_code
# #     print 'response content is', r.content
# # except:
# #     print "call api failed"
# #
# #
#
# #
# #
# # import requests
# # import json
# #
# #
# # def SendMsgToSparkRoom(msg=None):
# #     sparkapi = 'https://api.ciscospark.com/v1/messages'
# #     useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
# #     headers = {'Content-Type': 'application/json;charset=UTF-8',
# #                'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
# #     headers['User-Agent'] = useragent
# #     roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
# #     # roomId = '28e3c750-6908-11e6-a747-2b856e15b09b' ##this is CMR Scrum Room
# #     data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
# #     data = json.dumps(data)
# #     # print data
# #     try:
# #         r = requests.post(sparkapi, headers=headers, data=data)
# #         if r.status_code == 200:
# #             print "send msg successfully"
# #         print r.status_code
# #
# #     except Exception as e:
# #         print 'send msg failed', e
# #         pass
# #
# #
# # SendMsgToSparkRoom("test from python1 @yonzhan2@cisco.com")
#
# # import paramiko,socket,re
# #
# # server = '10.224.38.115'
# # rpmcmd = 'for i in `sudo rpm -qa|grep WBXappdb`; do echo `sudo rpm -qi $i` ;done'
# # ssh = paramiko.SSHClient()
# # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# #
# # hostname = ""
# # ipaddr = ""
# # for user, pwd in zip(['wbxbuilds'], ['P0w3rSupply!']):  # ['logs', 'wbxbuilds'], ['wbx@Aalogs', 'P0w3rSupply!'
# #     #print user, pwd
# #     try:
# #         ssh.connect(server, username=user, password=pwd, timeout=30)
# #         stdin, stdout, stderr = ssh.exec_command(rpmcmd)
# #         hostname = socket.gethostbyaddr(server)[0]
# #         ipaddr = socket.gethostbyname(hostname)
# #         print hostname, ipaddr
# #         break
# #     except:
# #         pass
# #     p1 = re.compile(r"Name : (.+?) Relocations:(.+?) Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")
# #     p2 = re.compile(r"Build Date: (.+?) Install Date:")  ##Build Date
# #     p3 = re.compile(r"Install Date: (.+?) Build Host:")  ##Install Date
# #     with open('/tmp/stdout', 'w+') as f:
# #         f.write(stdout.read())
# #     with open('/tmp/stdout') as fh:
# #         f = fh.read()
# #         p1_ret = re.findall(p1, f)
# #
# #         buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[2].strip(), build[3].strip()) for build in p1_ret]
# #         # print re.findall(p2, f)
# #         # print re.findall(p3, f)
# #         rpmdata = zip(buildsinfo, re.findall(p2, f), re.findall(p3, f))
# #         print rpmdata
# # import psutil
# # import requests
# # import json
# # import time
# #
# # date = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
# #
# # def SendMsgToSparkRoom(msg=None):
# #     sparkapi = 'https://api.ciscospark.com/v1/messages'
# #     useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
# #     headers = {'Content-Type': 'application/json;charset=UTF-8',
# #                'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
# #     headers['User-Agent'] = useragent
# #     roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
# #     # roomId = '28e3c750-6908-11e6-a747-2b856e15b09b' ##this is CMR Scrum Room
# #     data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
# #     data = json.dumps(data)
# #     # print data
# #     try:
# #         r = requests.post(sparkapi, headers=headers, data=data)
# #         if r.status_code == 200:
# #             print "send msg successfully"
# #         print r.status_code
# #
# #     except Exception as e:
# #         print 'send msg failed', e
# #         pass
# #
# #
# # # SendMsgToSparkRoom("test from python1 @yonzhan2@cisco.com")
# #
# # def checkurl(url):
# #     r = requests.get(url)
# #     content = r.content
# #     if content != 'OKOKOK':
# #         SendMsgToSparkRoom('Test failed with',url,date)
# #     else:
# #         print 'Test OKOKOK with',url,date
#
#
# # urllist = ['http://10.224.89.58:1801/webex/apachepolltom.php?wd=hf3wd&type=self',\
# #            'http://hf3mjs.qa.webex.com/wbxmjs/joinservice/health?AT=LB&domain=hf3wd',\
# #            'http://hf3mrs.qa.webex.com/wbxmbs/joinservice/health?AT=LB&domain=hf3wd',\
# #            'https://qat32.qa.webex.com/webex/apachepolltom.php?wd=hf3wd&type=self']
#
# # urllist = ['https://qat32.qa.webex.com/webex/apachepolltom.php?wd=hf3wd&type=self']
# #
# # while True:
# #     for url in urllist:
# #         checkurl(url)
#
# # #!/usr/bin/env python
# # import os
# # import socket
# # import json
# # import urllib
# # import urllib2
# #
# # df = '/tmp/df'
# #
# # hostname = socket.gethostname()
# #
# # def SendMsgToSparkRoom(msg=None):
# #     sparkapi = 'https://api.ciscospark.com/v1/messages'
# #     useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
# #     headers = {'Content-Type': 'application/json;charset=UTF-8',
# #                'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
# #     headers['User-Agent'] = useragent
# #     roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
# #     # roomId = '28e3c750-6908-11e6-a747-2b856e15b09b' ##this is CMR Scrum Room
# #     data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
# #     data = json.dumps(data)
# #     # print data
# #
# #     try:
# #         req = urllib2.Request(sparkapi, data=data,headers=headers)
# #         r = urllib2.urlopen(req)
# #
# #         if r.code == 200:
# #             print "send msg successfully"
# #         print r.code
# #
# #     except Exception as e:
# #         print 'send msg failed', e
# #         pass
# #
# # def checkusage(partition,percent):
# #     if int(percent.strip('%')) >= 90:
# #         msg ='[Warning]The disk usage of %s is %s on %s, Please Be Noticed!' % (partition,percent,hostname)
# #         SendMsgToSparkRoom(msg)
# #
# # def getdata():
# #     tmp = os.popen("df -h|awk '{print $4,$5,$6 }'")
# #     with open(df,'w+') as f:
# #         f.write(tmp.read())
# #
# #     with open(df) as f:
# #         for line in f:
# #             if not line.startswith('Avail') and line.strip():
# #                 line_format = line.split()
# #                 print line_format
# #                 if line_format[0].endswith('%'):
# #                     checkusage(line_format[-1],line_format[0])
# #                 else:
# #                     checkusage(line_format[-1],line_format[-2])
# #
# #
# # if __name__ == '__main__':
# #     getdata()
# #
# #
# # from cassandra.cluster import Cluster
# # from cassandra.auth import PlainTextAuthProvider
# # from cassandra import ConsistencyLevel
# # #import threading
# # import multiprocessing
# #
# # success = 0
# # failure = 0
# # def getdatafromcassandra():
# #     global success,failure
# #     cluster = Cluster(['173.37.48.138','173.37.48.139','173.37.48.140'],port=2701,auth_provider=PlainTextAuthProvider(username='test', password='pass'))
# #     session = cluster.connect('ks_j2ee_global')
# #     sql = session.prepare("select siteurl,clusterdns from ks_j2ee_global.wbxsiteurlclusterurlmap where siteurl='atlastestvcdmz111317tr1.mydev'")
# #     sql.consistency_level = ConsistencyLevel.LOCAL_QUORUM
# #     rows = session.execute(sql)
# #     if rows:
# #         print "OKOKOK",success
# #         success += 1
# #     else:
# #         print "NONONO",failure
# #         failure += 1
# #     session.shutdown()
# #     cluster.shutdown()
# #
# # for i in range(1000):
# #     multiprocessing.Process(target=getdatafromcassandra(),args=()).start()
# #
# # print "success:",success,"failure",failure
#
#
#
# #
# # def tag(name,cls=None,*args, **attrs):
# #     "generate one or more html tag"
# #     if cls is not None:
# #         attrs['class'] = cls
# #     if attrs:
# #         attr_str = ''.join(' %s="%s"' % (attr,value)
# #                            for attr,value
# #                            in sorted(attrs.items()))
# #     if 'opt' in attrs:
# #         opt = attrs.get('opt','No')
# #     else:
# #         attr_str = ''
# #     if args:
# #        return '\n'.join('<%s%s>%s</%s>' % (name,attr_str,c,name) for c in args)
# #     else:
# #         return '<%s%s />' % (name,attr_str)
# #
# #
#
# import os
# import requests
# import threading
# import time
#
# class MultithreadDownload(threading.Thread):
#     def __init__(self,url,startpos,endpos,f):
#         threading.Thread.__init__(self)
#         self.url = url
#         self.startpos = startpos
#         self.endpos = endpos
#         self.fd = f
#
#     def download(self):
#         downloadsize = 0
#         print "start thread：%s at %s" % (self.getName(),time.time())
#         #print "start %s,end %s:" % (self.startpos,self.endpos)
#         headers = {"Range":"bytes=%s-%s" % (self.startpos,self.endpos),'Accept-Encoding':'*'}
#         res = requests.get(self.url,headers=headers)
#         self.fd.seek(self.startpos)
#         self.fd.write(res.content)
#         self.fd.flush()
#         downloadsize += os.path.getsize(filename)
#         #print '[%s]%.0f' % ('=' * 20, int(downloadsize// filesize * 100)) + '%'
#         print "stop thread: %s at %s" % (self.getName(),time.time())
#
#     def run(self):
#         self.download()
#
#
# if __name__ == '__main__':
#     url = 'http://51reboot.com/blogimg/pc.jpg'
#     #url = 'http://labova.qa.webex.com/tools/KNOPPIX_V7.0.4CD-2012-08-20-EN.iso'
#     filename = url.split('/')[-1]
#     filesize = int(requests.head(url).headers['Content-Length'])
#     print '%s filesize is %d' % (filename,filesize)
#
#     threadnum = 10
#     threading.BoundedSemaphore(threadnum)
#
#     step = filesize // threadnum
#     print 'step',step
#     mtd_list = []
#     start = 0
#     end = -1
#
#     tempf = open(filename,'w+')
#     tempf.close()
#
#     with open(filename,'rb+') as f:
#         fileno = f.fileno()
#         print "fileno",fileno
#         while end < filesize -1:
#             start = end + 1
#             end = start + step -1
#             if end > filesize:
#                 end = filesize
#             print "start:%s, end:%s" % (start,end)
#             dup = os.dup(fileno)
#             #print 'dup',dup
#             fd = os.fdopen(dup,'rb+',-1)
#             #print 'fd',fd
#
#             t = MultithreadDownload(url,start,end,fd)
#             t.start()
#             #mtd_list.append(MultithreadDownload(url,start,end,fd))
#             #print 'mtd_list',mtd_list
#     for i in mtd_list:
#         i.setDaemon(True)
#         i.start()
#     for i in mtd_list:
#         i.join()
#
#
# # import os
# # import zipfile
# # import logging
# #
# # logging.basicConfig(filename='/Users/yonzhan2/Downloads/logging.txt',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
# # logging.info('test log')
# # logging.debug('debug log')
# # logging.error('error log')
# #
# # file = zipfile.ZipFile('/Users/yonzhan2/Downloads/test.zip','w')
# # for foldername,subfolders,filenames in os.walk('/Users/yonzhan2/Downloads/test/'):
# #     if not foldername.startswith('.'):
# #         print(foldername)
# #         file.write(foldername)
# #
# #     for name in filenames:
# #         if not name.startswith('.'):
# #             print(os.path.join(foldername,name))
# #             file.write(os.path.join(foldername,name))
# # file.close()
#
# #
# # def make_zip(source_dir, output_filename):
# #     zipf = zipfile.ZipFile(output_filename, 'w')
# #     pre_len = len(os.path.dirname(source_dir))
# #     for parent, dirnames, filenames in os.walk(source_dir):
# #         for filename in filenames:
# #             pathfile = os.path.join(parent, filename)
# #             arcname = pathfile[pre_len:].strip(os.path.sep)     #相对路径
# #             print(arcname)
# #             zipf.write(pathfile, arcname)
# #     zipf.close()
# #
# #
# # make_zip('/Users/yonzhan2/Downloads/test','/Users/yonzhan2/Downloads/test.zip')
#
# # import requests,sys
# # import pprint
# # from bs4 import BeautifulSoup
# #
# # import xml.etree.cElementTree as et
# #
# # url = 'http://10.224.90.254/public/wincfg_apptokeninfo.xml'
# #
# # #res = requests.get(url,auth=('wbxsisadmin','password'))
# #
# # #print(pprint.pprint(res.content))
# #
# # # root = et.fromstring(res.content)
# # # print (root.find('apptoken'))
# #
# # res =requests.get('http://google.com/search?q=' + ' '.join('python'))
# # res.raise_for_status()
# # print(res.content)
# #
# # soup = BeautifulSoup(res.content,'html.parser')
# # print(soup.select('.r a'))
# #
# # for i in soup.select('.r a'):
# #     print(i.get('href'))
# #!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
#
#
#
# # import socket
# #
# # print(socket.gethostname())
# # print(socket.gethostbyname("jhf3tc001.qa.webex.com"))
# # #print(type(socket.gethostname()))
# # #socket.gethostbyname(socket.gethostname())
# #
# # #print(socket.gethostbyname_ex(socket.gethostname()))
# # socket.gethostbyaddr('10.224.89.100')
# #
# # def get_host_ip():
# #     try:
# #         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #         s.connect(('8.8.8.8', 80))
# #         ip = s.getsockname()[0]
# #     finally:
# #         s.close()
# #
# #     return ip
# #
# # print(get_host_ip())
# #
# # import requests
# #
# # from requests.packages import urllib3
# # urllib3.dis
# #
# # import re, uuid
# # print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
# #
# # for i in range(1,51):
# #     print("win7-spc8{:0>2}".format(i))
# #
# # import logging
# # import re
# # log = logging.getLogger(__name__)
# # string = "Hello World! hello Eason ! hallo, The little baby."
# # log.debug('regexp test')
# # print(log.name)
# #
# #
# # print(re.match('Hello',string).group())
# #
# # print(re.search('hello',string,re.I).group())
# #
# # print(re.findall('hello',string,re.I))
# #
# # print('=======')
# # print([g.group() for g in re.finditer('hello',string,re.I)])
# #
# # print(re.split("hello",string,maxsplit=3))
# #
# # print(re.sub("hallo","hello",string))
# # s1= "print('hello')"
# # print(s1)
# # eval(s1)
# #
# # try:
# #     ret = re.match('hello',string).group()
# #     print( True)
# # except:
# #     print( False)
# #
# #
# # anyend = ".end"
# # print(re.match(anyend,'bend').group())
# # m = re.match('\w+@(\w+\.)*\w+\.com','nobody@xxx.yyy.zzz.com')
# # if m: print(m.group())
# #
# # m = re.match('(\w\w\w)-(\w\d\d\d)','abc-t123t')
# # if m: print(m.group(2),m.groups())
# #
# #
# # m = re.search('^The','The end.')
# # if m: print(m.group())
# #
# #
# # m = re.search(r'\BThe','BitThe dog.')
# # if m: print(m.group())
# #
# # s = 'This and that.'
# # print(re.findall(r'(th\w+)',s,re.I))
# #
# #
# # print(re.sub('X','Mr. Smith','attn: X\n\nDear X,\n'))
# #
# # print(re.subn('X','Mr. Smith','attn: X\n\nDear X,\n'))
# #
# # print(re.sub('[ae]','X','abcdef'))
# # print(re.subn('[ae]','X','abcdef'))
# #
# # print(re.sub(r'(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})',r'\2/\1/\3','2/20/91'))
# # print(re.sub(r'(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})',r'\2/\1/\3','2/20/1991'))
# # print('-'.join(re.findall('..','aabbcc')))
# #
# # import uuid
# # print('%012x' % uuid.getnode())
# # print(':'.join(re.findall('..', '%012x' % uuid.getnode())))
# #
# # print(re.split(', |(?= (?:\d{5}|[A-Z]{2})) ','Los Ang, CA 90950'))
# #
# # print(re.findall(r'(?i)yes','Yes?yes!YES!!'))
# # print(re.findall(r'yes','Yes?yes!YES!!',re.I))
# #
# # print(re.search('(\w+?)','Yong Zhang').groups())
# # url="https://sqdemo.dmz.webex.com"
# # print(re.search('(?P<sitename>\w+).dmz.webex.com',url).groupdict())
# #
# # ss=  "I  have a dog,  I  have a cat"
# # print(re.findall(r"I  have a (?:dog|cat)",ss))
# #
# # s= '''
# #
# #    sqdemo@dmz.webex.com
# #    sademo@dmz.webex.com
# #    sbdemo@dmz.webex.com.cn
# #    '''
# # print(re.findall('sqdemo.+',s))
# # print(re.findall((r'(?m)^\s+(?!sademo)(\w+)'),s))
# # print(re.findall((r'(?m)^\s+(?=sademo)(\w+)'),s))
# # print(re.findall((r'(?m)^\s+(?<=com)'),s))
# #
# #
# #
# # import socket
# # s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# # s.connect(("8.8.8.8",80))
# # print(s.getsockname()[0])
# #
# # print(socket.gethostbyname('jhf3tc001.qa.webex.com'))
# #
# # import requests,json
# #
# # headers={"Jenkins-Crumb": "19ea266a31e27d99328d0612c397deed"}
# # data = {"parameter": [{"name": "release_version", "value": "32.10.0"}, {"name": "feature_num", "value": "5672"}, {"name": "client_buildnum", "value": ""}]}
# # #data= json.loads(formdata)
# #
# # r = requests.post(url='http://admin:pass@10.224.38.201:8080/job/deployclient4f7865/buildWithParameters',headers=headers,data=data)
# # #r = requests.post(url='http://admin:pass@10.224.38.201:8080/job/GetVersionList4ATS/build?delay=0sec',headers=headers)
# # print(r.content)
# #
#
# #!/usr/bin/env python
# """
# Written by Chris Hupman
# Github: https://github.com/chupman/
# Example: Get guest info with folder and host placement
#
# """
# from __future__ import print_function
#
# from pyVmomi import vim, vmodl
#
# from pyVim.connect import SmartConnectNoSSL, Disconnect
#
# import argparse
# import atexit
# import getpass
# import json
# import csv
#
# #import openpyxl
# import pymysql
# #from collections import defaultdict
#
#
# def GetArgs():
#     """
#     Supports the command-line arguments listed below.
#     """
#     parser = argparse.ArgumentParser(
#         description='Process args for retrieving all the Virtual Machines')
#     parser.add_argument('-s', '--host', required=True, action='store',
#                         help='Remote host to connect to')
#     parser.add_argument('-o', '--port', type=int, default=443, action='store',
#                         help='Port to connect on')
#     parser.add_argument('-u', '--user', required=True, action='store',
#                         help='User name to use when connecting to host')
#     parser.add_argument('-p', '--password', required=False, action='store',
#                         help='Password to use when connecting to host')
#     parser.add_argument('--json', required=False, action='store_true',
#                         help='Write out to json file')
#     parser.add_argument('--jsonfile', required=False, action='store',
#                         default='getvmsbycluster.json',
#                         help='Filename and path of json file')
#     parser.add_argument('--silent', required=False, action='store_true',
#                         help='supress output to screen')
#     args = parser.parse_args()
#     return args
#
#
#
# def vmsummary(vm):
#     ip = vm.summary.guest.ipAddress
#     vmstat = vm.summary.runtime.powerState
#     vmpath = vm.summary.config.vmPathName
#     vmmacc = 'N/A'
#     try:
#         if hasattr(vm.config,'hardware'):
#             for dev in vm.config.hardware.device:
#                 if hasattr(dev,'macAddress'):
#                     vmmacc = dev.macAddress
#                 continue
#             return ip,vmmacc,vmstat,vmpath
#         else:
#             return 'N/A','N/A','N/A','N/A'
#
#     except Exception as e:
#         print(vm.summary.config.name,vmpath,e)
#
#
# class DBOperation:
#     def __init__(self,host,port,user,passwd,db):
#         self.host = host
#         self.port = port
#         self.user = user
#         self.passwd = passwd
#         self.db = db
#         try:
#             self.database = pymysql.connect(self.host, self.user, self.passwd, self.db)
#         except Exception as e:
#             print(e)
#         self.cursor = self.database.cursor()
#
#
#     def update(self,vmip,vmname,vmmacc):
#         sql = "UPDATE vminfo set ipaddr = %s where vmname = %s and vmmacc = %s ",(vmip,vmname,vmmacc)
#         try:
#             self.cursor.execute(*sql)
#             print('update successfully for',vmname)
#             self.database.commit()
#         except Exception as e:
#             print('update',e)
#
#     def disconnect(self):
#         self.database.close()
#
#
# def main():
#     """
#     Iterate through all datacenters and list VM info.
#     """
#     count = 0
#     #db = DBOperation('172.24.66.158','3306','test','pass','vmdb')
#     args = GetArgs()
#     outputjson = True if args.json else False
#
#     if args.password:
#         password = args.password
#     else:
#         password = getpass.getpass(prompt='Enter password for host %s and '
#                                    'user %s: ' % (args.host, args.user))
#
#     si = SmartConnectNoSSL(host=args.host,
#                            user=args.user,
#                            pwd=password,
#                            port=int(args.port))
#     if not si:
#         print("Could not connect to the specified host using specified "
#               "username and password")
#         return -1
#
#     atexit.register(Disconnect, si)
#
#     content = si.RetrieveContent()
#     children = content.rootFolder.childEntity
#     for child in children:  # Iterate though DataCenters
#         dc = child
#         print("DC Name: %s" % dc.name) ##qawbx11
#         clusters = dc.hostFolder.childEntity
#         for cluster in clusters:  # Iterate through the clusters in the DC
#             if hasattr(cluster,'host'):
#                 hosts = cluster.host # Variable to make pep8 compliance
#             else:
#                  continue
#             for host in hosts:  # Iterate through Hosts in the Cluster
#                 hostname = host.summary.config.name
#                 vms = host.vm
#                 #tasks = [vm.PowerOn() for vm in vms if vm.summary.runtime.powerState == 'PoweredOff']
#                 #WaitForTasks(tasks, si)
#                 for vm in vms:  # Iterate through each VM on the host
#                     #print('dir vm',dir(vm))
#                     vmname = vm.summary.config.name
#                     summary = vmsummary(vm)
#                     nic = vm.device.VirtualDeviceSpec()
#                     #print(summary[0],summary[1],summary[2],summary[3])
#                     vmip,vmmacc,vmstat,vmpath = summary
#                     vminfo = vmip,vmname,vmmacc
#                     print(vminfo)
#                     print(nic)
#                     db.update(*vminfo)
#     db.disconnect
#
# # Start program
# if __name__ == "__main__":
#     main()
#
import requests
# from novaclient import client
# from novaclient import base
# #print(help(client))
# nova = client.Client('2.0', 'cmadmin', 'cbdd746eb3a1d3f727de31e52f4573cf', 'd1cfe8499fd54ad187c96bea6b5f900d', 'https://ci92hf02int-keystone-srv.cisco.com:443/v2.0')
# #print(help(nova))
# print(dir(nova))
# print(nova.neutron)
# print(nova.glance.list())
# print(nova.servers.list())
# print(nova.flavors.list())
# print(nova.api_version)
# print(nova.networks.list())
# #nets = base.getid()
# #print(nets)
# my_image = [img for img in nova.glance.list() if img.name == 'CentOS72-x86_64-baseimage-ocp'][0]
#
# my_flavor = [flavor for flavor in nova.flavors.list() if flavor.name == '2vcpu-4gmem-72ghd'][0]
# print(my_image,my_flavor)
# server = nova.servers.create('pf1test001',my_image,my_flavor,nics=[{'net-id':'f848d24d-fa4d-455e-bf3a-1fa6cf9d533f','v4-fixed-ip':'10.224.82.240'}])
# print(server.id)
#
# import paramiko
# import logging
# import re
# import threading
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# cmd = '''sudo umount /mnt;sudo mount 172.24.88.80:/u01 /mnt; sudo /mnt/get_oracle_info.sh;sudo umount /mnt'''
# #cmd = '''umount /mnt;bash -c "/bin/echo nameserver 10.224.91.8 >/etc/resolv.conf";mount 10.224.95.242:/COLD /mnt; sh /mnt/get_oracle_info.sh;umount /mnt'''
# logging.basicConfig(filename='scan.log',format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
#
# def scanServer(segment):
#     for num in range(70, 71):
#         server =  segment + '.' + str(num)
#         for user, pwd in zip(['wbxroot','wbxbuilds','wbxbuilds','dosun','shuqli'], ['wbx@AaR00t','P0w3rSupply!','Ch4ll3ng3M3!','W0rk4life','Work4life']):
#             print server,user, pwd
#             try:
#                 ssh.connect(server, username=user, password=pwd, timeout=2)
#                 stdin, stdout, stderr = ssh.exec_command(cmd)
#                 print stdout.read()
#                 #print re.search("success",stdout.read()).group()
#                 if "success" == re.search("success",stdout.read()).group():
#                     logging.info('Success on {0}'.format(server))
#                 break
#             except Exception as e:
#                 #print e
#                 logging.error('Failure on {0} {1}'.format(server,e))
#
# ip_prefix = "10.194."
# threads = []
# for seg in range(246,247):
#     segment = ip_prefix + str(seg)
#     t = threading.Thread(target=scanServer,args=(segment,))
#     threads.append(t)
#     t.start()


import os

versionlist = set()
deldict = dict()
# def splitversion(dir):
#     res = dir.split('-')
#
#     #version,buildnum=res[1],res[2]
#     version= res[1]
#     print(version)
#     versionlist.add(version)
#     print(versionlist)
#
# splitversion('WBXclient-32.15.0-25')
# splitversion('WBXclient-33.15.0-25')
# splitversion('WBXclient-32.15.0-26')
#

# !/usr/bin/env python
# import glob
# import os
#
# version = glob.glob('/www/htdocs/client/WBXclient-*')
# versionlist=set()
# [versionlist.add(ver.split('/')[-1].split('-')[1]) for ver in version]
# print(versionlist)
#
# for ver in versionlist:
#     tmp = sorted(glob.glob('/www/htdocs/client/WBXclient-'+ver+'-*'))
#     removelist = tmp[:len(tmp)-3]
#     if len(removelist) > 0:
#         for rem in removelist:
#             print("Removing client " + rem + " ...")
#             os.system("rm -rf " + rem)

# from retry import retry
#
# import requests
# import uuid
#
# url = "https://videos.datacamp.com/transcoded_mp4/2533_driven_data_ML/v2/ch4_3.mp41"
# filename=url.split('/')[-1]
# print(filename)
#
# @retry(tries=3,exceptions=Exception)
# def getmp4(url):
#     req=requests.get(url)
#     with open(filename,'wb') as video:
#         for chunk in req.iter_content(chunk_size=1024):
#             if chunk:
#                 video.write(chunk)
#                 video.flush()
#     print("DEPLOY_" + str(uuid.uuid4()))
#
# getmp4(url)

import threading
import time

import requests

cmcurl = "csgcmc.qa.webex.com"

###QA CMC headers
headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

current_dir = os.path.dirname(__file__)


def deploywithplaybook(component, poolname, service_version, build_no=0100):
    playbook = '''component: %s

variables:
  pool: %s
  version: %s-%s

tasks:

- name: "register box in {{pool}}"
  action: RegisterBox
  pool: "{{pool}}"
  versionBuild: "{{version}}"
  boxList:
  - name: mhf9mcs12b
    ip: 10.224.23.55
    boxType: mmpmcs
  - name: mhf9mcs12c
    ip: 10.224.23.56
    boxType: mmpmcs
  - name: mhf9mcs12d
    ip: 10.224.23.57
    boxType: mmpmcs
  - name: mhf9mcs12e
    ip: 10.224.23.58
    boxType: mmpmcs
  - name: mhf9mcs12f
    ip: 10.224.23.59
    boxType: mmpmcs    
    ''' % (component, poolname, service_version, build_no)

    url = "https://%s/cmc/api/playbook/" % cmcurl
    filename = os.path.join(current_dir, 'mmpplaybook_%s.yml' % poolname)
    with open(filename, 'w+') as f:
        f.write(playbook)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    # os.remove(filename)
    print req.text


if __name__ == "__main__":
    deploywithplaybook('mmp', 'mhf9', '5.4.0', '0000')
