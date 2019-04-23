import requests
import threading
from bs4 import BeautifulSoup as bs4
from pprint import pprint
import urllib.request
import os

PAGE_URL_LIST = set()
IMG_URL_LIST = set()

# url = 'https://www.doutula.com/photo/list/'
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
# req = requests.get(url,headers=headers,timeout=10)
# res= req.content.decode('utf-8')
# #print(res)
# with open('content','w') as f:
#     f.write(res)

with open('content', 'r') as f:
    res = f.read()
soup = bs4(res, 'html.parser')
# print(soup.prettify())
imgurl = soup.find_all('img', src="//static.doutula.com/img/loader.gif")

for link in imgurl:
    IMG_URL_LIST.add(link.get("data-original"))

pprint(IMG_URL_LIST)


def download_img(url):
    file_name = url.split("/")[-1]
    if file_name.endswith('!dta'):
        file_name = file_name.split('!')[0]
    file_path = os.path.join('/Users/yonzhan2/Downloads/doutula', file_name)
    req = requests.get(url, headers=headers, timeout=5)
    data = req.content
    with open(file_path, 'wb') as f:
        f.write(data)
    print(file_name)


download_img('http://img.doutula.com/production/uploads/image//2019/04/10/20190410855635_MIXsdj.jpg!dta')
