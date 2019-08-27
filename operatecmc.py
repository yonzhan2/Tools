import requests
import pymongo
import json
import sys
import time
import re
import os

CMCURL_MAPPING = {"QA": {"URL": "csgcmc.qa.webex.com",
                         "KEY": "Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4="},
                  "DMZ": {"URL": "sjcmc.dmz.webex.com",
                          "KEY": "Q01DQVBJX0RNWjo5M2IyOGNiNzQ4NjM0YmJmYTI4YWZkNWVhODQ2NGY3Mg=="},
                  "ENG": {"URL": "sjcmc.eng.webex.com",
                          "KEY": "Q01DUUFfQVBJX0hGTEFCX2tleTozZmJmYTkwNWZiODQ0ODZjOGVkNzg0MTcyYzFjNDE4NA=="}
                  }
ordered_boxlist = []
tahoe_taskid_list = []
current_dir = os.path.dirname(__file__)


class MongoDB:
    def __init__(self, component, env):
        self.component = component.lower()
        self.env = env.upper()
        self.MONGODB = "173.36.203.62"
        self.client = pymongo.MongoClient("mongodb://{0}:2701/".format(self.MONGODB))
        self.mydb = self.client["envmapping"]
        self.mycoll = self.mydb["map"]

    def getpoolinfo(self):
        try:
            myquery = {"component": self.component, "env": self.env}
            ret = self.mycoll.find_one(myquery)
            pool, filtertype = ret.get('pool'), ret.get('filtertype')
            return pool, filtertype
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))

    def getgdmpoolinfo(self):
        try:
            myquery = {"component": self.component, "env": self.env}
            ret = self.mycoll.find_one(myquery)
            gdmpool = ret.get('gdmpool')
            return gdmpool
        except Exception as e:
            print(("Error %d: %s" % (e.args[0], e.args[1])))


class BatchTool:
    def __init__(self, component, env):
        self.component = component.lower()
        self.env = env.upper()
        self.cmcurl = CMCURL_MAPPING.get(self.env).get("URL")
        self.key = CMCURL_MAPPING.get(self.env).get("KEY")
        self.headers = dict(Authorization=f"Basic {self.key}")
        self.request_url = f"https://{self.cmcurl}/cmc/api/deploy/pool/request/"
        self.taskurl = f"https://{self.cmcurl}/cmc/api/deploy/task/"
        self.playbook_url = f"https://{self.cmcurl}/cmc/api/playbook/"
        self.pool = MongoDB(self.component, self.env).getpoolinfo()[0]
        self.filtertype = MongoDB(self.component, self.env).getpoolinfo()[1]
        self.gdmpool = MongoDB(self.component, self.env).getgdmpoolinfo()

    def getserverbypool(self, pool=None):
        if pool is None:
            pool = self.pool
        box_url = 'https://%s/cmc/api/sitBoxList/%s/?pool=%s&ignore_owner=yes' % (self.cmcurl, self.component, pool)
        req = requests.get(box_url, headers=self.headers)
        ret = req.json().get('rows')
        servers = [server.get('name') for server in ret if server.get('type') in self.filtertype]
        return servers

    def getcmcversionbypool(self, pool=None):
        if pool is None:
            pool = self.pool
        box_url = 'https://%s/cmc/api/sitBoxList/%s/?pool=%s&ignore_owner=yes' % (self.cmcurl, self.component, pool)
        req = requests.get(box_url, headers=self.headers)
        # print(req.content)
        ret = req.json().get('rows')
        servers_version_mapping = [{server.get('name'): server.get('version') + '-' + server.get('build')} for server in
                                   ret if server.get('type') in self.filtertype]
        return servers_version_mapping

    def getgdmserver(self):
        if self.gdmpool:
            print("Has GDM")
            for gdm in self.gdmpool.split(","):
                boxlist = self.getserverbypool(gdm)
                gdm_boxlist = [{"name": box} for box in boxlist]
                yield gdm_boxlist

    def getStatus(self, taskId):
        if not taskId:
            sys.stderr.write("Error: taskId is null,exit ...")
            sys.exit()
        try:
            req = requests.get(self.taskurl + str(taskId) + '/', headers=self.headers)
            ret = [status['status'] for status in json.loads(req.content)['poolList'][0]['boxList']]
            # print("ret is", ret)
            return ret
        except Exception as e:
            print(f"Error of getStatus {e}")

    def checkStatus(self, taskId):
        status = self.getStatus(taskId)
        while True:
            time.sleep(1)
            print(f"This taskId {taskId} status is {str(status)}")
            if all([x == 'success' for x in status]) or 'cancel' in status or 'time out' in status:
                break
            elif 'fail' in status and 'in progress' not in status:
                break
            else:
                status = self.getStatus(taskId)
        if all([x == 'success' for x in status]):
            return True
        return

    def execute_action_script(self, pool=None, script_name="Maintain", **kwargs):
        if pool is None:
            pool = self.pool
        boxlist = self.getserverbypool(pool)
        print(boxlist)
        if kwargs.get("boxtype"):
            boxlist_format = [{"name": box} for box in boxlist if re.search(kwargs.get("boxtype"), box)]
            print(boxlist_format)
        else:
            boxlist_format = [{"name": box} for box in boxlist]
        data = {"serviceName": self.component, "taskType": "action_script", "user": "yonzhan2",
                "additional": {"action_name": script_name}, "poolList": [{"name": pool, "boxList": boxlist_format}]}
        data = json.dumps(data)
        print(data)
        res = requests.get(self.request_url, data=data, headers=self.headers)
        taskId = json.loads(res.content)['taskId']
        # print(taskId)
        if self.checkStatus(taskId):
            return True

    def gettahoebox(self, pool=None):
        if pool is None:
            pool = self.pool
        boxlist = self.getserverbypool(pool)

        if self.filtertype == "tssrv,tassrv,tccsrv":
            for type in "ts0,as0,cc0".split(","):
                filter_boxlist = [box for box in boxlist if re.search(type, box)]
                print(filter_boxlist)
                if len(filter_boxlist) >= 2:
                    for sbox in reversed(filter_boxlist):
                        ordered_boxlist.append(sbox)
        return

    def post_action_service(self, pool, boxlist_format, **kwargs):
        if pool is None:
            pool = self.pool
        if kwargs.get("boxtype"):
            boxlist_format = [box for box in boxlist_format if re.search(kwargs.get("boxtype"), box.get("name"))]
        action = kwargs.get("action")
        data = {"serviceName": self.component, "taskType": "service_" + action, "user": "yonzhan2", "additional": {},
                "poolList": [{"name": pool, "boxList": boxlist_format}]}
        data = json.dumps(data)
        # print(data)

        res = requests.get(self.request_url, data=data, headers=self.headers)
        taskId = json.loads(res.content)['taskId']
        if self.checkStatus(taskId):
            # Spark.SparkBot(bot_app_name, spark_bot_token=spark_token,spark_bot_url=bot_url, spark_bot_email=bot_email).send_msg(f"{action} success at {boxlist_format}.")
            return True

    def stop_service(self, pool=None, **kwargs):
        if pool is None:
            pool = self.pool
        boxlist = self.getserverbypool(pool)
        boxlist_format = [{"name": box} for box in boxlist]
        print(f"boxlist format is {boxlist_format}")

        if self.component == "tahoe":
            _ = self.gettahoebox()
            print(f"ordered_boxlist is {ordered_boxlist}")
            for boxlist in ordered_boxlist:
                boxlist_format = [{"name": box} for box in [boxlist]]
                print(boxlist_format)
                if self.post_action_service(pool=None, boxlist_format=boxlist_format, action="stop"):
                    tahoe_taskid_list.append(True)
                    # Spark.SparkBot(bot_app_name, spark_bot_token=spark_token,spark_bot_url=bot_url, spark_bot_email=bot_email).send_msg(f"{boxlist} was stopped success.")
                    if re.search('ts0', boxlist):
                        time.sleep(180)
                    else:
                        time.sleep(90)
            if all(tahoe_taskid_list):
                return True
        elif self.component == "mmp":
            "Suspend Local MCC"
            if self.execute_action_script(script_name="Suspend", boxtype="mcc"):
                print(f"Suspend MCC for local {pool} pool")

            "Stop GDM MCS if has"
            if self.gdmpool:
                print("Has GDM")
                for gdm in self.gdmpool.split(","):
                    boxlist = self.getserverbypool(gdm)
                    gdm_boxlist = [{"name": box} for box in boxlist]
                    if self.post_action_service(gdm, boxlist_format=gdm_boxlist, action="stop"):
                        print(f"GDM pool {gdm} was stopped.")
                        time.sleep(10)
            else:
                print("No GDM")

            "Stop Local MCS"
            if self.post_action_service(pool=None, boxlist_format=boxlist_format, boxtype="mcs", action="stop"):
                print(f"Stopped MCS for local {pool} pool")
                time.sleep(60)

            "Stop Local MCC"
            if self.post_action_service(pool=None, boxlist_format=boxlist_format, boxtype="mcc", action="stop"):
                print(f"Stopped MCC for local {pool} pool")

        else:
            if self.post_action_service(pool, boxlist_format):
                return True

    def start_service(self, pool=None, **kwargs):
        if pool is None:
            pool = self.pool
        boxlist = self.getserverbypool(pool)
        boxlist_format = [{"name": box} for box in boxlist]
        if self.component == "mmp":
            "Start local mcc"
            self.post_action_service(pool=None, boxlist_format=boxlist_format, boxtype="mcc", action="start")
            "Start local mcs"
            self.post_action_service(pool=None, boxlist_format=boxlist_format, boxtype="mcs", action="start")

            "Start GDM MCS"
            if self.gdmpool:
                print("Has GDM")
                for gdm in self.gdmpool.split(","):
                    boxlist = self.getserverbypool(gdm)
                    gdm_boxlist = [{"name": box} for box in boxlist]
                    if self.post_action_service(gdm, boxlist_format=gdm_boxlist, action="start"):
                        print(f"Start GDM MCS for {gdm} pool.")

            "Resume Local MCC"
            if self.execute_action_script(script_name="Resume", boxtype="mcc"):
                print(f"Resume MCC for local {pool} pool")
            return True
        else:
            if self.post_action_service(pool=None, boxlist_format=boxlist_format, action="start"):
                return True

    def deploywithplaybook(self, pool, box=None, service_version=None, ):

        servers = self.getserverbypool(pool)
        box = [server for server in servers if re.search(box, server)]
        # print(f"box is {box}")
        if not service_version:
            servers_version_mapping = self.getcmcversionbypool(pool)
            service_version = [server.get(box[0]) for server in servers_version_mapping if server.get(box[0])][0]
        else:
            service_version = '-'.join(service_version.split(':'))

        if pool is None:
            pool = self.pool
        if box:
            box_list = '\n  '.join([f"    - name: {b}" for b in box])
        else:
            box_list = "    - name:"

        playbook = '''
component: %s
variables:
  pool: %s
  version: %s
tasks:
- name: "edit configuration for {{pool}}"
  action: Config
  pool: "{{pool}}" # if ignore this row, will use default
  versionBuild: "{{version}}" # if ignore this row, will use default
  changeStatus: approved
  # override:
  #   mainService:
  #     #Pool: "{{configs/poolConfig.yml:poolConfig}}"
  #     Pool:
  #       Enable: "true"
- name: "deploy pool for {{pool}}"
  action: Deploy
  pool: "{{pool}}"                    # if ignore this row, will use default
  versionBuild: "{{version}}"         # if ignore this row, will use default 
  taskType: service_refresh
  additional:
      configuration: false
      service: true
      package: false   
  boxList:
  %s
  user:
    yonzhan2
    ''' % (self.component, pool, service_version, box_list)

        filename = os.path.join(current_dir, '%s_playbook_%s.yml' % (self.component, pool))
        with open(filename, 'w+') as f:
            f.write(playbook)
        time.sleep(2)
        files = {'playbook': open(filename, 'rb')}
        res = requests.post(self.playbook_url, files=files, headers=self.headers)
        os.remove(filename)
        if res.status_code != 200:
            print(res.content)
            exit(1)
        time.sleep(5)
        content = json.loads(res.content)
        if content.get("result") != "0000":
            raise Exception(content.get("resultInfo"))
        time.sleep(5)
        pid = content.get("resultInfo").get("playbookId")
        _cache, action_index = [], 0
        while True:
            res = requests.get(self.playbook_url + "?pid=%s" % pid, headers=self.headers)
            if res.status_code != 200:
                raise Exception(res.content)
            content = json.loads(res.content)
            task_list = content.get("resultInfo", [])
            print(f"task_list is {task_list}")
            status = [task.get('status') for task in task_list]
            status = [True if s == 'success' else False for s in status]
            if all(status):
                return True
            if action_index == len(task_list):
                break
            tsk = task_list[action_index]
            result = tsk['result']
            if result:
                try:
                    result = json.dumps(tsk['result'], indent=4)
                except Exception as e:
                    pass
            if tsk['status'] not in ["created", "in progress"]:
                action_index += 1
                continue
            time.sleep(10)


if __name__ == '__main__':
    bt = BatchTool('tahoe', 'qa')
    # print(bt.getpoolinfo())
    # print(bt.getgdmpoolinfo())
    # bt.stop_service()
    # bt.start_service()
    # bt.maintain_service()
    #
    # md = MongoDB('mmp','dmz')
    # md.getpoolinfo()
    # print(bt.getcmcversionbypool('t02fa'))
    print(bt.deploywithplaybook('t02fa', box='as'))
