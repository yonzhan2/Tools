#!/bin/bash

function presetup(){
    vmname=$1
    vmip=$2
    sh /vmconfig/vmsetup.sh ${vmname} ${vmip}
}

if [ $# -ne 2 ];then
  echo "Usage: bash $0 <vm name> <vm ipaddr>"
else
    presetup $1 $2
fi