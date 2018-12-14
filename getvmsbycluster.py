#!/usr/bin/env python
"""
Written by Chris Hupman
Github: https://github.com/chupman/
Example: Get guest info with folder and host placement

"""
from __future__ import print_function

from pyVmomi import vim, vmodl

from pyVim.connect import SmartConnectNoSSL, Disconnect

import argparse
import atexit
import getpass
import json
import csv
import xlwt
# import openpyxl
import pymysql  # MySQLdb
import requests


# from collections import defaultdict


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host')
    parser.add_argument('--json', required=False, action='store_true',
                        help='Write out to json file')
    parser.add_argument('--jsonfile', required=False, action='store',
                        default='getvmsbycluster.json',
                        help='Filename and path of json file')
    parser.add_argument('--silent', required=False, action='store_true',
                        help='supress output to screen')
    args = parser.parse_args()
    return args


def vmsummary(vm):
    ip = vm.summary.guest.ipAddress
    vmstat = vm.summary.runtime.powerState
    vmpath = vm.summary.config.vmPathName
    vmmacc = 'N/A'
    try:
        if hasattr(vm.config, 'hardware'):
            for dev in vm.config.hardware.device:
                if hasattr(dev, 'macAddress'):
                    vmmacc = dev.macAddress
                continue
            return ip, vmmacc, vmstat, vmpath
        else:
            return 'N/A', 'N/A', 'N/A', 'N/A'

    except Exception as e:
        print(vm.summary.config.name, vmpath, e)


class DBOperation:
    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        try:
            self.database = pymysql.connect(self.host, self.user, self.passwd, self.db)
        except Exception as e:
            print(e)
        self.cursor = self.database.cursor()

    def precreation(self):

        vcinfo_table = '''
                        CREATE TABLE IF NOT EXISTS `vcinfo`(
                        `vcdns` VARCHAR(40) ,
                        `vcname` VARCHAR(20) ,
                        PRIMARY KEY ( `vcdns` )
                        ) DEFAULT CHARSET=utf8;'''

        vmlist_table = '''
                        CREATE TABLE IF NOT EXISTS `vmlist`(
                        `vmid` INT UNSIGNED AUTO_INCREMENT,
                        `vcname` VARCHAR(40) ,
                        `dcname` VARCHAR(20) ,
                        `cluster` VARCHAR(40) ,
                        `hostip` VARCHAR(40) ,
                        `vmname` VARCHAR(60) NOT NULL,
                        `vmip` VARCHAR(20) ,   
                        `vmmacc` VARCHAR(40) , 
                        `status` VARCHAR(40) , 
                        `vmpath` VARCHAR(120) , 
                        PRIMARY KEY ( `vmid` )
                        )   DEFAULT CHARSET=utf8
                        '''
        unique_index = '''create unique index idx_vmname_macc on vmlist(vmname,vmmacc)'''
        second_index = '''create index idx_dcname_cluster on vmlist(dcname,cluster)'''

        try:
            self.cursor.execute(vcinfo_table)
            self.cursor.execute(vmlist_table)
            self.cursor.execute(unique_index)
            self.cursor.execute(second_index)
            self.database.commit()
        except Exception as e:
            print('preCreation', e)

    def getVCName(self, vcdns):
        sql = "SELECT VCNAME FROM vminfo_vcinfo WHERE vcdns = '%s'" % (vcdns)
        try:
            self.cursor.execute(sql)
            vcname = self.cursor.fetchone()[0]
            return vcname
        except Exception as e:
            print('getVCname', e)

    def query(self, vmname, vmmacc):
        sql = "SELECT COUNT(1) FROM vminfo_vmlist where vmname = %s and vmmacc = %s ", (vmname, vmmacc)
        try:
            count = self.cursor.execute(*sql)
            if count > 0:
                return True
        except Exception as e:
            print('query', e)

    def insert(self, vcname, dc, cluster, hostname, vmname, vmip, vmmacc, vmstat, vmpath):
        _del_sql = "DELETE FROM vminfo_vmlist where vmname = %s and vmmacc = %s ", (vmname, vmmacc)
        _ins_sql = "INSERT INTO vminfo_vmlist( vcname,dcname,cluster,hostip,vmname,vmip,vmmacc,status,vmpath ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
        vcname, dc, cluster, hostname, vmname, vmip, vmmacc, vmstat, vmpath)
        if self.query(vmname, vmmacc):
            try:
                self.cursor.execute(*_del_sql)
                self.cursor.execute(*_ins_sql)
                print('insert success for %s' % vmname)
                self.database.commit()
            except Exception as e:
                print('insert failed', e)

    def saveData(self, vcname):
        wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = wbk.add_sheet(vcname, cell_overwrite_ok=False)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.height = 0x0190
        # font.bold = True
        style.font = font

        query_rows = "select count(*)  from vminfo_vmlist where vcname = '%s'" % (vcname)
        self.cursor.execute(query_rows)
        count_rows = self.cursor.fetchone()[0]

        sql = "select vcname,dcname,cluster,hostip,vmname,vmip,vmmacc,status,vmpath from vminfo_vmlist where vcname = '%s'" % (
            vcname)
        self.cursor.execute(sql)
        column_name = ['vcname', 'dcname', 'cluster', 'hostip', 'vmname', 'vmip', 'vmmacc', 'status', 'vmpath']

        for i in range(len(column_name)):
            sheet.write(0, i, column_name[i], style)

        for i in range(1, count_rows - 1):
            data = self.cursor.fetchone()
            for j in range(0, len(column_name)):
                sheet.write(i, j, data[j], style)
        # self.cursor.close()
        wbk.save('vmlist.xls')

    def update(self, vmname, vmmacc, status):
        sql = "UPDATE vminfo_vmlist set status = %s where vmname = %s and vmmacc = %s ", (status, vmname, vmmacc)
        try:
            self.cursor.execute(*sql)
            print('update successfully for', vmname)
        except Exception as e:
            print('update', e)

    def disconnect(self):
        self.database.close()


def WaitForTasks(tasks, si):
    """
    Given the service instance si and tasks, it returns after all the
    tasks are complete
    """

    pc = si.content.propertyCollector

    taskList = [str(task) for task in tasks]

    # Create filter
    objSpecs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                for task in tasks]
    propSpec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                          pathSet=[], all=True)
    filterSpec = vmodl.query.PropertyCollector.FilterSpec()
    filterSpec.objectSet = objSpecs
    filterSpec.propSet = [propSpec]
    filter = pc.CreateFilter(filterSpec, True)

    try:
        version, state = None, None

        # Loop looking for updates till the state moves to a completed state.
        while len(taskList):
            update = pc.WaitForUpdates(version)
            for filterSet in update.filterSet:
                for objSet in filterSet.objectSet:
                    task = objSet.obj
                    for change in objSet.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in taskList:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            taskList.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if filter:
            filter.Destroy()


def SendMsgToSparkRoom(msg=None):
    sparkapi = 'https://api.ciscospark.com/v1/messages'
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
    headers = {'Content-Type': 'application/json;charset=UTF-8',
               'Authorization': 'Bearer YjU2MzJhOTMtZDIzYS00MjMyLThmM2EtYzVjZjhhMjk4YjQwMTEzOWU4ZGUtNmFi'}
    headers['User-Agent'] = useragent
    roomId = '74bf8974-9b33-3892-b1f0-914bb42d465f'  # test room
    # roomId = '28e3c750-6908-11e6-a747-2b856e15b09b' ##this is CMR Scrum Room
    data = {"roomId": roomId, "text": msg, "markdown": "**%s**" % msg}
    data = json.dumps(data)
    # print data
    try:
        r = requests.post(sparkapi, headers=headers, data=data)
        if r.status_code == 200:
            print("send msg successfully")
        # print(r.status_code)

    except Exception as e:
        print('send msg failed', e)
        pass


def main():
    """
    Iterate through all datacenters and list VM info.
    """
    count = 0
    db = DBOperation('10.224.38.201', '3306', 'root', 'pass', 'vm')
    # db.precreation()
    args = GetArgs()
    outputjson = True if args.json else False

    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and '
                                          'user %s: ' % (args.host, args.user))

    si = SmartConnectNoSSL(host=args.host,
                           user=args.user,
                           pwd=password,
                           port=int(args.port))
    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    children = content.rootFolder.childEntity
    for child in children:  # Iterate though DataCenters
        dc = child
        clusters = dc.hostFolder.childEntity
        for cluster in clusters:  # Iterate through the clusters in the DC
            if hasattr(cluster, 'host'):
                hosts = cluster.host  # Variable to make pep8 compliance
            else:
                continue
            for host in hosts:  # Iterate through Hosts in the Cluster
                hostname = host.summary.config.name
                vms = host.vm
                # tasks = [vm.PowerOn() for vm in vms if vm.summary.runtime.powerState == 'PoweredOff']
                # WaitForTasks(tasks, si)
                for vm in vms:  # Iterate through each VM on the host
                    # print('dir vm',dir(vm))
                    vmname = vm.summary.config.name
                    summary = vmsummary(vm)
                    # print(summary[0],summary[1],summary[2],summary[3])
                    vmip, vmmacc, vmstat, vmpath = summary
                    vcname = db.getVCName(args.host)
                    vminfo = vcname, dc.name, cluster.name, hostname, vmname, vmip, vmmacc, vmstat, vmpath
                    # print(vminfo)
                    db.insert(*vminfo)
                    count += 1
    ret = "Total %s records inserted for %s !" % (count, vcname)
    print(ret)
    SendMsgToSparkRoom(ret)
    # db.saveData(vcname)
    db.disconnect()


# Start program
if __name__ == "__main__":
    main()
