# import time
# from selenium import webdriver
#
# # driver = webdriver.Firefox(r'C:\Users\yonzhan2\Downloads\chromedriver_win32\chromedriver.exe')  # Optional argument, if not specified will search path.
# driver = webdriver.Firefox()  # Optional argument, if not specified will search path.
#
# driver.get('http://www.google.com/xhtml');
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('python selenium')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!
# driver.quit()
#

# coding=utf-8
# from selenium import webdriver
# import sys
# print sys.path
#
#
# driver=webdriver.Firefox()
# url='http://www.baidu.com'
# driver.get(url)
# search_box = driver.find_element_by_name('search')
# search_box.send_keys('python selenium')
# search_box.submit()
#
# driver.close()

import time
from selenium import webdriver

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

driver = webdriver.Firefox()  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/xhtml');
time.sleep(5)  # Let the user actually see something!
search_box = driver.find_element_by_name('q')
print 'search_box is', search_box.tag_name
search_box.send_keys('python selenium')
search_box.submit()
time.sleep(5)  # Let the user actually see something!
driver.quit()
