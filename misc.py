# import paramiko
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# server='173.37.48.17'
# batch_job_cmd = """
# sudo useradd shuqli
#
# sudo useradd -g wbxbuilds -G wbxbuilds wbxroot >/dev/null 2>&1
# sudo echo -e "echo '<slim svc="'"data"'"  jrepath="'"/opt/slim/daemon/jre"'" logsize="'"1048576"'" loglevel="'"5"'" logdir="'"/tmp/slimlog/"'" sid="'"1"'" >' > /opt/slim/daemon/slimdm.ini" > changepwd.sh
# sudo echo "echo '                               <logserverip>192.168.165.101</logserverip> '  >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
# sudo echo "echo '                               <logserverip>192.168.165.102</logserverip> '   >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
# sudo echo "echo '               <allowedip>173.36.202.1-173.36.202.255,173.36.203.1-173.36.203.255,192.168.165.1-192.168.165.255</allowedip>'  >> /opt/slim/daemon/slimdm.ini" >> changepwd.sh
# sudo echo "echo '</slim>' >>  /opt/slim/daemon/slimdm.ini" >> changepwd.sh
# sudo echo 'echo "wbx@Aa\$hfe02"|passwd --stdin wbxroot' >> changepwd.sh
# sudo echo 'echo "wbx@Aa\$hfcm"|passwd --stdin shuqli' >> changepwd.sh
# sudo echo 'echo "Hard2GuessMe"|passwd --stdin wbxbuilds' >> changepwd.sh
# sudo echo 'echo "Hard2GuessMe"|passwd --stdin root' >> changepwd.sh
# sudo echo 'rm -f /opt/slim/daemon/auto_register.xml' >> changepwd.sh
# sudo echo 'rm -f /opt/slim/daemon/slimdm.log*' >> changepwd.sh
# sudo echo "sed -i '/wbxbuilds/d' /etc/sudoers " >> changepwd.sh
# sudo echo "sed -i '/wbxroot/d' /etc/sudoers " >> changepwd.sh
# sudo echo "sed -i '/shuqli/d' /etc/sudoers " >> changepwd.sh
# sudo echo 'echo \"wbxbuilds            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
# sudo echo 'echo \"wbxroot            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
# sudo echo 'echo \"shuqli            ALL=(ALL)       NOPASSWD: ALL\" >> /etc/sudoers ' >> changepwd.sh
# sudo echo 'echo "before kill: slimdm process is `ps -ef|grep slimdm|grep daemon|cut -c 9-15`"' >> changepwd.sh
# sudo echo "ps -ef|grep slimdm|grep daemon|cut -c 9-15|xargs kill -9 ">> changepwd.sh
# sudo echo "/opt/slim/daemon/slimdm start" >> changepwd.sh
# sudo echo "/opt/slim/daemon/slimdm start" >> changepwd.sh
# sudo echo 'echo "after kill: slimdm process is `ps -ef|grep slimdm|grep daemon|cut -c 9-15`"' >> changepwd.sh
# sudo echo "echo current dir is \`pwd\`"  >> changepwd.sh
# sudo chmod 755 changepwd.sh
# sudo sed -i 's/relayhost = cnlabmda.qa.webex.com/relayhost = sjdmzmda.dmz.webex.com/g' /etc/postfix/main.cf
# sudo sed -i 's/relayhost = mda.webex.com/relayhost = sjdmzmda.dmz.webex.com/g' /etc/postfix/main.cf
# sudo service postfix restart  >/dev/null 2>&1
# sudo sed -i 's/maxskew=100$/maxskew=100000000/g' /usr/local/bin/ntpchk.sh >/dev/null 2>&1
# sudo service ntpd stop  >/dev/null 2>&1
# sudo ntpdate `sudo route -n | grep ^0.0.0.0 | awk '{print $2}'` > /dev/null 2>&1
# sudo service ntpd start  >/dev/null 2>&1
# sudo sh changepwd.sh
# """
# for user, pwd in list(zip(['wbxbuilds'],['Hard2GuessMe'])):
#     print(user, pwd)
#     try:
#         ssh.connect(server, username=user, password=pwd, timeout=5)
#         stdin, stdout, stderr = ssh.exec_command(batch_job_cmd)
#         output = stdout.read()
#         err = stderr.read()
#         print(f"output is {output}")
#         print(f"err is {err}")
#         break
#     except Exception as e:
#         print("error is ", e)
#     finally:
#         stdin, stdout, stderr = ssh.exec_command('sudo rm -f changepwd.sh && echo "success"')
#         output = stdout.read()
#         err = stderr.read()
#         print(f"output is {output}")
