import requests
import os

cmcurl = "csgcmc.qa.webex.com"
# cmcurl = "sjcmc.eng.webex.com"

###QA CMC headers
headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

###SJ CMC headers
#headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}

current_dir = os.path.dirname(__file__)


def registerbox(component, poolname, service_version, build_no="0000"):
    playbook = '''component: %s

variables:
  pool: %s
  version: %s-%s

tasks:

- name: "register box in {{pool}}"
  action: RegisterBox
  pool: "{{pool}}"
  versionBuild: "{{version}}"
  boxList:
  - name: clhf3esc001
    ip: 10.224.89.13
    boxType: escsvr
  - name: clhf3esc002
    ip: 10.224.89.14
    boxType: escsvr  
  - name: clhf3esd001
    ip: 10.224.89.15
    boxType: esdsvr    
  - name: clhf3esd002
    ip: 10.224.89.16
    boxType: esdsvr    
  - name: clhf3esd003
    ip: 10.224.89.17
    boxType: esdsvr    
  - name: clhf3esm001
    ip: 10.224.89.18
    boxType: esmsvr                                           
    ''' % (component, poolname, service_version, build_no)

    url = "https://%s/cmc/api/playbook/" % cmcurl
    filename = os.path.join(current_dir, 'playbook_%s.yml' % poolname)
    with open(filename, 'w+') as f:
        f.write(playbook)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    os.remove(filename)
    print(req.text)


if __name__ == "__main__":
    registerbox('esaas', 'clhf3', '6.5.4', '1901')
