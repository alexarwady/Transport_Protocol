import os
import socket
import binascii
import time

host = "127.0.0.1"
port = 13029
buf = 1044
count = 1
ACK = "ACK"
EXIT = "EXIT"
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.bind(addr)
olddata = "aaa"

filename = "lalala1.txt"

#Handshake
tm, addr = UDPSock.recvfrom(1024)
print("Connected on %s" % tm.decode('ascii'))

#Checksum functions
def generate_checksum(message):
    return str(binascii.crc32(message) & 0xffffffff)

def validate_checksum(message):
    msg,reported_checksum = message.rsplit('|',1)
    msg += '|'
    check1=generate_checksum(msg)
    if check1 == reported_checksum:
        return True
    else:
        return False

#Begin of file receipt
f = open(filename,"wb")
(data, addr) = UDPSock.recvfrom(buf)
checked=validate_checksum(data)

while (data):
    if count == 1:
        while not checked:
            (data, addr) = UDPSock.recvfrom(buf)
            checked=validate_checksum(data)
        data,notimp = data.rsplit('|',1)
        f.write(data)
        UDPSock.sendto(ACK, addr)
        count = 0
    else:
        (data, addr) = UDPSock.recvfrom(buf)
        checked=validate_checksum(data)
        while not checked:
            (data, addr) = UDPSock.recvfrom(buf)
            checked=validate_checksum(data)
        data,notimp = data.rsplit('|',1)
        
        if olddata == data:
            print "duplicate"
            (data, addr) = UDPSock.recvfrom(buf)
            checked=validate_checksum(data)
            count = 1
        else:
            olddata = data
            f.write(data)
            UDPSock.sendto(ACK, addr)
UDPSock.sendto(EXIT, addr) 
f.close()    

#Close socket
UDPSock.close()
os._exit(0)
