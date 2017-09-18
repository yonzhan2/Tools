import socket

server = '10.224.89.100'
try:
    hostname = socket.gethostbyaddr(server)[0]
    ipaddr = socket.gethostbyname(hostname)
    print hostname, ipaddr
except Exception, e:
    print "cannot get hostname", e
    hostname = ''
    ipaddr = ''
