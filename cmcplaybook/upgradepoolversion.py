import requests
import os
import time
from multiprocessing import Pool, Manager, cpu_count
from yaml import load

CMCURL_MAPPING = {"QA": {"URL": "csgcmc.qa.webex.com",
                         "KEY": "Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4="},
                  "DMZ": {"URL": "sjcmc.dmz.webex.com",
                          "KEY": "Q01DQVBJX0RNWjo5M2IyOGNiNzQ4NjM0YmJmYTI4YWZkNWVhODQ2NGY3Mg=="},
                  "ENG": {"URL": "sjcmc.eng.webex.com",
                          "KEY": "Q01DQVBJX0VOR19rZXk6YmFkMGE4MjQ3Zjg0NGVkMWE0ZmQ2MzlhNTcwNzM5Y2I="}
                  }

# env = "qa"
env = "dmz"

cmcurl = CMCURL_MAPPING.get(env.upper()).get("URL")
headers = {'Authorization': f'Basic {CMCURL_MAPPING.get(env.upper()).get("KEY")}'}

current_dir = os.path.dirname(__file__)
start = time.time()


class GetData:
    def __init__(self, cmcmapping_file):
        self.pool_data = load(open(cmcmapping_file))
        self.version_data = load(open('cmcversion.yml'))
        self.pool_component = self.pool_data.get('component')
        self.version_component = self.version_data.get('component')

    def getcomponent(self):
        component_name = [name for name in self.pool_component.keys()]
        return component_name

    def getpool(self, component):
        pools = self.pool_component.get(component).get('pools')
        #pools = [pool for pool in pools if  re.search("hf|sz|ak", pool)]
        return pools

    def getversion(self, component):
        version = self.version_component.get(component).get('version')
        return version


def generateconfig(component, poolname, service_version, build_no="0100"):
    url = 'https://%s/cmc/api/deploy/configuration/inherit/' % cmcurl
    data = {"service_name": component, "pools[]": poolname, "ow_p": "0", "new_service_version": service_version,
            "new_build_no": build_no}
    req = requests.post(url, data=data, headers=headers)
    ret = req.json()
    # print(ret,component,poolname)
    time.sleep(1)
    if ret["result"] == "0000":
        return "Success on %s-%s " % (component, poolname)
    else:
        return "Filure with %s-%s " % ret + " on " + (component, poolname)


def upgradewithplaybook(component, poolname, service_version, build_no="0100", boxlist=''):
    if boxlist:
        namelist = ''.join(["    - name: %s \n" % name for name in boxlist])
        print(namelist)

    else:
        namelist = "    #- name: "

    playbook = '''
component: %s

variables:
  pool: %s
  
  version: %s-%s

tasks:

# - name: "edit configuration for {{pool}}"
#   action: Config
#   pool: "{{pool}}" # if ignore this row, will use default
#   versionBuild: "{{version}}" # if ignore this row, will use default
#   changeStatus: approved
#   override:
#     mainService:
#       #Pool: "{{configs/poolConfig.yml:poolConfig}}"
#       Pool:
#         EnableLog: "true"

- name: "deploy pool for {{pool}}"
  action: Deploy
  pool: "{{pool}}"                    # if ignore this row, will use default
  versionBuild: "{{version}}"         # if ignore this row, will use default
  #taskType: service_refresh
  additional:
      configuration: true
      service: true
      package: true
  #boxTypeList:
  #  - provisioner
  boxList:
%s
  user:
    yonzhan2 

    ''' % (component, poolname, service_version, build_no, namelist)

    url = "https://%s/cmc/api/playbook/" % cmcurl
    filename = os.path.join(current_dir, '%s_%s.yml' % (component, poolname))
    with open(filename, 'w+') as f:
        f.write(playbook)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    os.remove(filename)
    return req.text


def upgrade_task(workqueue, index):
    process_id = "Process-" + str(index)
    while not workqueue.empty():
        print(f"qsize is {workQueue.qsize()}")
        parameter_split = workQueue.get(timeout=2)
        print(f"get parameters {parameter_split}")
        try:
            component_name, pname, service_version, build_no = parameter_split.split('-')
            print("Generate config for %s-%s " % (component_name, pname))
            generateconfig(component_name, pname, service_version, build_no)
            print("Deploy pool for %s-%s " % (component_name, pname))
            upgradewithplaybook(component_name, pname, service_version, build_no)
            print(process_id, workqueue.qsize(), parameter_split)
        except Exception as e:
            print(process_id, workqueue.qsize(), parameter_split, "Error happened", e)


if __name__ == "__main__":
    getdata = GetData(f'cmcmapping_{env}.yml')
    print(getdata.pool_component)
    result = []

    manager = Manager()
    workQueue = manager.Queue(1000)

    for component_name in getdata.getcomponent():

        service_version, build_no = getdata.getversion(component_name).split(':')
        print(component_name, service_version, build_no)

        for pname in getdata.getpool(component_name):
            pool = Pool(cpu_count() - 1)

            print("Generate config for %s-%s " % (component_name, pname))
            generateconfig(component_name, pname, service_version, build_no)
            print("Deploy pool for %s-%s " % (component_name, pname))
            result.append(
                pool.apply_async(func=upgradewithplaybook, args=(component_name, pname, service_version, build_no)))

        pool.close()
        pool.join()

    for res in result:
        print('***:', res.get())

    end = time.time()
    print("Total run time: %s " % (end - start))