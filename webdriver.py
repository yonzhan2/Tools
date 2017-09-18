import os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from requests import get
import json

from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

status = {}
status_json = '/tmp/status.json'


def getCuspStatus(cusp):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)

    # driver = webdriver.Firefox() # Instantiate a webdriver object
    driver.get('http://{}/admin/Common/HomePage.do'.format(cusp))

    # print dir(driver)

    elem_user = driver.find_element_by_id("username")
    elem_user.send_keys("monitor")
    elem_pwd = driver.find_element_by_id("password")
    elem_pwd.send_keys("C!sco$cusp")
    elem_pwd.send_keys(Keys.RETURN)

    driver.switch_to.frame('contentiframe')
    ret = driver.find_element_by_xpath(".//*[@id='dash2']/fieldset/table/tbody/tr/td[2]").text
    status[cusp] = ret
    print status
    driver.save_screenshot(cusp + '.png')
    driver.quit()


cusps = ['173.37.48.122', '173.37.48.124']

for cusp in cusps:
    getCuspStatus(cusp)
    with open(status_json, 'w+') as f:
        f.write(json.dumps(status))

from_addr = 'dmzhealthcheck@cisco.com'
to_addr = ['yonzhan2@cisco.com', 'tigao@cisco.com', 'qidong@cisco.com', 'huixzhan@cisco.com', 'hf-cme@cisco.com']
send_date = time.strftime('%m/%d/%Y %H:%M:%S GMT', time.localtime(time.time()))


def sendmail():
    msg = MIMEMultipart()
    att1 = MIMEText(open(cusp + '.png', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename=cusp + ".png"'
    msg.attach(att1)
    # msg = MIMEText('[' + send_date +']' + ' ' + str(cusp) + ' : ' + status.get(cusp) + ' Please Check ASAP! Thanks' , 'plain', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr)
    msg['Subject'] = Header(u'DMZ Healthcheck Alter on ' + cusp, 'utf-8').encode()
    server = smtplib.SMTP('localhost')
    # server.set_debuglevel(1)
    server.sendmail(from_addr, to_addr, msg.as_string())


def checkStatus():
    try:
        if os.path.isfile(status_json):
            with open(status_json) as f:
                ret = json.load(f)[cusp]
                if ret == "All Server Group Elements are up!":
                    status[cusp] = ret
                    return True
                else:
                    status[cusp] = ret
                    return False
    except Exception, e:
        print e


for cusp in cusps:
    if not checkStatus():
        sendmail()
