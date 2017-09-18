import requests
import re
import time
import threading

running_list = []
down_list = []
proxies = {
    "http": "http://proxy.esl.cisco.com:8080/",
}


class MyThread(threading.Thread):
    def __init__(self, seq):
        threading.Thread.__init__(self)
        self.seq = seq

    def run(self):
        getversion(self.seq)


def getversion(seq):
    try:

        # print seq
        # site_url = 'http://nebulasq{}.dmz.webex.com/mc3200/meetingcenter/support/support.do?siteurl=sqdemo&Action=downloads'.format (
        # seq)
        site_url = 'https://nebulabu.webex.com/mc3100/meetingcenter/support/support.do?siteurl=gpstest-t31-bu&Action=downloads'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        try:
            response = requests.get(site_url, headers, allow_redirects=False, timeout=10, proxies=proxies, verify=False)
            # print 'staus code is',response.status_code
            pageversion_pattern = re.compile(r'<span class=\"fr\">(.+?)</span>Page version:')
            clientversion_pattern = re.compile(r'<span class=\"fr\">(.+?)</span>Application version:')
            pageversion = pageversion_pattern.findall(response.text)[0].split('>')[-1]
            clientversion = clientversion_pattern.findall(response.text)[0].split('>')[-1]
            print "nebulsq{}'s page version is {},client version is {}".format(seq, pageversion, clientversion)
            # running_list.append('nebulsq{}'.format(seq))
            running_list.append('nebulabu')
        except:
            print "nebulsq{} Access Failed, please check !!!".format(seq)
            # down_list.append ('nebulsq{}'.format (seq))
            down_list.append('nebulabu')
    except:
        pass


if __name__ == '__main__':
    t1 = time.time()

    threads = []
    for seq in range(0, 1):
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
