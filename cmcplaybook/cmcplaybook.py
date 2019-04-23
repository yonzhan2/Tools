import requests
import os
import time
import re
from multiprocessing import Pool, cpu_count

cmcurl = "csgcmc.qa.webex.com"
# cmcurl = "sjcmc.eng.webex.com"

###QA CMC headers
headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

###SJ CMC headers
#headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}
current_dir = os.path.dirname(__file__)
start = time.time()


def getpools():
    # url = 'https://%s/cmc/api/deploy/distIns/logstashagent/qa/?ignore_owner=yes' % cmcurl
    url = 'https://%s/cmc/api/deploy/distIns/appdjavaagent/qa/?ignore_owner=yes' % cmcurl
    session = requests.Session()
    session.headers = headers
    req = session.get(url)

    ret = req.json()[0].get('children')
    pools = [cld['name'] for child in ret for cld in child['children']]
    ### filter TA pools
    # pools = [pool for pool in pools if not re.search("ta|pj|pf|px|py|sd|bala", pool)]
    pools = [pool for pool in pools if re.search("hf|sz|ak", pool)]
    return pools


def generateconfig(poolname, service_version, build_no="0100"):
    url = 'https://%s/cmc/api/deploy/configuration/inherit/' % cmcurl
    data = {"service_name": "logstashagent", "pools[]": poolname, "ow_p": "1", "new_service_version": service_version,
            "new_build_no": build_no}
    req = requests.post(url, data=data, headers=headers)
    ret = req.json()
    time.sleep(2)
    if ret["result"] == "0000":
        return "Success on %s " % poolname
    else:
        return "Filure with %s " % ret + " on " + poolname


def deploywithplaybook(poolname, service_version, build_no="0100"):
    playbook = '''
component: appdjavaagent

variables:
  pool: %s
  version: %s-%s

tasks:

- name: "edit configuration for {{pool}}"
  action: Config
  pool: "{{pool}}" # if ignore this row, will use default
  versionBuild: "{{version}}" # if ignore this row, will use default
  changeStatus: approved
  override:
    mainService:
      #Pool: "{{configs/poolConfig.yml:poolConfig}}"
      Pool:
        Enable: "true"
- name: "deploy pool for {{pool}}"
  action: Deploy
  pool: "{{pool}}"                    # if ignore this row, will use default
  versionBuild: "{{version}}"         # if ignore this row, will use default 
  #taskType: service_refresh
  additional:
      configuration: true
      service: false
      package: false   
  #boxTypeList:
  #  - provisioner
  #boxList:
   # - name: cfgszpri101 
  user:
    yonzhan2

    ''' % (poolname, service_version, build_no)

    url = "https://%s/cmc/api/playbook/" % cmcurl
    filename = os.path.join(current_dir, 'logstashagent/configs/logstashagentplaybook_%s.yml' % poolname)
    with open(filename, 'w+') as f:
        f.write(playbook)
    time.sleep(5)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    os.remove(filename)
    return req.text


if __name__ == "__main__":
    pool = Pool(cpu_count())
    result = []
    service_version = "4.5.6.24621"
    build_no = "0003"
    for pname in getpools():
        # print("Generate config for %s " % pname)
        # generateconfig(pname, service_version, build_no)
        print("Deploy pool for %s " % pname)
        result.append(pool.apply_async(func=deploywithplaybook, args=(pname, service_version, build_no,)))

    pool.close()
    pool.join()

    for res in result:
        print('***:', res.get())

    end = time.time()
    print("Total run time: %s " % (end - start))
