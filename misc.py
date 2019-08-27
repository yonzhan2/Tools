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
# import requests,json
#
# headers={"Jenkins-Crumb": "19ea266a31e27d99328d0612c397deed"}
# data = {"parameter": [{"name": "release_version", "value": "39.6.0"}, {"name": "feature_num", "value": "10863"}, {"name": "client_buildnum", "value": ""}]}
# #data= json.loads(formdata)
#
# r = requests.post(url='http://admin:pass@10.224.38.201:8080/job/deployclient4f10863/buildWithParameters',headers=headers,data=data)
# #r = requests.post(url='http://admin:pass@10.224.38.201:8080/job/GetVersionList4ATS/build?delay=0sec',headers=headers)
# print(r.content)
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
import asyncio

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
from pprint import pprint
# import requests
#
# # cmcurl = "csgcmc.qa.webex.com"
# cmcurl = "sjcmc.eng.webex.com"
#
# ###QA CMC headers
# # headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}
#
# ###SJ CMC headers
# headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}
#
# current_dir = os.path.dirname(__file__)
#
#
# def getIP(component, pool):
#     url = 'https://%s/cmc/api/sitBoxList/%s/?pool=%s&ignore_owner=yes' % (cmcurl, component, pool)
#     req = requests.get(url, headers=headers)
#     res = req.json()
#     rows = res.get("rows")
#     # print(res)
#     for row in rows:
#         yield row["ip"]
#
#
# if __name__ == "__main__":
#     for ip in getIP("j2ee","jsq1"):
#         print ip

# def fun():
#     l = []
#     for i in range(20):
#         yield i
#
# if __name__ == '__main__':
#     for x in fun():
#         print(x)

# def fun():
#     for i in range(20):
#         x=yield i
#         print('good',x)
#
# if __name__ == '__main__':
#     a=fun()
#     for i in range(30):
#         x=a.next()
#         print("x=",x)
# import types
# def fab(max):
#     n,a,b = 0,0,1
#     while n < max:
#         yield b
#         a , b = b, a + b
#         n = n + 1
#
# for n in fab(5):
#     print n,
#
# def read_file(fpath):
#    BLOCK_SIZE = 1024
#    with open(fpath, 'rb') as f:
#        while True:
#            block = f.read(BLOCK_SIZE)
#            if block:
#                print block
#            else:
#                return
#
#
# read_file('getversion.py')
# for i in read_file('getversion.py'):
#     print i,
#     import  time
#     time.sleep(3)
#
# from retrying import retry
# url ="http://10.224.89.58:1801/webex/apachepolltom.php?wd=hf2wd&type=self1"
#
# @retry(stop_max_attempt_number=3,wait_fixed=200)
# def getdata(url):
#     try:
#         req = requests.get(url)
#         ret = req.content
#         print ret
#     except Exception as e:
#         assert False, e
#
#     return True
#
# print getdata(url)
# from pprint import pprint
# from yaml import load
#
# data = load(open('cmcplaybook/install_msi.yml'))
# pprint(data)
#
#
# import re
# #s="Name : WBXmcc Relocations: /opt/webex/mmp Version : 6.0.0 Vendor: (none) Release : 5485 Build Date: Sat 22 Mar 2019 12:58:05 AM GMT Install Date: Fri 22 Mar 2019 04:33:56 AM GMT Build Host: ed124cc06738 Group : Applications/Communications Source RPM: WBXmcc-6.0.0-5485.src.rpm Size : 36676218 License: Cisco Software License 1.0 Signature : RSA/SHA1, Fri 22 Mar 2019 01:27:30 AM GMT, Key ID 952e62c3230c0099 URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: date=Thu Mar 21 17:58:04 PDT 2019 hostname=ed124cc06738 HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_WebEx_Servers_main_webex-mmp_i386_CentOS6_9_32_2991482_201903211745/webex-mmp/config/rpm/WBXmcc pwd=/cctg/workingDirectory/official_WebEx_Servers_main_webex-mmp_i386_CentOS6_9_32_2991482_201903211745/webex-mmp/build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)"
# #s="Name : WBXmcc Version : 6.0.0 Release : 5431 Architecture: x86_64 Install Date: Thu 21 Mar 2019 10:47:11 AM GMT Group : Applications/Communications Size : 53857756 License : Cisco Software License 1.0 Signature : RSA/SHA1, Mon 18 Mar 2019 03:36:30 AM GMT, Key ID 952e62c3230c0099 Source RPM : WBXmcc-6.0.0-5431.src.rpm Build Date : Mon 18 Mar 2019 02:51:01 AM GMT Build Host : ed5f9f5122c9 Relocations : /opt/webex/mmp URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: date=Sun Mar 17 19:51:01 PDT 2019 hostname=ed5f9f5122c9 HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_WebEx_Servers_main_webex-mmp_x86_64_CentOS7_2981326_201903171936/webex-mmp/config/rpm/WBXmcc pwd=/cctg/workingDirectory/official_WebEx_Servers_main_webex-mmp_x86_64_CentOS7_2981326_201903171936/webex-mmp/build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)"
# #s='''WBXappdb.T33 Relocations: /opt/webex/package/WBXappdb.T33-39.3.0 Version : 39.3.0 Vendor: (none) Release : 50 Build Date: Wed 27 Mar 2019 03:46:24 AM GMT Install Date: Thu 28 Mar 2019 04:21:27 AM GMT Build Host: cctg-ci-lnx227.cisco.com Group : Applications/Communications Source RPM: WBXappdb.T33-39.3.0-50.src.rpm Size : 80662 License: Cisco Software License 1.0 Signature : (none) URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: date=Tue Mar 26 20:46:23 PDT 2019 hostname=cctg-ci-lnx227.cisco.com HOME=/home/ccatgbld FROM=/spare/workspace/official_Train_Appdb_main_webex-db-application-patch_3002767_201903262045/webex-db-application-patch/T39.3 pwd=/spare/workspace/official_Train_Appdb_main_webex-db-application-patch_3002767_201903262045/webex-db-application-patch/build uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)'''
# s=''' Name : WBXpagecommon Relocations: /opt/webex/package/WBXpagecommon Version : 39.3.0 Vendor: (none) Release : 127 Build Date: Wed Mar 27 23:54:17 2019 Install Date: Thu Mar 28 04:32:29 2019 Build Host: 3e206370d9d9 Group : Applications/Communications Source RPM: WBXpagecommon-39.3.0-127.src.rpm Size : 81997934 License: Cisco Software License 1.0 Signature : RSA/SHA1, Wed Mar 27 23:55:07 2019, Key ID 952e62c3230c0099 URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: JAVA_HOME=/cctg/artcache/Java/openjdk_x64/1.8.0.121 date=Wed Mar 27 16:54:16 PDT 2019 hostname=3e206370d9d9 HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_Train_Web_39.3.0_pagecommon_3004780_201903271640/webex-web-applications-build/build/linux/../../../STAGING/Deliverable pwd=/cctg/workingDirectory/official_Train_Web_39.3.0_pagecommon_3004780_201903271640/webex-web-applications-build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)
# Name : WBXpage.T32L Relocations: /opt/webex/package/WBXpage.T32L Version : 32.25.0 Vendor: (none) Release : 57 Build Date: Wed Mar 27 16:29:44 2019 Install Date: Wed Mar 27 23:43:59 2019 Build Host: a8528d927bc9 Group : Applications/Communications Source RPM: WBXpage.T32L-32.25.0-57.src.rpm Size : 255474701 License: Cisco Software License 1.0 Signature : RSA/SHA1, Wed Mar 27 16:33:49 2019, Key ID 952e62c3230c0099 URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: JAVA_HOME=/cctg/artcache/Java/openjdk_x64/1.8.0.121 date=Wed Mar 27 09:29:42 PDT 2019 hostname=a8528d927bc9 HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_Train_Web_32.25.0.oneversion_T32L_page_3004253_201903270900/webex-web-applications-build/build/linux/../../../STAGING/Deliverable pwd=/cctg/workingDirectory/official_Train_Web_32.25.0.oneversion_T32L_page_3004253_201903270900/webex-web-applications-build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)
# Name : WBXadmin Relocations: /opt/webex/package/WBXadmin Version : 6.3.0 Vendor: (none) Release : 181 Build Date: Wed Mar 27 23:48:14 2019 Install Date: Thu Mar 28 04:31:40 2019 Build Host: bcffab781475 Group : Applications/Communications Source RPM: WBXadmin-6.3.0-181.src.rpm Size : 75725545 License: Cisco Software License 1.0 Signature : RSA/SHA1, Wed Mar 27 23:49:27 2019, Key ID 952e62c3230c0099 URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: date=Wed Mar 27 16:48:13 PDT 2019 hostname=bcffab781475 HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_WebEx_WebServices_main_webex-web-wbxadmin_3004782_201903271640/webex-web-wbxadmin/build/../../webex-web-wbxadmin/STAGING/Deliverable pwd=/cctg/workingDirectory/official_WebEx_WebServices_main_webex-web-wbxadmin_3004782_201903271640/webex-web-wbxadmin/build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)
# Name : WBXpage.T33L Relocations: /opt/webex/package/WBXpage.T33L Version : 39.3.0 Vendor: (none) Release : 256 Build Date: Thu Mar 28 00:06:11 2019 Install Date: Thu Mar 28 04:34:32 2019 Build Host: 25d34aafb3fc Group : Applications/Communications Source RPM: WBXpage.T33L-39.3.0-256.src.rpm Size : 255476350 License: Cisco Software License 1.0 Signature : RSA/SHA1, Thu Mar 28 00:11:23 2019, Key ID 952e62c3230c0099 URL : http://www.cisco.com/ Summary : rpmgen-generated image Description : Packaging information: JAVA_HOME=/cctg/artcache/Java/openjdk_x64/1.8.0.121 date=Wed Mar 27 17:06:09 PDT 2019 hostname=25d34aafb3fc HOME=/home/ccatgbld FROM=/cctg/workingDirectory/official_Train_Web_39.3.0_page_3004779_201903271640/webex-web-applications-build/build/linux/../../../STAGING/Deliverable pwd=/cctg/workingDirectory/official_Train_Web_39.3.0_page_3004779_201903271640/webex-web-applications-build/rpm uid=50293(ccatgbld) gid=50293(ccatgbld) groups=50293(ccatgbld)'''
# p2 = re.compile(r"Install Date: (\w \w)\s") #\d+ \d+\:\d+\:\d+ \d{4}
# p3 = re.compile(r"Build Date[ ]{0,1}: (.*? \d+)\s")
#
# #print(re.findall("Name : (.*?)\s",s))
#
# package = re.findall("Name : (.*?)\s",s)
# release = re.findall("Version : (.*?)\s",s)
# version = re.findall("Release : (.*?)\s",s)
#
#
#
# p1 = list(zip(package,release,version))
# print(list((package[p],release[p],version[p]) for p in range(len(package))))
# #print(re.findall(p1,s))
#
# print("p2,p3:", re.findall(p2, s), re.findall(p3, s))
# buildsinfo = ['{0}-{1}-{2}'.format(build[0].strip(), build[1].strip(), build[2].strip()) for build in p1]
#
# print(list(zip(buildsinfo, re.findall(p2, s), re.findall(p3, s))))
#
# from concurrent.futures import ThreadPoolExecutor
# import requests
# def fetch_url(url):
#     u = requests.get(url)
#     data = u.content
#     return data
# pool = ThreadPoolExecutor(10)
# # Submit work to the pool
# a = pool.submit(fetch_url, 'https://www.baidu.com/')
# b = pool.submit(fetch_url, 'https://sqdemo.dmz.webex.com')
# # Get the results back
# x = a.result()
# y = b.result()
# print(x)
# print(y)


# from IPy import IP
#
# netmask = "255.255.224.0"
# gateway = "10.224.56.1"
# ip = IP('10.224.56.0/23')
# vlanid = 50
# print("IP\t NetMask\t GateWay\t VlanId")
# for i in ip:
#     print(i, netmask, gateway, vlanid)
#
#
# class ManipulateDataToMongo(object):
#     def __init__(self):
#         self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(MONGODB))
#         self.mydb = self.client["build"]
#         self.mycoll = self.mydb["buildinfo"]
#
#     def querydata(self, ipaddr):
#
#         try:
#             myquery = {"ipaddr": ipaddr}
#             ret = self.mycoll.find_one(myquery)
#             if ret:
#                 return True
#             return
#         except Exception as e:
#             print(("Error %d: %s" % (e.args[0], e.args[1])))
#
#     def insertdata(self, env, type, build, hostname, ipaddr):
#
#         try:
#             mydict = {"env": env, "type": type, "build": build, "hostname": hostname, "ipaddr": ipaddr,
#                       "createtime": getCurrentTime()}
#             if build and ipaddr:
#                 self.mycoll.insert_one(mydict)
#             print(("inserted done for %s" % hostname))
#         except Exception as e:
#             print(("Error %d: %s" % (e.args[0], e.args[1])))
#
#     def updatedata(self, env, type, build, hostname, ipaddr):
#
#         try:
#             myquery = {"ipaddr": ipaddr}
#             newvalues = {"$set": {"env": env, "type": type, "build": build, "hostname": hostname}}
#             self.mycoll.update_one(myquery, newvalues)
#             print(("updated build info done for %s" % ipaddr))
#         except Exception as e:
#             print(("Error %d: %s" % (e.args[0], e.args[1])))

#
# class Car():
#     def __init__(self, make, model, year):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.__odemeter_reading = 0
#
#     def get_car_description(self):
#         long_name = str(self.year) + ' ' + self.make + ' ' + self.model
#         return long_name.title()
#
#     def get_odemeter(self):
#         print("This car has " + str(self.__odemeter_reading) + " miles on it.")
#
#     def update_odemeter(self, mileage):
#         if mileage >= self.__odemeter_reading:
#             self.__odemeter_reading = mileage
#         else:
#             print("Rollback odemeter is not allowed!")
#
#     def increate_odemeter(self, miles):
#         self.__odemeter_reading += miles
#
#     def fill_gas_tank(self):
#         print("Filling Gas to Car")
#
#
# class TypeMismatchError(Exception):
#     pass
#
#
# class Battery():
#     def __init__(self, battery_size=70):
#         self.battery_size = battery_size
#
#     def describle_battery(self):
#         print("The Electric Car has " + str(self.battery_size) + '-kWh battery')
#
#     def set_battery(self, size):
#         if isinstance(size, int):
#             self.battery_size = size
#         else:
#             raise TypeMismatchError
#
#     def get_range(self):
#         if self.battery_size == 70:
#             range = 240
#         if self.battery_size == 85:
#             range = 250
#         msg = "This car can go approximately " + str(range) + " miles on a full charge."
#         print(msg)
#
#
# class ElectricCar(Car):
#     def __init__(self, make, model, year):
#         super().__init__(make, model, year)
#         self.battery = Battery()
#
#     #
#     # def describle_battery(self):
#     #     print("The Electric Car has " + str(self.battery.battery_size) + '-kWh battery')
#
#     def fill_gas_tank(self):
#         print("This Car doesn't need a gas tank!")
#
#
# ecar = ElectricCar('tesla', 'o4', 2018)
# ecar.get_odemeter()
# ecar.battery.describle_battery()
# ecar.fill_gas_tank()
# ecar.battery.describle_battery()
# # ecar.battery.set_battery(85)
# ecar.battery.describle_battery()
# ecar.battery.get_range()
#
# if hasattr(ecar,'year'):
#     print(True)
#     setattr(ecar,'year','2020')
#     print(getattr(ecar,'year'))

# car = Car('audi', 'a8', 2016)
# print(car.get_car_description())
# car.get_odemeter()
# car._Car__odemeter_reading = 50
# car.get_odemeter()
# car.update_odemeter(100)
# car.get_odemeter()
# print(car._Car__odemeter_reading )
# car.update_odemeter(10)
# print(car._Car__odemeter_reading )
# car.increate_odemeter(10)
# car.get_odemeter()
# print(car._Car__odemeter_reading )


import requests, json
from bs4 import BeautifulSoup as bs4
import pprint

#
# headers={"Jenkins-Crumb": "19ea266a31e27d99328d0612c397deed"}
# data = {"parameter": [{"name": "release_version", "value": "39.6.0"}, {"name": "feature_num", "value": "10863"}, {"name": "client_buildnum", "value": ""}]}
# #data= json.loads(formdata)
#
# r = requests.post(url='http://10.224.38.201:8080/job/deployclient4f10863/buildWithParameters',headers=headers,data=data,auth=('admin','pass'))
# print(r.headers.get("Location"))
# if r.status_code == 201:
#     print("Success")
# else:
#     print("Fail")
#
#
#
# import re
#
# username = 'admin'
# password = 'pass'
# auth = requests.auth.HTTPBasicAuth(username, password)
#
# parameter_pattern = re.compile('<input name="name" type="hidden" value="(.*?)"/>')
# value_pattern = re.compile('<input class="setting-input" name="value" type="text" value="(.*?)"/>')
#
# url = "http://10.224.38.201:8080/job/deployclient4f10150/build?delay=0sec"
# # url = "http://10.224.38.201:8080/job/deploypage4train/build?delay=0sec"
#
# "Get release_version parameter"
# clientid = 200
# try:
#     r = requests.get(url, timeout=5, auth=auth)
#     soup = bs4(r.content, 'html.parser')
#     name_value = soup.select('div input[name="name"]')
#     input_value = soup.select('div input[name="value"]')  # soup.find_all(type="text")
#     name_value = str(name_value)
#     input_value = str(input_value)
#     # print(name_value)
#     # print(input_value)
#     parameters = parameter_pattern.findall(name_value)
#     values = value_pattern.findall(input_value)
#     pvmap = zip(parameters, values)
#     params_format = [{"name": p[0], "value": p[1]} for p in list(pvmap)]
#     print(params_format)
#     if clientid:
#         params_format[2]["value"] = str(clientid)
#     client_data = {"parameter": params_format}
#
#     print("params_format is ", json.dumps(client_data))
#
#     print('TEst'.lower())
# except Exception as e:
#     print("Get paramter failed due to {}".format(e))
#
# str = 'failover';
# print(str.startswith("upgrade|fail|maintain"))
#
# from pprint import pprint
#
# CMCURL_MAPPING = {"QA": {"URL": "csgcmc.qa.webex.com",
#                          "KEY": "Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4="},
#                   "DMZ": {"URL": "sjcmc.dmz.webex.com",
#                           "KEY": "Q01DQVBJX0RNWjo5M2IyOGNiNzQ4NjM0YmJmYTI4YWZkNWVhODQ2NGY3Mg=="}}
# cmcurl = CMCURL_MAPPING.get('QA').get("URL")
# key = CMCURL_MAPPING.get('QA').get("KEY")
# headers = dict(Authorization=f"Basic {key}")
#
#
# def getserverbypool(component, pool):
#     # pool, filtertype = self.getpoolinfo()
#     box_url = 'https://%s/cmc/api/sitBoxList/%s/?pool=%s&ignore_owner=yes' % (cmcurl, component, pool)
#     req = requests.get(box_url, headers=headers)
#     ret = req.json().get('rows')
#     servers = [(server.get('id'), server.get('name')) for server in ret]
#     pprint(servers)
#
#
# # getserverbypool('j2ee','jhf3')
#
# def getmbs():
#     url = "https://train.qa.webex.com/webappng/healthcheck"
#     req = requests.get(url, headers=headers)
#     print(json.loads(req.content))
#     mbsver = 'WBXmbs2-' + json.loads(req.content).get("mbs").get("version")
#     print(mbsver)
#
#
# # getmbs()
#
# async def stop(msg, time):
#     await asyncio.sleep(time)
#     print("stop" + msg)


#
# class ThreeTwoOne:
#     async def begin(self):
#         begin=time.time()
#         print(3)
#
#         await stop('cc',5)
#         print(2)
#         await stop('as',3)
#         print(1)
#         await stop('ts',1)
#         end = time.time()
#         print("time is ", end - begin)
#         return
#
# async def game():
#     t = ThreeTwoOne()
#     await t.begin()
#     print('start')

# def main():
#     import asyncio
#     loop = asyncio.get_event_loop()
#     tasks = [stop('cc', 60), stop('as', 30), stop('ts', 20)]
#     begin = time.time()
#     res = loop.run_until_complete(asyncio.wait(tasks))
#     end = time.time()
#     loop.close()
#     time.sleep(0)
#     print("time is ", end - begin)
#
#
# #main()
#
# def foo(bar, baz):
#   print('hello {0}'.format(bar))
#   time.sleep(5)
#   return 'foo' + baz
#
# def foo1(bar, baz):
#   print('hello1 {0}'.format(bar))
#   time.sleep(3)
#   return 'foo1' + baz
#
# from multiprocessing.pool import ThreadPool
# #pool = ThreadPool(processes=1)
#
# from multiprocessing import Pool,cpu_count
# pool = Pool(cpu_count())

# begin=time.time()
# async_result = pool.apply_async(foo, ('world', 'foo')) # tuple of args for foo
# async_result1 = pool.apply_async(foo1, ('world', 'foo')) # tuple of args for foo
# do some other stuff in the main process

# return_val = async_result.get()
# return_val1 = async_result1.get()
# end=time.time()
# col_time=end-begin
# print(return_val)
# print(return_val1)
# print("Col_time:" ,col_time)
#
# str = 'j2ee in qa with pool=t02fa'
# str1 = 'j2ee in qa with pool=t02fa server like as001'
# ret1 = cmc_pattern_with_server.findall(str1)
# print(ret1)
# ret = cmc_pattern_without_server.findall(str)
# print(ret)

# post_data = extract_message("refresh", post_data.text).strip()
# post_data = 'j2ee in qa with pool=t02fa server like as001' ##[('j2ee', 'qa', 't02fa', 'as001')]
# post_data = 'j2ee in qa with pool=t02fa version=5.6.0-0100'   ##[('j2ee', 'qa', 't02fa', '5.6.0-0100')]
# post_data = 'j2ee in qa with pool=t02fa'  ##[('j2ee', 'qa', 't02fa')]
# cmc_pattern_with_version = re.compile("(.*)\s* in\s* (dmz|qa|eng)\s* with\s* pool=(.*)\s* version=(.*)\s*", re.I)
# cmc_pattern_with_server = re.compile("(.*)\s* in\s* (dmz|qa|eng)\s* with\s* pool=(.*)\s* server\s* like\s* (.*)", re.I)
# cmc_pattern_without_server = re.compile("(.*)\s* in\s* (dmz|qa|eng)\s* with\s* pool=(.*)\s*", re.I)
# box=None
# version=None
#
# try:
#     if "server" in post_data:
#         p_result = cmc_pattern_with_server.findall(post_data)
#         print(p_result)
#         service, env, pool, box = p_result[0]
#     elif "version" in post_data:
#         p_result = cmc_pattern_with_version.findall(post_data)
#         print(p_result)
#         service, env, pool, version = p_result[0]
#     else:
#         p_result = cmc_pattern_without_server.findall(post_data)
#         print(p_result)
#         service, env, pool= p_result[0]
#
#     #sys.stderr.write("p_result is {}".format(p_result))
#
#     service = service.strip()
#     env = env.strip()
#     pool = pool.strip()
#     if box:
#         box = box.strip()
#     if version:
#         version = version.strip()
# except Exception as e:
#     pass
#     return "`- refresh (component_name) in (dmz|qa|eng) with pool=<pool_name> [version=<cmc version>][server like <server as reg>]`"

# print(service)
# print(env)
# print(pool)
# print(version)
# print(box)

#
# import jenkins
# from pprint import pprint
#
# server = jenkins.Jenkins('http://10.224.38.201:8080', username='admin', password='pass')
# user = server.get_whoami()
# version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))
# print(server.jobs_count())
#
# jobs = server.get_jobs()
# #pprint(jobs)
# project='deployclient4f10150'
# #server.build_job(project, {'release_version': '39.7.0', 'client_buildnum': ''})
# #time.sleep(10)
# current_job_info = server.get_job_info(project)
# last_build_number = server.get_job_info(project)['lastBuild']['number']
# last_completed_build = server.get_job_info(project)['lastCompletedBuild']['number']
# try:
#     last_failed_build = server.get_job_info(project)['lastFailedBuild']['number']
# except Exception as e:
#     last_failed_build = None
# last_build_url = server.get_job_info(project)['lastBuild']['url']
# pprint(f"last_build_number is {last_build_number}")
# pprint(f"last_build_url is {last_build_url}")
# pprint(current_job_info)
# pprint(f"last_completed_build is {last_completed_build}")
# pprint(f"last_failed_build is {last_failed_build}")
# #
# #print(build_info)
# feature_num='thinclient'
# def get_result(build_number):
#     while True:
#         last_completed_build_number = server.get_job_info(project)['lastCompletedBuild']['number']
#         last_failed_build = server.get_job_info(project)['lastFailedBuild']['number']
#         print(f"Last completed build is {last_completed_build_number}, failed build is {last_failed_build}.")
#         if last_failed_build == build_number:
#             return False
#         if last_completed_build_number != build_number:
#             print("Sleep 10s")
#             time.sleep(10)
#             get_result(build_number)
#         else:
#             return True
#
#
# if get_result(last_build_number):
#     print( f"upgraded job for {feature_num} success.")
# else:
#     print( f"upgraded job for {feature_num} failed.")

from datetime import datetime
from bs4 import BeautifulSoup as bs4
from pprint import pprint

xml = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<title>me01sqvce101 - Zones</title><meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<link rel="stylesheet" type="text/css" href="/inc/allstyles.css?etag=68270-1537279821" />
<script type="text/javascript" src="/inc/thirdpartyscripts.js?etag=475041-1537279821"></script>
<script type="text/javascript" src="/inc/allscripts.js?etag=112617-1537279821"></script>
<style type="text/css">
</style>
<script type="text/javascript">//<![CDATA[
var table_sorter;function initSorter(){table_sorter = new TableTools("zones_table_table");table_sorter.setDefaultSortColumn( 'Name', true );table_sorter.setSortByType('Name' , 'presort');table_sorter.addtopresort('Name','DefaultZone'  );table_sorter.init();}$(window).on('load', initSorter);function dtf_filterResults( value ){table_sorter.filter( value );tableResize.resize();return false;}$(window).on('load', function(event) {form_update(document.forms);});$(window).on('load', function(){new DigitalClock('clock', 1563830985);});
$(window).on('resize', function(){handle_window_resize();});
warningcheckintervalmultiplier = 30;
//]]>
</script>
<link rel="shortcut icon" href="/favicon.ico" type="image/vnd.microsoft.icon"/>
<link rel="icon" href="/favicon.ico" type="image/vnd.microsoft.icon"/>
</head>
<body>
<div id="ttFwHeader">
<div id="header_title">
<div id="header_logo">
<a href="/overview"><img src="/inc/cisco.png?etag=1640-1537279820" style="width:85px;height:59px;" alt="Cisco" title="Cisco" /></a>
<span class='header_product_logo header_product_logo_category' >
Cisco TelePresence</span>
<span class='header_product_logo' >
Video Communication Server Expressway</span>
<a href="#ttFwContent" title="Skip page navigation." class="navjump">Skip page navigation</a></div>
</div>
<div class="popupbubble" id="warningpopup" style="display:none;"><div class="popupbubble_le"><div class="popupbubble_ri"><a href="alarms" class="popupbubble_ct">This system has 4 alarms</a></div></div></div><div id="header_icons"><a href="alarms" id="warningicon"><img src="/inc/warning.gif?etag=560-1537279820" style="width:15px;height:15px;" alt="This system has 4 alarms" title="This system has 4 alarms"  id="warningimg"/></a>
<a href="/inc/help/en_US.utf8/VCS_help_CSH.htm#zones" onclick="return openHelpWindow('/inc/help/en_US.utf8/VCS_help_CSH.htm#zones', true, 'MCWebHelpXC');"><img src="/inc/icon_help.gif?etag=1070-1537279820" style="width:16px;height:16px;" alt="Help on this page" title="Help on this page" /></a>
<a href="/inc/help/en_US.utf8/VCS_help_CSH.htm#zones" class="icontext" onclick="return openHelpWindow('/inc/help/en_US.utf8/VCS_help_CSH.htm#zones', true, 'MCWebHelpXC');;return false;" >Help </a><a href="logout"><img src="/inc/icon_logout.gif?etag=1064-1537279820" style="width:16px;height:16px;" alt="Log out" title="Log out" /></a>
<a href="logout" class="icontext">Logout</a> </div><div id="header_menu">
<ul id="m2" style="display: none;">
<li><a href="overview"onclick='return false;'>Status</a><ul><li><a href="overview">Overview</a></li>
<li><a href="alarms">Alarms</a></li>
<li><a href="systeminformation"onclick='return false;'>System</a><ul><li><a href="systeminformation">Information</a></li>
<li><a href="ethernetstatus">Ethernet</a></li>
<li><a href="ipstatus">IP</a></li>
<li><a href="resourceusage">Resource usage</a></li>
</ul></li>
<li><a href="registrations"onclick='return false;'>Registrations</a><ul><li><a href="registrations">By device</a></li>
<li><a href="registrationsbyalias">By alias</a></li>
<li><a href="registrationhistory">History</a></li>
</ul></li>
<li><a href="calls"onclick='return false;'>Calls</a><ul><li><a href="calls">Calls</a></li>
<li><a href="callhistory">History</a></li>
</ul></li>
<li><a href="searchhistory">Search history</a></li>
<li><a href="localzonestatus">Local Zone</a></li>
<li><a href="zonestatus">Zones</a></li>
<li><a href="linkstatus"onclick='return false;'>Bandwidth</a><ul><li><a href="linkstatus">Links</a></li>
<li><a href="pipestatus">Pipes</a></li>
</ul></li>
<li><a href="policyservicestatus">Policy services</a></li>
<li><a href="turnrelays">TURN relay usage</a></li>
<li><a href="edgestatus">Unified Communications status</a></li>
<li><a href="publishers"onclick='return false;'>Applications</a><ul><li><a href="publishers"onclick='return false;'>Presence</a><ul><li><a href="publishers">Publishers</a></li>
<li><a href="presentities">Presentities</a></li>
<li><a href="subscribers">Subscribers</a></li>
</ul></li>
<li><a href="b2buastatus">Microsoft interoperability</a></li>
</ul></li>
<li><a href="hardware">Hardware</a></li>
<li><a href="eventlog"onclick='return false;'>Logs</a><ul><li><a href="eventlog">Event Log</a></li>
<li><a href="configurationlog">Configuration Log</a></li>
<li><a href="networklog">Network Log</a></li>
</ul></li>
</ul></li>
<li><a href="system"onclick='return false;'>System</a><ul><li><a href="system">Administration settings</a></li>
<li><a href="#"onclick='return false;'>Network interfaces</a><ul><li><a href="ethernet">Ethernet</a></li>
<li><a href="ip">IP</a></li>
<li><a href="routeadd">Static routes</a></li>
</ul></li>
<li><a href="dns">DNS</a></li>
<li><a href="time">Time</a></li>
<li><a href="snmp">SNMP</a></li>
<li><a href="clustering">Clustering</a></li>
<li><a href="#"onclick='return false;'>Protection</a><ul><li><a href="#"onclick='return false;'>Firewall rules</a><ul><li><a href="firewallrulesconfig">Configuration</a></li>
<li><a href="activefirewallrules">Current active rules</a></li>
</ul></li>
<li><a href="protectionoverview"onclick='return false;'>Automated detection</a><ul><li><a href="protectionoverview">Configuration</a></li>
<li><a href="protectionexemptions">Exemptions</a></li>
<li><a href="protectionbanlist">Blocked addresses</a></li>
</ul></li>
</ul></li>
<li><a href="uploadwelcomemessage">Login page</a></li>
<li><a href="qos">Quality of Service</a></li>
<li><a href="externalmanager">External manager</a></li>
<li><a href="tmsservices">TMS Provisioning Extension services</a></li>
</ul></li>
<li><a class=" selected" href="h323"onclick='return false;'>Configuration</a><ul><li><a href="h323"onclick='return false;'>Protocols</a><ul><li><a href="h323">H.323</a></li>
<li><a href="sip">SIP</a></li>
<li><a href="interworking">Interworking</a></li>
</ul></li>
<li><a href="registrationconfig"onclick='return false;'>Registration</a><ul><li><a href="registrationconfig">Configuration</a></li>
<li><a href="allowlist">Allow List</a></li>
<li><a href="denylist">Deny List</a></li>
</ul></li>
<li><a href="outboundconnectioncredentials"onclick='return false;'>Authentication</a><ul><li><a href="outboundconnectioncredentials">Outbound connection credentials</a></li>
<li><a href="credentials"onclick='return false;'>Devices</a><ul><li><a href="credentials">Local database</a></li>
<li><a href="ntlm">Active Directory Service</a></li>
<li><a href="ldap">H.350 directory service</a></li>
<li><a href="ldapschemas">H.350 directory schemas</a></li>
</ul></li>
</ul></li>
<li><a href="callconfig">Call routing</a></li>
<li><a href="defaultsubzone"onclick='return false;'>Local Zone</a><ul><li><a href="defaultsubzone">Default Subzone</a></li>
<li><a href="traversalsubzone">Traversal Subzone</a></li>
<li><a href="subzones">Subzones</a></li>
<li><a href="membershiprules">Subzone membership rules</a></li>
</ul></li>
<li><a class=" selected" href="zones"onclick='return false;'>Zones</a><ul><li><a class=" selected" href="zones">Zones</a></li>
<li><a href="defaultzoneaccessrules">Default Zone access rules</a></li>
</ul></li>
<li><a href="domains">Domains</a></li>
<li><a href="edge"onclick='return false;'>Unified Communications</a><ul><li><a href="edge">Configuration</a></li>
<li><a href="staticroutes">Federated static routes</a></li>
<li><a href="federationallowlist">Federated domains allow list</a></li>
<li><a href="federationdenylist">Federated domains deny list</a></li>
</ul></li>
<li><a href="dialplanconfig"onclick='return false;'>Dial plan</a><ul><li><a href="dialplanconfig">Configuration</a></li>
<li><a href="transforms">Transforms</a></li>
<li><a href="searchrules">Search rules</a></li>
<li><a href="policyservices">Policy services</a></li>
</ul></li>
<li><a href="bandwidth"onclick='return false;'>Bandwidth</a><ul><li><a href="bandwidth">Configuration</a></li>
<li><a href="links">Links</a></li>
<li><a href="pipes">Pipes</a></li>
</ul></li>
<li><a href="ports"onclick='return false;'>Traversal</a><ul><li><a href="ports">Ports</a></li>
<li><a href="turn">TURN</a></li>
<li><a href="locallyregisteredendpoints">Locally registered endpoints</a></li>
</ul></li>
<li><a href="adminpolicy"onclick='return false;'>Call Policy</a><ul><li><a href="adminpolicy">Configuration</a></li>
<li><a href="callpolicywizard">Rules</a></li>
</ul></li>
</ul></li>
<li><a href="conferencefactory"onclick='return false;'>Applications</a><ul><li><a href="conferencefactory">Conference Factory</a></li>
<li><a href="presence">Presence</a></li>
<li><a href="b2buaconfig"onclick='return false;'>B2BUA</a><ul><li><a href="b2buaconfig"onclick='return false;'>Microsoft interoperability</a><ul><li><a href="b2buaconfig">Configuration</a></li>
<li><a href="b2bualisteners">Trusted hosts</a></li>
<li><a href="b2buatranscoders">External transcoders</a></li>
<li><a href="b2buarules">External transcoder policy rules</a></li>
<li><a href="b2buarestart">Restart service...</a></li>
</ul></li>
<li><a href="b2buaturn">B2BUA TURN servers</a></li>
</ul></li>
<li><a href="userpolicy">FindMe</a></li>
<li><a href="fusioncerts">Cloud Certificate management</a></li>
</ul></li>
<li><a href="adminaccounts"onclick='return false;'>Users</a><ul><li><a href="adminpasswordsecurity">Password security</a></li>
<li><a href="adminaccounts">Administrator accounts</a></li>
<li><a href="admingroups">Administrator groups</a></li>
<li><a href="adminsessions">Active administrator sessions</a></li>
<li><a href="loginldap">LDAP configuration</a></li>
</ul></li>
<li><a href="upgrade"onclick='return false;'>Maintenance</a><ul><li><a href="upgrade">Upgrade</a></li>
<li><a href="logging">Logging</a></li>
<li><a href="optionkeys">Option keys</a></li>
<li><a href="loggingsnapshot"onclick='return false;'>Tools</a><ul><li><a href="locate">Locate</a></li>
<li><a href="checkpattern">Check pattern</a></li>
<li><a href="localportlist"onclick='return false;'>Port usage</a><ul><li><a href="localportlist">Local inbound ports</a></li>
<li><a href="sourceportlist">Local outbound ports</a></li>
<li><a href="remoteportlist">Remote listening ports</a></li>
</ul></li>
<li><a href="ping"onclick='return false;'>Network utilities</a><ul><li><a href="ping">Ping</a></li>
<li><a href="traceroute">Traceroute</a></li>
<li><a href="tracepath">Tracepath</a></li>
<li><a href="dnslookup">DNS lookup</a></li>
<li><a href="connectivitytest">Connectivity test</a></li>
</ul></li>
</ul></li>
<li><a href="trustedcacertificate"onclick='return false;'>Security</a><ul><li><a href="trustedcacertificate">Trusted CA certificate</a></li>
<li><a href="servercertificate">Server certificate</a></li>
<li><a href="crlupdater">CRL management</a></li>
<li><a href="certificatetesting">Client certificate testing</a></li>
<li><a href="cbaconfig">Certificate-based authentication configuration</a></li>
<li><a href="domaincertificate">Domain certificates</a></li>
<li><a href="ciphers">Ciphers</a></li>
<li><a href="sshconfig">SSH configuration</a></li>
</ul></li>
<li><a href="backuprestore">Backup and restore</a></li>
<li><a href="loggingsnapshot"onclick='return false;'>Diagnostics</a><ul><li><a href="loggingsnapshot">Diagnostic logging</a></li>
<li><a href="snapshot">System snapshot</a></li>
<li><a href="incidentreporting"onclick='return false;'>Incident reporting</a><ul><li><a href="incidentreporting">Configuration</a></li>
<li><a href="incidentview">View</a></li>
</ul></li>
<li><a href="networkloglevels"onclick='return false;'>Advanced</a><ul><li><a href="networkloglevels">Network Log configuration</a></li>
<li><a href="developerloglevels">Support Log configuration</a></li>
</ul></li>
<li><a href="hybridservicesloglevels">Hybrid Services Log Levels</a></li>
</ul></li>
<li><a href="maintenancemode">Maintenance mode</a></li>
<li><a href="webprefs">Language</a></li>
<li><a href="maintenancemode"onclick='return false;'>Serviceability</a><ul><li><a href="sch">Smart Call Home</a></li>
</ul></li>
<li><a href="restartoptions">Restart options</a></li>
</ul></li>
</ul></div> <!-- menu -->
<div id="header_location">
<div id="header_location_title">
<span>Zones</span>
</div>
<div id="header_location_map">
<span>You are here:</span>
<span>
<a href="h323">Configuration</a>
<img src="/inc/bullet.gif?etag=57-1537279820" style="width:8px;height:7px;" alt="" title="" /><a href="zones">Zones</a>
<img src="/inc/bullet.gif?etag=57-1537279820" style="width:8px;height:7px;" alt="" title="" />Zones
</span>
</div>
</div>
</div>
<div id="ttFwContent">
<div id="content" class="layout">
<form class='tt_form' name="zones_table" id="zones_table" method="post" action="zones" ><div class="scrollable_table_container"><div class="scrollable_thead_container" style="display:none;"><table class="status_table"><thead>
<tr>
<th align="center" style="width:30px;"></th>
<th><a href="#" onclick="table_sorter.sort('Name',true);return false;">Name</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort1"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort1"/></th>
<th><a href="#" onclick="table_sorter.sort('Type',true);return false;">Type</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort2"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort2"/></th>
<th><a href="#" onclick="table_sorter.sort('Calls',true);return false;">Calls</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort3"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort3"/></th>
<th><a href="#" onclick="table_sorter.sort('Bandwidth used',true);return false;">Bandwidth used</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort4"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort4"/></th>
<th><a href="#" onclick="table_sorter.sort('H323 status',true);return false;">H323 status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort5"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort5"/></th>
<th><a href="#" onclick="table_sorter.sort('SIP status',true);return false;">SIP status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort6"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort6"/></th>
<th><a href="#" onclick="table_sorter.sort('Search rule status',true);return false;">Search rule status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort7"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort7"/></th>
<th>Actions</th>
</tr>
</thead>
</table></div><div class="scrollable_tbody_container"><div>
<table class="status_table" id='zones_table_table' >
<thead>
<tr>
<th align="center" style="width:30px;"></th>
<th><a href="#" onclick="table_sorter.sort('Name',true);return false;">Name</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort1"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort1"/></th>
<th><a href="#" onclick="table_sorter.sort('Type',true);return false;">Type</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort2"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort2"/></th>
<th><a href="#" onclick="table_sorter.sort('Calls',true);return false;">Calls</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort3"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort3"/></th>
<th><a href="#" onclick="table_sorter.sort('Bandwidth used',true);return false;">Bandwidth used</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort4"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort4"/></th>
<th><a href="#" onclick="table_sorter.sort('H323 status',true);return false;">H323 status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort5"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort5"/></th>
<th><a href="#" onclick="table_sorter.sort('SIP status',true);return false;">SIP status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort6"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort6"/></th>
<th><a href="#" onclick="table_sorter.sort('Search rule status',true);return false;">Search rule status</a><img src="/inc/tablesort_asc.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowUpSort7"/><img src="/inc/tablesort_des.gif?etag=114-1537279820" style="" alt="" title=""  class="tableSortArrow arrowDownSort7"/></th>
<th>Actions</th>
</tr>
</thead>
<tbody class="status_table_highlight" id="zones_table_tbody">
<tr>
<td align="center" style="width:30px;"></td><td><a href="defaultzone">DefaultZone</a></td><td>Default zone</td>
<td>0</td>
<td>0 kbps</td>
<td>On</td>
<td>On</td>
<td></td>
<td><a href='defaultzone'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[1]" value="1" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=1">e-CUSP</a></td><td>Neighbor</td>
<td>0</td>
<td>0 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>Enabled <a href="searchrules?target=ZS1DVVNQ&enabled=Enabled">search rules</a>: 5</p></td><td><a href='editzone?id=1'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[2]" value="2" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=2">i-CUSP-internet</a></td><td>Neighbor</td>
<td>0</td>
<td>0 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>Enabled <a href="searchrules?target=aS1DVVNQLWludGVybmV0&enabled=Enabled">search rules</a>: 2</p></td><td><a href='editzone?id=2'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[3]" value="3" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=3">i-CUSP-WebEx</a></td><td>Neighbor</td>
<td>0</td>
<td>0 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>Disabled <a href="searchrules?target=aS1DVVNQLVdlYkV4&enabled=Disabled">search rules</a>: 3</p></td><td><a href='editzone?id=3'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[4]" value="4" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=4">Ben_testzone</a></td><td>Neighbor</td>
<td>0</td>
<td>0 kbps</td>
<td>Off</td>
<td>Failed</td>
<td><p>No <a href="searchrules">search rules</a> configured</p></td><td><a href='editzone?id=4'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[5]" value="5" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=5">eCP-3.5</a></td><td>Neighbor</td>
<td>3</td>
<td>8992 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>Enabled <a href="searchrules?target=ZUNQLTMuNQ==&enabled=Enabled">search rules</a>: 1</p></td><td><a href='editzone?id=5'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[6]" value="6" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=6">iCP-3.5</a></td><td>Neighbor</td>
<td>3</td>
<td>8992 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>Enabled <a href="searchrules?target=aUNQLTMuNQ==&enabled=Enabled">search rules</a>: 3</p></td><td><a href='editzone?id=6'>View/Edit</a></td></tr>
<tr>
<td class="checkbox-cell" align="center" style="width:30px;"><input type="checkbox" name="selection[7]" value="7" onclick="form_update($(this.form));event.cancelBubble=true;"/></td><td><a href="editzone?id=7">iCP-3.0</a></td><td>Neighbor</td>
<td>0</td>
<td>0 kbps</td>
<td>Off</td>
<td>Active</td>
<td><p>No <a href="searchrules">search rules</a> configured</p></td><td><a href='editzone?id=7'>View/Edit</a></td></tr>
</tbody></table>
</div>
</div>
</div>
<input type="hidden" name="cmd" value="" />
<input type="hidden" name="returnto" value=""/>
<input type="hidden" name="sessionid" value="219e4ac92ccef369f743e04b7835e675f15c8a95760ed9edc0d754b15e278afe" />
<div id='zones_table_buttons'>
<input type="submit" name="new" value="New" id="new" onclick="this.form.returnto.value='/zones'; this.form.cmd.value='new'" class="button" onmouseover="this.className='button-hover'" onmouseout="this.className='button'" />
<input type="submit" name="btnCheckListener[delete]" value="Delete" onclick="return form_confirm(this.form,'Are you sure you want to delete the selected zone?',&quot;f=document.forms['zones_table'];f.returnto.value='/zones';f.cmd.value='delete';f.submit();&quot;,&quot;&quot;,&quot;Yes&quot;,&quot;No&quot;)" disabled="disabled"  class="button" onmouseover="this.className='button-hover'" onmouseout="this.className='button'" />
<input type="submit" name="selectAll" id="selectAll" value="Select all" onclick="return set_all_DTF_checkboxes(this.form,1);" class="button" onmouseover="this.className='button-hover'" onmouseout="this.className='button'" />
<input type="submit" name="btnCheckListener[unselectAll]" id="unselectAll" disabled="disabled" value="Unselect all" onclick="return set_all_DTF_checkboxes(this.form,0);" class="button" onmouseover="this.className='button-hover'" onmouseout="this.className='button'" />
</div>
</form>
</div> <!-- content -->
</div> <!-- ttFwContent -->
<div class="ttFwFooter">
<div class="container">
      <div class="left">
      <span class="label">User:</span>
      <span class="value">tigao</span>
      <span class="label">Access:</span>
      <span class="value">Read-write</span>
      <span class="label">System host name:</span>
      <span>me01sqvce101</span>
      <span class="label">System time:</span>
      <span id="clock">00:00</span>
      <span>PDT</span>
</div>
      <div class="right">
         <span class="label" title="Language: en_US.utf8">Language:</span>
         <span class="value" title="Language: en_US.utf8"><a href="webprefs">en_US</a></span>
         <span class="label">S/N:</span>
         <span class="value">02E277CA</span>
         <span class="label">Version:</span>
         <span class="value">X8.11.2</span>
</div>
</div>
</div> <!-- ttFwFooter -->
<div id="dlg-1-O" title="DIALOG TITLE" class="overlayContentContainer"></div><script type="text/javascript">
//<![CDATA[

setTimeout( function () {check_login();}, 30*60*1000);
vcs.updateRequiredFields();
//]]>
</script>
</body>
</html>
'''

# soup = bs4(xml,'html.parser')
# pprint(soup.find_all(name='a', attrs={'href':"editzone"}))


# client_pattern_with_upgrade = re.compile(
#         "(.*)\s* in\s* (dmz|local)\s* with\s* (server|pool)=(.*)\s* build=(.*) upgrade=(.*)", re.I)
# incoming_msg = "page in local with pool=10.224.89.100 build=WBXpage.T33L-39.7.0 WBXpagecommon-39.7.0 upgrade=True"
# p_result = client_pattern_with_upgrade.findall(incoming_msg)
# print(p_result)

CMCURL_MAPPING = {"QA": {"URL": "csgcmc.qa.webex.com",
                         "KEY": "Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4="},
                  "DMZ": {"URL": "sjcmc.dmz.webex.com",
                          "KEY": "Q01DQVBJX0RNWjo5M2IyOGNiNzQ4NjM0YmJmYTI4YWZkNWVhODQ2NGY3Mg=="},
                  "ENG": {"URL": "sjcmc.eng.webex.com",
                          "KEY": "Q01DUUFfQVBJX0hGTEFCX2tleTozZmJmYTkwNWZiODQ0ODZjOGVkNzg0MTcyYzFjNDE4NA=="}}
#
# class CMCInfo:
#     def __init__(self, component, env):
#         self.component = component
#         self.env = env
#         self.cmcurl = CMCURL_MAPPING.get(self.env).get("URL")
#         self.key = CMCURL_MAPPING.get(self.env).get("KEY")
#         self.headers = dict(Authorization=f"Basic {self.key}")
#
#     def getserverbypool(self, pool=None, filtertype=None):
#         if pool is None:
#             pool = self.pool
#         box_url = 'https://%s/cmc/api/sitBoxList/%s/?pool=%s&ignore_owner=yes' % (self.cmcurl, self.component, pool)
#         req = requests.get(box_url, headers=self.headers)
#         ret = req.json().get('rows')
#         # print(ret)
#         if filtertype:
#             servers = [{server.get('name'): server.get('ip')} for server in ret if
#                        server.get('type') in filtertype]
#         else:
#             for server in ret:
#                 yield server # {server.get('name'): server.get('ip')}
#         #     servers = ({server.get('name'): server.get('ip')} for server in ret)
#         # return servers
#
#
# begin = time.time()
# cmcinfo = CMCInfo('j2ee','DMZ')
# ret = cmcinfo.getserverbypool('jsq1','j2eeweb,')
#
# #print(cmcinfo.getserverbypool('jsq1','j2eeweb,'))
# for server in ret:
#     if server.get('type') in 'j2eeweb,':
#         print({server.get('name'): server.get('ip')})
# end = time.time()
# elapsed_time = end - begin
# print("Elapsed time is %ss." % elapsed_time)
#

# from multiprocessing import Pool, Manager
# manager = Manager()
# workQueue = manager.Queue()
# component_name='j2ee'
# service_version='39.8.0'
# build_no='0000'
#
# workQueue.put('-'.join([component_name,service_version,build_no]))
# ret = workQueue.get()
# print(ret)
#
#
#
# from fabric import Connection
#
# result = Connection('10.224.89.100',user='wbxroot',connect_kwargs={'password':'wbx@AaR00t'}).run('hostname',hide=False)
# print(result)
