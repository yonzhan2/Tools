
#!/usr/bin/env python
import glob
import os
import re
import time
from subprocess import Popen, PIPE

cmd = "find /www/htdocs/client/ -maxdepth 1 -type l -ls|awk '{print $11}'"

version = glob.glob('/www/htdocs/client/WBXclient-*')
versionlist = set()
[versionlist.add(ver.split('/')[-1].split('-')[1]) for ver in version]
print(versionlist)
linkedlist = []


def getlinkedlist():
    output, stderr = Popen(cmd, stdout=PIPE, shell=True).communicate()
    ret = output.decode('utf-8').split("\n")
    ret.remove("")
    print(ret)
    for link in ret:
        if os.path.realpath(link) and os.path.exists(link):
            linkedlist.append(os.path.realpath(link))

def getduration(version):
    now = time.time()
    mtime = os.stat(version).st_mtime
    duration = now - mtime
    return duration / (60 * 60 * 24)


getlinkedlist()
print("linkedlist is {0}".format(linkedlist))

for ver in versionlist:
    tmp = sorted(glob.glob('/www/htdocs/client/WBXclient-' + ver + '-*'), key=lambda x: int(x.split('-')[-1]))
    removelist = tmp[:len(tmp) - 3]
    leftversionlist = tmp[-3:]
    print("tmp list is %s" % tmp)
    print("removelist is %s" % removelist)
    print("leftversion is %s" % leftversionlist)

    if len(leftversionlist) > 0:
        try:
            for rem in leftversionlist:
                # if re.search(r'WBXclient-\d+\.\d+\.\d+\.\w+-\d+',rem) and getduration(rem) > 31:
                if re.search(r'WBXclient-\d+\.\d+\.\d+-\d+', rem) and getduration(rem) > 180:
                    print("Removing expired client " + rem + "...")
                    os.system("rm -rf " + rem)
        except OSError as e:
            pass

    if len(removelist) > 0:
        try:
            for rem in removelist:
                if rem not in linkedlist:
                    print("Removing client " + rem + " ...")
                    os.system("rm -rf " + rem)
                else:
                    print("{0} was linked, ignore this ...".format(rem))
        except OSError as e:
            pass

os.system("find /www/htdocs/client/ -type l -exec test ! -e {} \; -print|xargs rm -f")
