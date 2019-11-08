# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You don’t install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import numpy as np
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

iparray = np.empty((1,40,16),dtype=str)

#Test/Demo Purposes
k = 0

# Assigns a port for the server that listens to clients connecting to this port.
serv.bind(('172.20.10.5', 8080))
while True:
    while True:
        data, addr = serv.recvfrom(4096)
        if not data: break
        data = data.decode()
        print("Data provided is: ")
        print(data)
        print('\n')

        recData = ""

        #Empty the array if the received data is a RESET function
        if(data == "RESET"):
            iparray = np.empty((1,40,16),dtype=str)
            recData = "RESET"

        #Parse the data into position and IP address.
        else:
            posBool = True
            ipBool = True
            pos = ""
            ip = ""
            i = 0
            while posBool:
                if(data[i] == ','):
                    posBool = False
                    i = i+1
                    break
                pos = pos + data[i]
                i = i+1
            
            while ipBool:
                if(i >= len(data)):
                    ipBool = False
                    break
                ip = ip + data[i]
                i = i+1

            #Add the IP address to the array of IP addresses that will later be referenced
            for j in range (0, len(ip)):
                iparray[(0,int(pos)-1)][j] = ip[j]

            recData = str(int(pos)+1)

        print("iparray[" + str((int(pos)-1)) + "]: ")

        ipAdd = ""

        for l in range (0,len(iparray[0,int(pos)-1])):
            ipAdd = ipAdd + iparray[0,int(pos)-1][l]

        print(ipAdd)
        print('\n')

        k = k + 1

        serv.sendto((recData).encode(),(ipAdd,8080))

        if (k > 1000):
            break
        
    if (k > 1000):
        break

print("Parsing demo completed")

ipArr = []
for k in range (0,len(iparray[0])):
    ipTemp = ""
    for temp in range (0,len(iparray[0,k])):
        ipTemp = ipTemp + iparray[0,k][temp]
    ipArr.append(ipTemp)


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