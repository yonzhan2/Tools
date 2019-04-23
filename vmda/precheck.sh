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

if isct74 ; then
    echo "net.ipv6.conf.all.disable_ipv6=1" >> /etc/sysctl.conf
    echo "net.ipv6.conf.default.disable_ipv6=1" >> /etc/sysctl.conf
    sysctl -p
else
  count=`grep eth1 /etc/udev/rules.d/70-persistent-net.rules |wc -l`

  if [ $count -gt 0 ];then
    sed -i '/eth0/d' /etc/udev/rules.d/70-persistent-net.rules
    sed -i 's/eth1/eth0/g' /etc/udev/rules.d/70-persistent-net.rules
    udevadm control --reload-rules
    udevadm trigger --attr-match=subsystem=net
    service network restart
  fi

fi