#!/usr/bin/env python
import glob
import os
import re
import time

version = glob.glob('/www/htdocs/client/WBXclient-*')
versionlist = set()
[versionlist.add(ver.split('/')[-1].split('-')[1]) for ver in version]
print(versionlist)


def getduration(version):
    now = time.time()
    mtime = os.stat(version).st_mtime
    duration = now - mtime
    return duration / (60 * 60 * 24)


for ver in versionlist:
    tmp = sorted(glob.glob('/www/htdocs/client/WBXclient-' + ver + '-*'), key=lambda x: int(x.split('-')[-1]))
    removelist = tmp[:len(tmp) - 3]
    leftversionlist = tmp[-3:]

    if len(removelist) > 0:
        try:
            for rem in removelist:
                print("Removing client " + rem + " ...")
                os.system("rm -rf " + rem)
        except OSError as e:
            pass

    if len(leftversionlist) > 0:
        try:
            for rem in leftversionlist:
                if re.search(r'WBXclient-\d+\.\d+\.\d+\.\w+-\d+', rem) and getduration(rem) > 31:
                    print("Removing expired client " + rem + "...")
                    os.system("rm -rf " + rem)
        except OSError as e:
            pass
