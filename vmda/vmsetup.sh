#!/bin/bash

function isct74()
{
grep -o "CentOS Linux release 7.*" /etc/redhat-release  > /dev/null
if [ $(echo $?) -eq 0 ];then
    return 0
else
    return 1
fi
}

function vmsetup()
{

    hostname=$1
    ip=$2


    prefix=`echo ${ip} |cut -d"." -f1-3`
    gateway=${prefix}.1
    subfix=`echo ${gateway} |cut -d"." -f3-4`

    ##configure /etc/hosts
    sed -i "/${hostname}/d" /etc/hosts
    echo "$(echo ${ip}|cut -d '-' -f 1) ${hostname}.qa.webex.com ${hostname} " >> /etc/hosts

    ##configure network
    if isct74 ;then
        echo "${hostname}.qa.webex.com" > /etc/hostname
    else
        sed -i "/HOSTNAME/d"  /etc/sysconfig/network
        echo "HOSTNAME=${hostname}.qa.webex.com" >> /etc/sysconfig/network
    fi

    if isct74 ; then
        ethname=ens192
    else
        ethname=eth0
    fi

    ##configure network
    cp -fp /etc/sysconfig/network-scripts/ifcfg-${ethname} /tmp

    start=`echo ${ip} |cut -d'-' -f1|cut -d '.' -f4`
    if [ $(echo ${ip} |grep -o '-' |wc -l) -gt 0 ];then
        end=`echo ${ip} |cut -d'-' -f2`
    else
        end=${start}
    fi

    loop=`expr $end - $start`
    i=0
    while [ $i -le $loop ];
    do

        if [ $i -eq 0  ];then
            eth_name=${ethname};
        else
            eth_name=${ethname}:`expr $i - 1`
        fi

        echo "DEVICE=${eth_name}" > /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        if isct74 ; then
            echo "NAME=${ethname}" >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        fi
        echo "BOOTPROTO=static"   >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        echo "IPADDR=${prefix}.`expr ${start} + $i`"  >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        echo "NETMASK=255.255.255.128" >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        echo "ONBOOT=yes"         >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        echo "TYPE=Ethernet"      >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}
        echo "GATEWAY=${gateway}" >> /etc/sysconfig/network-scripts/ifcfg-${eth_name}

        let i++

    done

    chmod 755 /etc/sysconfig/network-scripts/ifcfg-*

    /etc/init.d/network restart

    ##configure reslove.conf
    cp /etc/resolv.conf /etc/resolv.conf.bak
    echo "nameserver 10.194.241.211" > /etc/resolv.conf
    echo "nameserver 10.194.241.212" >> /etc/resolv.conf
    #echo "nameserver 10.240.${subfix}" > /etc/resolv.conf
    #echo "nameserver 10.241.${subfix}" >> /etc/resolv.conf


    echo "#NTP Client" > /etc/ntp.conf
    echo "server ${gateway}" >> /etc/ntp.conf
    echo "restrict default noserve noquery nomodify" >> /etc/ntp.conf
    echo "restrict 127.0.0.1" >> /etc/ntp.conf
    echo "restrict ${gateway} mask 255.255.255.255 nomodify notrap noquery" >> /etc/ntp.conf
    echo "driftfile /var/lib/ntp/drift" >> /etc/ntp.conf

    ###update ntp setting
    sed -i 's/maxskew=100/maxskew=1000000000/g' /usr/local/bin/ntpchk.sh
    sh /usr/local/bin/ntpchk.sh >/dev/null 2>&1

    ###update slim config
    /opt/slim/daemon/slimdm kill
    rm -f /opt/slim/daemon/slimdm.ini.orig23
    cp   -rf /opt/slim/daemon/slimdm.ini   /opt/slim/daemon/slimdm.ini.orig23
    cat   /dev/null  > /opt/slim/daemon/slimdm.ini
    echo '<slim svc="data"  jrepath="/opt/slim/daemon/jre" logsize="1048576" loglevel="5" logdir="/tmp/slimlog/" sid="1" >' > /opt/slim/daemon/slimdm.ini
    echo '                               <logserverip>10.224.41.22</logserverip> '  >> /opt/slim/daemon/slimdm.ini
    echo '                               <logserverip>10.224.41.23</logserverip> '   >> /opt/slim/daemon/slimdm.ini
    echo '               <allowedip>10.224.41.0-10.224.41.255,10.224.42.0-10.224.42.255</allowedip>'  >> /opt/slim/daemon/slimdm.ini
    echo '</slim>' >>  /opt/slim/daemon/slimdm.ini
    cat  /opt/slim/daemon/slimdm.ini
    chmod 755  /opt/slim/daemon/slimdm.ini
    sed -i 's/Defaults    requiretty/#Defaults    requiretty/g' /etc/sudoers
    /opt/slim/daemon/slimdm start
    /opt/slim/daemon/slimdm start

    ##cmnfigure ssh key
    test -d /home/wbxbuilds/.ssh || mkdir /home/wbxbuilds/.ssh -p

    ####Interal PFLAB SSH KEY########
    echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvELFpPfxgsCgCqlsG4lEYXr8rpIdX4uRIKFG4XzbFMu0Yjpp+JnvjSoIlW5OMKiVFdyDaVFHrlxpsoY0C0DihPCxqbpP2wci4bmZJVUj/RN22+CbO0qQdYLFfVF8A5csCLWrvadbxtjZ7SZEzSgWxsXMtMHCatFOVCPa4LWAoeeUKNUHCWNE8AiQmUwx9Yer6LdP7lGjGrYErxO/XWd6wngxKiyUVhKw3JyO2OYPZF5GpPeIp/kFJ6AYISS1AeECYyk0AkBXMKuELL2u8mNbnS2pJ4fe/p05ahMHzkLuhi4yYjBp2201aovSwCapNcjYjFuKP3nhGAb0d0VHWncVUw== wbxbuilds@sshlogin" > /home/wbxbuilds/.ssh/authorized_keys

    chown wbxbuilds.wbxbuilds /home/wbxbuilds/.ssh -R

    ##reboot server
#    /sbin/reboot
}

vmsetup $1 $2