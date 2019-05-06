#!/usr/local/bin/python

from __future__ import print_function
import paramiko
import requests
import threading
import re

cmcurl = "sjcmc.dmz.webex.com"
headers = {'Authorization': 'Basic Q01DQVBJX0RNWl9rZXk6MGE1ZGJhYTFmY2E5NGVhZThiYTE4YzIzZDYyZmI3Yzg='}

##current_dir = os.path.dirname(__file__)

pool_lists = []
ip_lists = []
gLock = threading.Lock()


def get_pool_lists():
    # url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    session = requests.Session()
    session.headers = headers
    req = session.get(url)

    ret = req.json()[0].get('children')
    global pool_lists
    pool_lists = [cld['name'] for child in ret for cld in child['children']]
    ### filter TA pool_lists
    pool_lists = [pool for pool in pool_lists if not re.search("ta|pj|pf|px|py|sd|bala", pool)]
    return pool_lists


def get_ip():
    while True:
        gLock.acquire()
        if len(pool_lists) == 0:
            gLock.release()
            break
        else:
            pool = pool_lists.pop()
            gLock.release()
            url = 'https://%s/cmc/api/sitBoxList/logstashagent/?pool=%s&ignore_owner=yes' % (cmcurl, pool)
            req = requests.get(url, headers=headers)
            res = req.json()
            #           print(res)
            rows = res.get("rows")
            # print(rows)
            ip_lists.extend([rec.get('ip') for rec in rows])


def sync_time_with_gateway():
    '''Sync time with Gateway'''
    while True:
        gLock.acquire()
        if len(ip_lists) == 0:
            gLock.release()
            break
        else:
            server = ip_lists.pop()
            gLock.release()
            print("Sync Server %s" % server)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ntp_sync_cmd = '''
                            sudo sed -i 's/maxskew=100/maxskew=100000000/g' /usr/local/bin/ntpchk.sh
                            sudo service ntpd stop > /dev/null 2>&1
                            sudo ntpdate `sudo route -n | grep ^0.0.0.0 | awk '{print $2}'` > /dev/null 2>&1
                            sudo ntpdate `sudo route -n | grep ^0.0.0.0 | awk '{print $2}'` > /dev/null 2>&1
                            sudo service ntpd start  > /dev/null 2>&1
                            sudo chkconfig ntpd on
                            if [ $? -eq 0 ];then
                                echo "Sync Time Success on `hostname -i`" 
                            else
                                echo "Sync Time Failure on `hostname -i`"
                            fi
                            '''
            for user, pwd in zip(['wbxbuilds', 'shuqli'], ['P0w3rSupply!', 'wbx@Aa$hfcm']):
                # print user, pwd
                try:
                    ssh.connect(server, username=user, password=pwd, timeout=5)
                    stdin, stdout, stderr = ssh.exec_command(ntp_sync_cmd)
                    break
                except Exception as e:
                    print("error is ", e)

            print("stdout is ", stdout.read())


if __name__ == '__main__':

    ###Producer
    for i in range(3):
        th = threading.Thread(target=get_ip)
        # th.setDaemon(True)
        th.start()

    ###Consumer
    for i in range(4):
        th = threading.Thread(target=sync_time_with_gateway)
        # th.setDaemon(True)
        th.start()
