import requests
import re
import time
import threading

running_list = []
down_list = []

class MyThread(threading.Thread):
    def __init__(self, seq):
        threading.Thread.__init__(self)
        self.seq = seq

    def run(self):
        getversion(self.seq)


def getversion(seq):
    try:

        # print seq
        site_url = 'http://nebulasq{}.dmz.webex.com/mc3200/meetingcenter/support/support.do?siteurl=sqdemo&Action=downloads'.format(
            seq)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        try:
            response = requests.get(site_url, headers=headers, allow_redirects=False, timeout=20, verify=False)
            # print 'staus code is',response.status_code
            pageversion_pattern = re.compile(r'Page version:<span class=\"fr\">(.+?)</span>')
            clientversion_pattern = re.compile(r'Application version:<span class=\"fr\">(.+?)</span>')
            pageversion = pageversion_pattern.findall(response.text)[0].split('>')[-1]
            clientversion = clientversion_pattern.findall(response.text)[0].split('>')[-1]
            #print 'pageversion,clientversion is',pageversion,clientversion
            print "nebulsq{}'s page version is {},client version is {}".format(seq, pageversion, clientversion)
            running_list.append('nebulsq{}'.format(seq))
        except Exception as e:
            print "nebulsq{} Access Failed, please check !!! {}".format(seq, e)
            down_list.append('nebulsq{}'.format(seq))
    except:
        pass


if __name__ == '__main__':
    t1 = time.time()

    threads = []
    for seq in range(0, 30):
        if seq == 0:
            seq = ''
        else:
            seq = '{:0>2}'.format(seq)
        threads.append(MyThread(seq))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t2 = time.time()
    used_time = t2 - t1
    print 'used_time:', used_time
    print sorted(running_list)
    print sorted(down_list)
