#!/bin/bash

function presetup(){
    vmname=$1
    vmip=$2
    vmnetmask=$3
    vmgateway=$4
    sh /vmconfig/vmsetup.sh ${vmname} ${vmip} ${vmnetmask} ${vmgateway} >/vmconfig/vmsetup.log 2>&1
}

if [ $# -ne 4 ];then
  echo "Usage: bash $0 <vm name> <vm ipaddr> <vm netmask> <vm gateway>"
else
    presetup $1 $2 $3 $4
fi
