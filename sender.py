import os
import socket
import binascii
import time

host = "127.0.0.1"
port = 13029
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.settimeout(0.5)

filename = "lalala.txt"

#Handshake
print("Connecting to %s" % str(addr))
currentTime = time.ctime(time.time()) + "\r\n"
UDPSock.sendto(currentTime.encode('ascii'), addr)

#Checksum function
def generate_checksum(message):
    return str(binascii.crc32(message) & 0xffffffff)

#Begin of file transmission
f = open (filename, "rb")
l = f.read(1024)
l1 = l + '|'
check = generate_checksum(l1)
l2 = l1 + check
UDPSock.sendto(l2, addr)

while True:
    l = f.read(1024)
    l1 = l + '|'
    check = generate_checksum(l1)
    l2 = l1 + check
    UDPSock.sendto(l2, addr)    
    acknowledged = False

    while not acknowledged:
        try:
            ACK, addr = UDPSock.recvfrom(1024)
            acknowledged = True
        except socket.timeout:
            UDPSock.sendto(l, addr)
    if ACK=="EXIT":
        print ACK
        break
    print ACK

#Close socket
UDPSock.close()
os._exit(0)
