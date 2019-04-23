import requests
import os

# cmcurl = "csgcmc.qa.webex.com"
cmcurl = "sjcmc.eng.webex.com"

###QA CMC headers
# headers = {'Authorization': 'Basic Q01DUUFfQVBJX0hGQ0lfa2V5OjdlMGRhNmU4ODk1MzRkMjQ4N2IwZjI4MzQ0OWIwM2Q4='}

###SJ CMC headers
headers = {'Authorization': 'Basic Q01DVVNBUElfa2V5OjQ4ZGJkZDcwNjkzNzRjMzhhMGMyNGIyMTcxMWQzYTA2'}

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
  - name: tsb1cms003
    ip: 192.168.163.68
    boxType: cmssvr
  - name: tsb1cms004
    ip: 192.168.163.69
    boxType: cmssvr                         
    ''' % (component, poolname, service_version, build_no)

    url = "https://%s/cmc/api/playbook/" % cmcurl
    filename = os.path.join(current_dir, 'playbook_%s.yml' % poolname)
    with open(filename, 'w+') as f:
        f.write(playbook)
    files = {'playbook': open(filename, 'rb')}
    req = requests.post(url, files=files, headers=headers)
    # os.remove(filename)
    print(req.text)


if __name__ == "__main__":
    registerbox('cms', 'tsb1', '3.1.0', '1515')
