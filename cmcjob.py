#!/usr/local/bin/python3

import requests
import json
import time
import sys
import threading
import logging
import argparse
import tempfile
import os

CMCURL_MAPPING = {"QA": {"URL": "csgcmc.qa.webex.com",
                         "KEY": "Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4="},
                  "DMZ": {"URL": "sjcmc.dmz.webex.com",
                          "KEY": "Q01DQVBJX0RNWl9rZXk6MGE1ZGJhYTFmY2E5NGVhZThiYTE4YzIzZDYyZmI3Yzg="}}


def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to cmcjob')

    parser.add_argument('-c', '--cmc_url',
                        required=True,
                        action='store',
                        help='CMC URL')

    parser.add_argument('-f', '--mapping_file',
                        required=True,
                        action='store',
                        help='cmc mapping file name')

    args = parser.parse_args()
    return args


class DeployJob:

    def __init__(self, cmc, type, version, pool, boxList):
        self.cmcurl = CMCURL_MAPPING.get(cmc).get("URL")
        self.key = CMCURL_MAPPING.get(cmc).get("KEY")
        self.type = type
        self.version = version
        self.pool = pool
        self.boxList = boxList
        self.headers = dict(Authorization=f"Basic {self.key}")
        self.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, ' \
                                     'like Gecko) Chrome/74.0.3729.131 Safari/537.36 '
        self.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,' \
                                 '*/*;q=0.8,application/signed-exchange;v=b3 '
        self.requesturl = f"https://{self.cmcurl}/cmc/api/deploy/pool/request/"
        self.checkurl = f"https://{self.cmcurl}/cmc/api/deploy/task/"
        self.taskid = {}
        self._server_info = '-'.join([self.type, self.pool, self.boxList.split(',')[0].strip().strip('"')])

    def getTaskId(self):
        data = '{"serviceName":"%s","version":"%s","user":"yonzhan2", "taskType":"service_refresh","additional":{' \
               '"refresh_option": {"configuration": "true", "service": "false", "package": "false"}}, ' \
               '"requestId":"CI", "requestType":"CMC","poolList":[{"name":"%s","boxList":[%s]}]}' % (
                   self.type, self.version, self.pool, self.boxList)
        logger.debug(data)
        try:
            req = requests.get(self.requesturl, headers=self.headers, data=data)
            logger.info(req.content)
            taskId = json.loads(req.content)['taskId']
            self.taskid[self.type] = taskId
            logger.info(self._server_info + " taskId is " + str(taskId))
            return taskId
        except Exception as e:
            print(e)

    def getStatus(self):
        taskId = self.taskid.get(self.type)
        if not taskId:
            logger.error("Error: taskId is null,exit ...")
            sys.exit()
        try:
            req = requests.get(self.checkurl + str(taskId) + '/', headers=self.headers)
            ret = [status['status'] for status in json.loads(req.content)['poolList'][0]['boxList']]
            # print("ret is", ret)
            return ret
        except Exception as e:
            print(f"Error of getStatus {e}")

    def checkStatus(self):
        taskId = self.taskid.get(self.type)
        status = self.getStatus()
        while True:
            time.sleep(20)
            logger.info(self._server_info + " status is " + str(status))
            if all([x == 'success' for x in status]) or 'cancel' in status or 'time out' in status:
                break
            elif 'fail' in status and 'in progress' not in status:
                break
            else:
                status = self.getStatus()
        return status


def main(cmc, type, version, pool, boxList):
    server_info = '-'.join([type, pool, boxList.split(',')[0].strip().strip('"')])
    dj = DeployJob(cmc, type, version, pool, boxList)
    dj.getTaskId()
    dj.getStatus()
    if all([x == 'success' for x in dj.checkStatus()]):
        logger.info("job is successful for " + server_info)
        sys.exit(0)
    elif any([x == 'cancel' for x in dj.checkStatus()]):
        logger.warning("job is canceled for " + server_info)
        sys.exit(1)
    elif any([x == 'create fail' for x in dj.checkStatus()]):
        logger.error("job create failed for " + server_info)
        sys.exit(2)
    else:
        logger.info("second job is running due to last job is failed for " + server_info)
        dj.getTaskId()
        sys.exit(3)


class MyThread(threading.Thread):
    def __init__(self, cmc, type, version, pool, boxList):
        # threading.Thread.__init__(self)
        super().__init__()
        self.cmc = cmc
        self.type = type
        self.version = version
        self.pool = pool
        self.boxList = boxList

    def run(self):
        main(self.cmc, self.type, self.version, self.pool, self.boxList)


if __name__ == "__main__":

    args = get_args()
    cmc_url = args.cmc_url
    mapping_file = args.mapping_file
    if cmc_url is None or mapping_file is None:
        logging.error("CMCULR and mapping file are needed!")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-8s %(levelname)-4s %(lineno)d %(threadName)s %(message)s',
                        # filename=os.path.join(tempfile.gettempdir(), mapping_file + '.log'),
                        filename=os.path.join(os.path.curdir, mapping_file + '.log'),
                        filemode='w')
    logger = logging.getLogger(__name__)
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.CRITICAL)
    logger.info("Job is Starting ...")
    threads = []
    fobj = open(os.path.abspath(os.path.basename(mapping_file)), 'r')
    for line in fobj.readlines():
        if not line.startswith('#') and line.strip('\n'):
            threads.append(MyThread(cmc_url, *line.split(',', 3)))

    fobj.close()

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    logger.info("Job is End ...")
