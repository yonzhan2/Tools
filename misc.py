# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">...</p>
# """
#
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')
#
# #print(soup.prettify())
#
# print soup.title.string
#
# print soup.find_all('a')[0]['id']
# print soup.get_text()


# coding=utf-8
# from selenium import webdriver
# import unittest, time
# class TestLogin(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox()
#         self.driver.maximize_window()
#         self.driver.implicitly_wait(5)
#         self.base_url = "http://mail.qa.webex.com"
#         self.verificationErrors = []
#         self.accept_next_alert = True
#     def test_login(self):
#         driver = self.driver
#         driver.get(self.base_url)
#
#         driver.find_element_by_id("usernameshow").clear()
#         driver.find_element_by_id("usernameshow").send_keys("yonzhan2@qa.webex.com")
#         driver.find_element_by_id("pwshow").clear()
#         driver.find_element_by_id("pwshow").send_keys("Aa1234")
#         driver.find_element_by_class_name("Bsbttn").click()
#         print driver.find_elements_by_tag_name('frame')
#         driver.switch_to.frame('f1')
#         driver.find_element_by_xpath('html/body/a[2]').click()
#         driver.implicitly_wait(2)
#         print driver.window_handles
#         #driver.switch_to.window(driver.window_handles[0])
#         print driver.find_elements_by_tag_name('frame')
#         #driver.switch_to.parent_frame(driver.switch_to.frame('f1'))
#         driver.switch_to.default_content()
#         driver.switch_to.frame('f2')
#         driver.switch_to.frame('f3')
#         driver.find_element_by_xpath('html/body/form/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]/input').send_keys('yonzhan2@qa.webex.com')
#         driver.find_element_by_xpath('html/body/form/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/input').send_keys('test by yong' + '_'  +  str(time.time()))
#         driver.find_element_by_xpath(".//*[@id='EasyMail_Text']").send_keys('test')
#         #upload file
#         driver.switch_to.default_content()
#         #driver.switch_to.frame('f1')
#         driver.switch_to.frame('f2')
#         #driver.switch_to.frame('f3')
#         driver.switch_to.frame('f4')
#         upload = driver.find_element_by_class_name('textbox')
#         upload.send_keys('/tmp/progress.log')
#         print upload.get_attribute('value')
#         driver.find_element_by_xpath('html/body/form/table/tbody/tr/td/input[3]').click()
#         driver.switch_to.default_content()
#         driver.switch_to.frame('f2')
#         driver.switch_to.frame('f3')
#         time.sleep(5)
#         driver.find_element_by_xpath('html/body/form/table/tbody/tr[1]/td/input[1]').click()
#         driver.implicitly_wait(5)
#         driver.switch_to.default_content()
#         #driver.switch_to.parent_frame()
#         #driver.switch_to.frame('f1')
#         #driver.switch_to.frame('f2')
#         #driver.find_element_by_xpath('html/body/table/tbody/tr/td[2]/form/table/tbody/tr[4]/td/input').click()
#         #driver.find_element_by_class_name('Bsbttn').click()
#     def tearDown(self):
#         self.driver.quit()
#         self.assertEqual([], self.verificationErrors)
# if __name__ == "__main__":
#     unittest.main()


# def timeConvert(s, isGMT8=True):
#     if isGMT8:
#         return s[-4:] + '-' + s[4:7] + '-' + s[8:10] + ' ' + s[11:-5] + ' GMT+08:00'
#     else:
#         return s[-4:] + '-' + s[4:7] + '-' + s[8:10] + ' ' + s[11:-5] + ' GMT-07:00'
# print timeConvert(rpmdata[0][1])
#
#
#
# builds = [('WBXsuper-32.5.0-679.src.rpm', 'Wed Jul 26 08:48:54 2017', 'Wed Jul 26 23:38:00 2017'), ('WBXsuperui-32.5.0-679.src.rpm', 'Wed Jul 26 08:49:09 2017', 'Wed Jul 26 23:37:33 2017')]
#
# for build in builds:
#     print build[0],
# if 'WBXsuper-32.5.0-679.src.rpm' in (build[0],):
#     print True
# else:
#     print False
#
# from datetime import datetime,timedelta,tzinfo
# import time
# class GMT8(tzinfo):
#     delta=timedelta(hours=8)
#     def utcoffset(self,dt):
#         return self.delta
#     def tzname(self,dt):
#         return "GMT+8"
#     def dst(self,dt):
#         return self.delta
#
# class GMT(tzinfo):
#     delta=timedelta(0)
#     def utcoffset(self,dt):
#         return self.delta
#     def tzname(self,dt):
#         return "GMT+0"
#     def dst(self,dt):
#         return self.delta
# from_tzinfo=GMT()#GMT tz +0
# local_tzinfo=GMT8()#Local tz,+8
# gmt_time = datetime.strptime('2011-08-15 21:17:14', '%Y-%m-%d %H:%M:%S')
# gmt_time = gmt_time.replace(tzinfo=from_tzinfo)
# local_time = gmt_time.astimezone(local_tzinfo)
#
# print gmt_time,local_time
#



#
# import paramiko,re,socket
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# p1 = re.compile(r"Name : (.+?) Relocations:(.+?) Version :(.+?) Vendor: \(none\) Release : (.+?) Build Date")  #(.+?)Release :  Build Date:
# p2 = re.compile(r"Build Date: (.+?) Install Date:")
# p3 = re.compile(r"Install Date: (.+?) Build Host:")
# PkgDict = {}
# #server="10.224.89."
# #rpmcmd= "for i in `sudo rpm -qa|grep WBXpage`; do echo `sudo rpm -qi $i` ;done"
# type='Superadmin'
# server = "10.224.82.69"
# rpmcmd = "for i in `sudo rpm -qa|grep WBXsuper`; do echo `sudo rpm -qi $i` ;done"
# for user, pwd in zip(['wbxbuilds'], ['P0w3rSupply!']):
#     try:
#         ssh.connect(server, username=user, password=pwd,timeout=30)
#         stdin, stdout, stderr = ssh.exec_command(rpmcmd)
#         break
#     except:
#         pass
# with open('/tmp/stdout','w+') as f:
#     f.write(stdout.read())
# with open('/tmp/stdout') as fh:
#     f = fh.read()
# print "content of f:" ,f
# p1_ret = re.findall(p1, f)
# print 'p1 :',p1_ret
# buildsinfo = [ '{0}-{1}-{2}'.format(build[0].strip(),build[2].strip(),build[3].strip()) for build in p1_ret]
#
# print buildsinfo
#
# print 'p2', re.findall(p2,f)
# print 'p3', re.findall(p3,f)
# rpmdata = zip(buildsinfo, re.findall(p2, f), re.findall(p3, f))
# print rpmdata
# PkgDict[type] = {"builds": [line for line in sorted(rpmdata)]}
# print 'it is' , PkgDict
#
#
# import time,datetime
# # print time.strftime("%Y-%m-%d %H:%M:%S",time.strptime("Thu Nov 08 17:15:30 +0800 2012", "%a %b %d %H:%M:%S +0800 %Y"))
# #
# print time.strftime("%Y-%m-%d %H:%M:%S", time.strptime("Fri 30 Jun 2017 07:49:46 PM GMT", "%a %d %b %Y %H:%M:%S %p GMT"))
#
# t1 = time.mktime(time.strptime("Fri 28 Jul 2017 02:00:01 PM GMT", "%a %d %b %Y %I:%M:%S %p GMT"))
# #t2 = time.mktime(time.strptime("Fri 30 Jun 2017 07:49:45 PM GMT", "%a %d %b %Y %H:%M:%S %p GMT"))
#
# #print time.mktime(time.localtime())
# print 't1',t1

#
# print time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(t1))
# print time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(t2))
# 1501250401
#
# def timeConvert(s):
#     timestruct = time.strptime(s, "%a %d %b %Y %I:%M:%S %p GMT")
#     timeformat = time.strftime("%Y-%m-%d %H:%M:%S",timestruct)
#     timestamp = time.mktime(timestruct)
#     return timeformat,timestamp
#
# #print timeConvert(p2[0])[0]
#
#
# import requests
# url = 'http://10.224.57.21:8090/data/v1/buildDeployHistory/QA/packageList?appKey=qatest&appSecret=CntbrbG-aSTCHdYe3Pa8NrT7XtlMGEKV2NSlD9B_Xmk'
# headers= {'Content-Type':'application/json;charset=UTF-8'}
# try:
#     r = requests.post(url,headers=headers,data=("name"))
#     print 'response staus is', r.status_code
#     print 'response content is', r.content
# except:
#     print "call api failed"
#
#



import requests
import json


def SendMsgToSparkRoom(msg=None):
    sparkapi = 'https://api.ciscospark.com/v1/messages'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
    headers['User-Agent'] = useragent
    roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
    # roomId = '28e3c750-6908-11e6-a747-2b856e15b09b' ##this is CMR Scrum Room
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


SendMsgToSparkRoom("test from python1 @yonzhan2@cisco.com")
