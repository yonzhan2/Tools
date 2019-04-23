import urllib2
import base64
import json

username = "admin"
password = "@,=*[[&<8_&.8~<@"


def getservergroups():
    request = urllib2.Request("http://127.0.0.1:3004/cloudproxy/v1/config/sipServerGroup")
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)

    data = json.load(response)
    servergroups = [sg["serverGroupName"] for sg in data]
    return servergroups


def getsubsg(sg_name):
    request = urllib2.Request("http://127.0.0.1:3004/cloudproxy/v1/runtime/sipServerGroup/status/" + sg_name)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    response = urllib2.urlopen(request)

    data = json.load(response)
    print(sg_name, data["runtime"][0]["serverGroupStatus"]["status"])


for sg in getservergroups():
    getsubsg(sg)
