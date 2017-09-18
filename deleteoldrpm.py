import os
import time
from subprocess import PIPE, Popen


class RemoveOldRpm():
    def __init__(self):
        pass

    def getProdRpms(self, name, type):
        self.prodlist = []
        proddir = '/opt/webex/prodlist'
        URL = "https://rmc.webex.com/api/files/more/bts/%s/%s?minutes=%s" % (name, type, 2 * 360 * 1440)
        ProdListTemp = "%s/%s.%s.temp" % (proddir, name, type)
        ProdList = "%s/%s.%s" % (proddir, name, type)
        CMD = ''' curl -u "rmc_app_access_key:5c05382eee0e43728e0af0f8c11aa338" -s -o %s %s 2>/dev/null''' % (
        ProdListTemp, URL)
        p = Popen(CMD, shell=True)
        p.wait()
        time.sleep(1)
        p = Popen('''awk -F '|' '{print $1}' %s | awk -F':' {'print $2'} > %s''' % (ProdListTemp, ProdList), shell=True)
        with open(ProdList, 'r') as f:
            for rpm in f:
                self.prodlist.append(rpm.strip())
        print self.prodlist


if __name__ == "__main__":
    ror = RemoveOldRpm()
    ror.getProdRpms('j2ee', 'noarch')
