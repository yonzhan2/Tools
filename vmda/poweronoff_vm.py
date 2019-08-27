#!/usr/bin/env python
"""
Written by Dann Bohn
Github: https://github.com/whereismyjetpack
Email: dannbohn@gmail.com

Clone a VM from template example
"""
# from __future__ import print_function
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
import atexit
import argparse
import getpass
import re


def get_args():
    """ Get arguments from CLI """
    parser = argparse.ArgumentParser(
        description='Arguments for talking to vCenter')

    parser.add_argument('-s', '--host',
                        required=True,
                        action='store',
                        help='vSpehre service to connect to')

    parser.add_argument('-o', '--port',
                        type=int,
                        default=443,
                        action='store',
                        help='Port to connect on')

    parser.add_argument('-u', '--user',
                        required=True,
                        action='store',
                        help='Username to use')

    parser.add_argument('-p', '--password',
                        required=False,
                        action='store',
                        help='Password to use')

    parser.add_argument('-v', '--vm-name',
                        required=True,
                        action='store',
                        help='Name of the VM you wish to make')

    args = parser.parse_args()

    if not args.password:
        args.password = getpass.getpass(
            prompt='Enter password')

    return args


def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True


def main():
    """
    Let this thing fly
    """
    args = get_args()

    # connect this thing
    si = SmartConnectNoSSL(
        host=args.host,
        user=args.user,
        pwd=args.password,
        port=args.port)
    # disconnect this thing
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    container = content.rootFolder  # starting point to look into
    viewType = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    containerView = content.viewManager.CreateContainerView(
        container, viewType, recursive)

    children = containerView.view
    vmlist = [vm.name for vm in children if re.search(args.vm_name, vm.name)]
    ct74 = list(filter(lambda x: re.search('ct74', x), vmlist))
    ct69 = list(filter(lambda x: not re.search('ct74', x), vmlist))
    print(vmlist, ct74, ct69)

    powerofftask = [vm.PowerOff() for vm in children if vm.name in ct74]
    powerontask = [vm.PowerOn() for vm in children if vm.name in ct69]

    wait_for_task(powerofftask)
    wait_for_task(powerontask)
    print("Task is done!")


# start this thing
if __name__ == "__main__":
    main()
