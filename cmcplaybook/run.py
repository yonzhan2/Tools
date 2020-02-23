# -*- coding: utf-8 -*-
try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3
import json
import os, zipfile

import requests
import time
from prettytable import PrettyTable

url = "https://sjcmc.eng.webex.com/cmc/api/playbook/"
playbook_dir = "logstashagent/"
headers = {
    "Authorization": "Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2"
}

current_dir = os.path.dirname(__file__)
playbook_full_path = os.path.join(current_dir, playbook_dir)


def create_zip():
    ss = StringIO.StringIO()
    memeryZip = zipfile.ZipFile(ss, "a", zipfile.ZIP_DEFLATED, False)
    files = []

    def get_files(path):
        file_list = os.listdir(path)
        for file in file_list:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                get_files(filepath)
            else:
                files.append(filepath)

    get_files(playbook_full_path)
    for file_full_name in files:
        with open(file_full_name) as op:
            t = op.read()
            tmp_paths = file_full_name.split(playbook_full_path)
            name = tmp_paths[1]
            memeryZip.writestr(name, t.encode("utf-8"))
    memeryZip.close()
    ss.seek(0)
    data = ss.read()
    ss.close()
    return data


def send(data):
    print "Info: request sending....."
    # res = requests.post(url, headers=headers, files={"playbook": ("cmcplaybook.yml", data)})
    res = requests.post(url, headers=headers, files={"playbook": ("cmcConfig.zip", data)})
    if res.status_code != 200:
        print res.content
        exit(1)
    print "Info: request send success."
    time.sleep(5)
    content = json.loads(res.content)
    if content.get("result") != "0000":
        raise Exception(content.get("resultInfo"))
    print "Info: tasks executing details:"
    time.sleep(5)
    pid = content.get("resultInfo").get("playbookId")
    t = PrettyTable(["Action", "Name", "Status", "Result"])
    t.align = 'l'
    _cache, action_index = [], 0
    while True:
        res = requests.get(url + "?pid=%s" % pid, headers=headers)
        if res.status_code != 200:
            raise Exception(res.content)
        content = json.loads(res.content)
        summary = content.get("summary")
        task_list = content.get("resultInfo", [])
        if action_index == len(task_list):
            print "Summary:"
            print json.dumps(summary, indent=4)
            print "execute finished."
            break
        tsk = task_list[action_index]
        result = tsk['result']
        if result:
            try:
                result = json.dumps(tsk['result'], indent=4)
            except:
                pass
        t.add_row(
            [tsk["action"],
             tsk['name'],
             tsk['status'],
             result]
        )
        print t.get_string(header=False)
        t.clear_rows()
        if tsk['status'] not in ["created", "in progress"]:
            action_index += 1
            print t.get_string(header=False)
            t.clear_rows()
            continue
        time.sleep(10)


data = create_zip()
# f = "FullRefresh.yml"
# ymlwith open(playbook_full_path + "/" + f) as t:
# data = t.read()
send(data)
