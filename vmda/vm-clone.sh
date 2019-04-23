#!/bin/bash

read -s -p "your CEC password: " password
#read -p "datastore step: " step
#read -p "vm start step: " start
#read -p "vm end step: " end
#echo "your input is : ${step} ${start} ${end}"

while read line;do
    python vm-clone.py -s cctg-sj-pf-vc2.cisco.com -u cisco\\yonzhan2 -p $password -v ${line} --template ct67b322c4g74g-withda --datacenter-name cctg-sj-pflab2 --vm-folder pflab-bed-env1 --datastore-name SJC_NETAPP3_LUN_APP_Env1  --cluster-name pflab-bed-env1 --no-power-on &

    if [ $(ps -ef|grep clone|grep -v grep|wc -l) -gt 3 ];then
        sleep 10
    fi
done <vmlist

###vmlist format
ed9stcbmm11-10.29.53.12-14
ed9stcbmm12-10.29.53.15-17