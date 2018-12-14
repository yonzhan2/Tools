import os
import urllib
import urllib2
import threading
import time
import sys


class MultithreadDownload(threading.Thread):
    def __init__(self, url, startpos, endpos, f):
        threading.Thread.__init__(self)
        self.url = url
        self.startpos = startpos
        self.endpos = endpos
        self.fd = f

    def download(self):
        downloadsize = 0
        print "start thread: %s at %s" % (self.getName(), time.time())
        req = urllib2.Request(self.url)
        req.add_header("Range", "bytes=%s-%s" % (self.startpos, self.endpos))
        req.add_header('Accept-Encoding', '*')
        resp = urllib2.urlopen(req)
        self.fd.seek(self.startpos)
        self.fd.write(resp.read())
        self.fd.flush()
        downloadsize += os.path.getsize(filename)
        # print '[%s]%.0f' % ('=' * 20, int(downloadsize// filesize * 100)) + '%'
        print "stop thread: %s at %s" % (self.getName(), time.time())

    def run(self):
        self.download()


if __name__ == '__main__':
    url = 'http://rmc.webex.com/qa/j2ee/noarch/WBXclient.mac.T33L-33.9.0-128.noarch.rpm'
    # url = sys.argv[1]
    filename = url.split('/')[-1]
    urlHandler = urllib.urlopen(url)
    headers = urlHandler.info().headers
    for header in headers:
        if header.find('Length') != -1:
            length = header.split(':')[-1].strip()
            length = int(length)
    filesize = length
    print '%s filesize is %d' % (filename, filesize)

    threadnum = 50
    threading.BoundedSemaphore(threadnum)

    step = filesize // threadnum
    print 'step', step
    mtd_list = []
    start = 0
    end = -1

    tempf = open(filename, 'wb+')
    tempf.close()

    with open(filename, 'rb+') as f:
        fileno = f.fileno()
        print "fileno", fileno
        while end < filesize - 1:
            start = end + 1
            end = start + step - 1
            if end > filesize:
                end = filesize
            print "start:%s, end:%s" % (start, end)
            dup = os.dup(fileno)
            # print 'dup',dup
            fd = os.fdopen(dup, 'rb+', -1)
            # print 'fd',fd

            t = MultithreadDownload(url, start, end, fd)
            t.start()
    import time

    start = time.time()
    for i in mtd_list:
        i.setDaemon(True)
        i.start()


    def islive(tasks):
        for task in tasks:
            if task.isAlive():
                return True
        return False


    while islive(mtd_list):
        downloaded = sum([task.downloadsize for task in mtd_list])
        process = downloaded / float(filesize) * 100
        show = u'\rFilesize:%d Downloaded:%d Completed:%.2f%%' % (filesize, downloaded, process)
        sys.stdout.write(show)
        sys.stdout.flush()
        time.sleep(0.5)

    for i in mtd_list:
        i.join()
    end = time.time()
    elapsed = end - start
    print "elapsed time: ", elapsed
