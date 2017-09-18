#!/usr/bin/env/python

import requests
import json
import time
import sys
import threading


# data = '{"serviceName":"j2ee","version":"32.6.0:0000","user":"yonzhan2", "taskType":"service_refresh","requestId":"CI","requestType":"CMC","poolList":[{"name":"jhf3","boxList":["jhf3tc001.qa.webex.com"]}]}'

# taskid={}
class DeployJob:
    def __init__(self, type, version, pool, boxList):
        self.type = type
        self.version = version
        self.pool = pool
        self.boxList = boxList
        self.headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}
        self.requesturl = 'https://sjcmc.eng.webex.com/cmc/api/deploy/pool/request/'
        self.checkurl = 'https://sjcmc.eng.webex.com/cmc/api/deploy/task/'
        self.taskid = {}

    def getTaskId(self):
        data = '{"serviceName":"%s","version":"%s","user":"yonzhan2", "taskType":"service_refresh","requestId":"CI","requestType":"CMC","poolList":[{"name":"%s","boxList":[%s]}]}' % (
        self.type, self.version, self.pool, self.boxList)
        print data
        try:
            req = requests.get(self.requesturl, headers=self.headers, data=data)
            print req.content
            taskId = json.loads(req.content)['taskId']
            self.taskid[self.type] = taskId
            print self.type + '-' + self.pool + " taskId is", taskId
            return taskId
        except Exception, e:
            print e

    def getStatus(self):
        taskId = self.taskid.get(self.type)
        if not taskId:
            print "taskId is null,exit ..."
            sys.exit()
        try:
            req = requests.get(self.checkurl + str(taskId), headers=self.headers)
            ret = [status['status'] for status in json.loads(req.content)['poolList'][0]['boxList']]
            # print ret
            return ret
        except Exception, e:
            print e

    def checkStatus(self):
        taskId = self.taskid.get(self.type)
        while True:
            time.sleep(20)
            status = self.getStatus()
            print self.type + '-' + self.pool + " status is", status
            if all(map(lambda x: x == 'success', status)) or 'cancel' in status or 'time out' in status:
                break
            elif 'fail' in status and 'in progress' not in status:
                break
            else:
                status = self.getStatus()
        return status


def main(type, version, pool, boxList):
    dj = DeployJob(type, version, pool, boxList)
    dj.getTaskId()
    dj.getStatus()
    if all(map(lambda x: x == 'success', dj.checkStatus())):
        print "job is successful for " + type + '-' + pool
    elif any(map(lambda x: x == 'cancel', dj.checkStatus())):
        print "job is canceled for " + type + '-' + pool
    else:
        print "second job is running due to last job is failed for " + type + '-' + pool
        dj.getTaskId()


class MyThread(threading.Thread):
    def __init__(self, type, version, pool, boxList):
        threading.Thread.__init__(self)
        self.type = type
        self.version = version
        self.pool = pool
        self.boxList = boxList

    def run(self):
        main(self.type, self.version, self.pool, self.boxList)


if __name__ == "__main__":

    fobj = open('cmcmapping', 'r')

    threads = []
    for line in fobj.readlines():
        if not line.startswith('#') or line.strip():
            threads.append(MyThread(*line.split(',', 3)))

    fobj.close()

    for t in threads:
        t.start()
    for t in threads:
        t.join()
