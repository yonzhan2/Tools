import ConfigParser
import os
import requests
import telnetlib

cf = ConfigParser.ConfigParser()
cf.read(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'hckconfig.properties')
secs = cf.sections()
# print secs
status = {'DPL': 'OKOKOK'}


class HealthCheck:
    "get the server's health check status via the parameter input"
    x = 1

    def __init__(self, type):
        self.type = type
        self.ip, self.rpmcmd, self.hckurl = (cf.get(type, opt) for opt in cf.options(type))
        self.statustatus = {}

    def getStatus(self):
        try:
            data = requests.get(self.hckurl)
            # print data.status_code
            if data.status_code == 200:
                status[self.type] = 'OKOKOK'
                # print 'status is %s' % self.status
                return "OKOKOK"

        except:
            status[self.type] = 'NONONO'
            # print 'status is %s' % self.status
            return "NONONO"

    def Telnet(self):
        try:
            tn = telnetlib.Telnet(self.ip, self.hckurl)
            status[self.type] = 'OKOKOK'
            return 'OKOKOK'
        except:
            status[self.type] = 'NONONO'
            return 'NONONO'


for type in secs:
    hck = HealthCheck(type)
    # print hck.ip,hck.rpmcmd,hck.hckurl
    print type, hck.ip, hck.getStatus()
print 'url status is %s' % status

for type in 'TahoeTS', 'WebACD':
    hck = HealthCheck(type)
    # print hck.ip,hck.rpmcmd,hck.hckurl
    print type, hck.ip, hck.Telnet()
print 'telnet status is %s' % status

try:
    data = requests.get('http://szmrs.qa.webex.com/meeting-registry/api/v1/ping1').content

    m_okokok = re.compile('OKOKOK', re.I)
    m_online = re.compile('online', re.I)
    if m_okokok.search(data) or m_online.search(data):
        print "OKOKOK"
    else:
        print 'NONONO'
except:
    print 'EXCEPT NONONO'
