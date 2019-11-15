# Uses Mark Geha's code https://github.com/markgeha8/CapstoneProject180D/blob/master/Server/serverConnect.py
# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You don’t install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import numpy as np
import socket
import fcntl
import struct
import pickle

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode())
    )[20:24])



serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ipDict = dict()

#Test/Demo Purposes
k = 0

# Assigns a port for the server that listens to clients connecting to this port.
'''
try:
    portno = int(input("What port would you like to use for the server? "))
except ValueError:
    print("This is not a valid number.")
'''
portno = 8080

serverIP = get_ip_address('wlan0')
print("This is the SERVER.")
print("The server IP address is:", serverIP)

serv.bind((serverIP, portno))
while True:
    while True:
        data, addr = serv.recvfrom(4096)
        if not data: 
            break

        '''
        #Empty the array if the received data is a RESET function
        if(data == "RESET"):
            iparray = np.empty((40,16),dtype=str)
            recData = "RESET"

        #Parse the data into position and IP address.
        else:
        '''

        piNum,ip = pickle.loads(data) # data already decoded above
        ipDict[piNum] = ip

        print("Data provided is: ", piNum, "   ", ip)
        # serv.sendto((recData).encode(),(ipAdd,8080))

        k = k + 1
        
        if (k > 1000):
            break
        
    if (k > 1000):
        break

print(ipDict)

'''ipArr = []
for k in range (0,len(iparray[0])):
    ipTemp = ""
    for temp in range (0,len(iparray[0,k])):
        ipTemp = ipTemp + iparray[0,k][temp]
    ipArr.append(ipTemp)
'''

#https://wiki.python.org/moin/UdpCommunication

#______________________________________________________________________________________________________#
#Code Test

#https://www.geeksforgeeks.org/socket-programming-python/
#i_add = 0
#cont = True
#serv.listen(40)
#
#while True:
#    while cont:
#        c, add = serv.accept()
#        if(add == ipArr[i_add]):
#            cont = False
#        else:
#            cont = True
#            c.close()

#    c.send(("testLED").encode())
#    c.close()

#______________________________________________________________________________________________________#
#Time Increment

#i_add = 0
#cont = True
#hold = True
#serv.listen(40)

#while True:
#    while cont:
#        c, add = serv.accept()
#        if(add == ipArr[i_add]):
#            cont = False
#        else:
#            cont = True
#            c.close()

#    c.send(("startLED").encode())

#    while hold:
#        msg = c.recv(4096)
#        if((msg.decode()) == "Done"):
#            hold = False

#    c.close()
