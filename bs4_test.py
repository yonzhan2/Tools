from bs4 import BeautifulSoup, element
import requests, re

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
<li>
  <span class="fr">32.3.0.354</span>Page version:
</li>
<li>
  <span class="fr">32.3.0.341</span>Application version:
</li>
"""
sisfile = '''
<?xml version="1.0" encoding="UTF-8"?>

<WINCFG>
	<WIN Name="prodc76win" Version="7.20.1" Comment="Primary Jabber Cluter isj1 for YUM">
		<ClusterInfo Name="isj1" PrimaryName="isj1" GSBName="gitx1" PeerClusterName="gitx1" XCPListenPort="7400" SharedSecret="wbxadmin" DialbackSecret="A1rwerit76DRkx1" RestartIntervalByProcManager="20" WaitTimeForRouterStart="300" PublicKeyFile="/opt/jabber/certs/imlogging_publickey.pem" EncryptionPassword="00112233445566778899aabbccddeeff00112233445566778899aabbccddeeff" GlobalSubjectKey="prodzone" DependentPlatform="groupserver" DependentClusterList="asj1,gatx1" URLForPostStatistics="http://abt1ngs201.webex.com/postJabberStats.php" MSEndCell="pncell_PMSJ1PR0" EnableMDM="1" EnablePUSH="1" />
		<DatabaseServer HostName="xcpdb" ServiceName="sjjbr1ha.webex.com" UserName="dvjbr1" Password="jbr4n1St" TableSpace="JBR_DATA">
			<DatabaseNode Host="10.252.8.171" Port="1901"/>
			<DatabaseNode Host="10.252.8.172" Port="1901"/>
                        <DatabaseNode Host="10.252.8.173" Port="1901"/>
		</DatabaseServer>
                  <Pools>
                     <Pool name="A" Description="Pool A" zone="JSM"/>
                    <Pool name="*" Description="default pool" zone="JSM"/>
                    <Pool name="JXF" Description="JAF/JXF pool" zone="JAF"/>
                </Pools>
                 <WAPIDBServer HostName="wapidb" ServiceName="sjconha.webex.com" UserName="connectwapi3" Password="X5alth0m!" TableSpace="WAPI_DATA">
                          <DatabaseNode Host="10.252.9.112" Port="1618"/>
                          <DatabaseNode Host="10.252.9.113" Port="1618"/>
                          <DatabaseNode Host="10.252.9.114" Port="1618"/>
                   </WAPIDBServer> 
	</WIN>
</WINCFG>
'''

soup = BeautifulSoup(html, 'html.parser')

sis = BeautifulSoup(sisfile, 'html5lib')
print soup.head
print soup.head.contents[0]
print type(soup.a.string)
if type(soup.a.string) == element.Comment:
    print soup.a.string

print soup.find_all('span')
print type(soup.p.attrs)
soup.p.attrs['name'] = 'test'
print soup.p.string

for link in sis.find_all('pool'):
    print link.get('zone')
