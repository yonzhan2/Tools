import requests
import os
import time
import re
from threading import Lock
import threading
import pprint

# cmcurl = "csgcmc.qa.webex.com"
cmcurl = "sjcmc.eng.webex.com"

###QA CMC headers
# headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

###SJ CMC headers
headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}
current_dir = os.path.dirname(__file__)
start = time.time()
iplist = []


def getpools():
    url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    session = requests.Session()
    session.headers = headers
    req = session.get(url)

    ret = req.json()[0].get('children')
    pools = [cld['name'] for child in ret for cld in child['children']]
    ### filter TA pools
    pools = [pool for pool in pools if not re.search("ta|pj|pf|px|py|sd|bala", pool)]
    return pools


def getPoolsIP(poolname):
    url = 'https://%s/cmc/api/sitBoxList/logstashagent/?pool=%s&ignore_owner=yes' % (cmcurl, poolname)
    session = requests.Session()
    session.headers = headers
    req = session.get(url)
    ret = req.json().get('rows')
    ips = [ip.get('ip') for ip in ret]
    iplist.extend(ips)


if __name__ == "__main__":
    start = time.time()
    threads = []
    for pool in getpools():
        threads.append(threading.Thread(target=getPoolsIP, args=(pool,)))
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
    end = time.time() - start
    pprint.pprint(iplist)
    print("eclipsed time1: ", end)

    start2 = time.time()
    for pool in getpools():
        getPoolsIP(pool)
    end = time.time() - start2
    print("eclipsed time2: ", end)
