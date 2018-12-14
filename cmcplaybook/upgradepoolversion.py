import requests
import os
import time
from multiprocessing import Pool, cpu_count
from yaml import load

# cmcurl = "csgcmc.qa.webex.com"
cmcurl = "sjcmc.eng.webex.com"

###QA CMC headers
# headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

###SJ CMC headers
headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}
current_dir = os.path.dirname(__file__)
start = time.time()


class GetData():
    def __init__(self):
        self.data = load(open('cmcmaping_dmz.yml'))
        self.component = self.data.get('component')

    def getcomponent(self):
        component_name = [name for name in self.component.keys()]
        return component_name

    def getpool(self, component):
        pools = self.component.get(component).get('pools')
        return pools

    def getversion(self, component):
        version = self.component.get(component).get('version')
        return version


def generateconfig(component, poolname, service_version, build_no="0100"):
    url = 'https://%s/cmc/api/deploy/configuration/inherit/' % cmcurl
    data = {"service_name": component, "pools[]": poolname, "ow_p": "0", "new_service_version": service_version,
            "new_build_no": build_no}
    req = requests.post(url, data=data, headers=headers)
    ret = req.json()
    # print(ret,component,poolname)
    time.sleep(5)
    if ret["result"] == "0000":
        return "Success on %s-%s " % (component, poolname)
    else:
        return "Filure with %s-%s " % ret + " on " + (component, poolname)


def deploywithplaybook(component, poolname, service_version, build_no="0100", boxlist=''):
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
    time.sleep(10)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    # os.remove(filename)
    return req.text


if __name__ == "__main__":
    getdata = GetData()
    print(getdata.component)
    result = []
    for component_name in getdata.getcomponent():

        service_version, build_no = getdata.getversion(component_name).split('-')
        print(component_name, service_version, build_no)

        for pname in getdata.getpool(component_name):
            pool = Pool(cpu_count())

            print("Generate config for %s-%s " % (component_name, pname))
            generateconfig(component_name, pname, service_version, build_no)
            print("Deploy pool for %s-%s " % (component_name, pname))
            result.append(
                pool.apply_async(func=deploywithplaybook, args=(component_name, pname, service_version, build_no)))

        pool.close()
        pool.join()

    for res in result:
        print('***:', res.get())

    end = time.time()
    print("Total run time: %s " % (end - start))
