#!/bin/bash
#release_version=39.5.0
#feature_num=meetsimplejun
echo "job is deploying client ${release_version} ${feature_num} ${client_buildnum}"

function listbuild(){
    buildnum=$1
    mac=`yum list WBXclient.mac.T33L-${release_version}.${feature_num}-${buildnum} | tee | tail -n 1|awk '{print $2}'` >/dev/null 2>&1
    win=`yum list WBXclient.T33L-${release_version}.${feature_num}-${buildnum} | tee | tail -n 1|awk '{print $2}'` >/dev/null 2>&1
    if [ X${win} == X${mac} ];then
        return 0
    else
    	return 1
    fi
}
if [ $(date +%Y%m%d) -lt 20190610 ];then

    find /var/tmp -name "*.rpm" -exec rm -f {} \;
    rm -f /etc/yum.repos.d/cmc_j2ee.repo && cp -fp /tmp/cmc_j2ee.repo /etc/yum.repos.d/cmc_j2ee.repo
    yum clean all >/dev/null 2>&1
    yum erase -y `rpm -qa|grep -E 'WBXclient|WBXmsi'` >/dev/null 2>&1
#    ##Download ci repo file
#    repo_url=https://cctg-cirepo.cisco.com   ##EC repo
#    repo_url=https://cctg-sjc16-cirepo.cisco.com  ##Jenkins repo
#    wget -q --user=ecuser --password=P@sslogin ${repo_url}/cirepo/webex_artifacts/client/webex-mac-packaging.mac/${release_version}.${feature_num}/build_history.webex-mac-packaging.${release_version}.txt -O /tmp/${release_version}-${feature_num}.txt --no-check-certificate
#
#    ##Parse file
#    cat /tmp/${release_version}-${feature_num}.txt |grep Buildnumber|tail -n 5|awk -F':' '{print $2}'|sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | sort -r > /tmp/buildnumber
#
#
#
#
#    while read line; do
#        listbuild $line
#        if [[ $? -eq 0 ]];then
#            echo "Current client build ${line} is going to deploy ..."
#            client_buildnum=$line
#            break
#        else
#            echo "Windows package number is not equal to Mac, ignore this package ${line} ..."
#        fi
#    done < /tmp/buildnumber

    if [[ -z ${client_buildnum} ]];then
    		echo
        yum install -y WBXclient.T33L-${release_version}.${feature_num}
    else
        yum install -y WBXclient.T33L-${release_version}.${feature_num}-${client_buildnum}

    fi


    if [[  $? -eq 0  ]];then

        ###change client directory to f${feature_num}

        cd /www/htdocs/client/

        ###Normal Case
#        clientver=`rpm -qa|grep client|grep WBXclient.T33L-${release_version}.f${feature_num} | awk -F'-' '{print $3}'|cut -d. -f1`
#        getdir=`ls -l |grep ^d |grep -w ${release_version}-${clientver} |awk '{print $NF}' |awk '{print $NF}' > /tmp/getdir`
#
#
#
#        if [[ -d  "WBXclient-${release_version}.f${feature_num}-${clientver}" ]];then
#            echo "client directory already changed done"
#            rm -rf WBXclient-${release_version}-${clientver}
#        else
#            mv $(cat /tmp/getdir) WBXclient-${release_version}.f${feature_num}-$clientver
#            pushd WBXclient-${release_version}.f${feature_num}-$clientver/version
#            echo  WBXclient-${release_version}.f${feature_num}-$clientver.txt > verclient.txt
#            mv $(cat /tmp/getdir).txt WBXclient-${release_version}.f${feature_num}-$clientver.txt
#             popd
#        fi
#
#        rm -f F${feature_num}
#        ln -sf WBXclient-${release_version}.f${feature_num}-$clientver F${feature_num}
#        chown -h nobody.nobody F${feature_num}
#        echo "change link done for this new client $clientver"


        ###Sepcial case without F character in build
        clientver=`rpm -qa|grep client|grep WBXclient.T33L-${release_version}.${feature_num} | awk -F'-' '{print $3}'|cut -d. -f1`

        getdir=`ls -l |grep ^d |grep -w ${release_version}-${clientver} |awk '{print $NF}' |awk '{print $NF}' > /tmp/getdir`

        if [ -d  "WBXclient-${release_version}.${feature_num}-${clientver}" ];then
            echo "client directory already changed done"
            rm -rf WBXclient-${release_version}.${feature_num}-$clientver
        fi


        mv $(cat /tmp/getdir) WBXclient-${release_version}.${feature_num}-$clientver
        pushd WBXclient-${release_version}.${feature_num}-$clientver/version
        echo  WBXclient-${release_version}.${feature_num}-$clientver.txt > verclient.txt
        mv $(cat /tmp/getdir).txt WBXclient-${release_version}.${feature_num}-$clientver.txt
        popd


        rm -f ${feature_num}
        ln -sf WBXclient-${release_version}.${feature_num}-$clientver ${feature_num}
        chown -h nobody.nobody ${feature_num}
        echo "change link done for this new client $clientver"
    else
        echo "Upgraded job failed. exit ..."
        exit 1
    fi

else
    echo "reached to maximum time slot, exit ..."
    exit 1
fi
