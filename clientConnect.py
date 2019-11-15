# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct
import pickle

#Read in IP
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s'.encode(), ifname[:15].encode())
    )[20:24])

clientIP = get_ip_address('wlan0')
#Test print of IP address

print("This is the CLIENT.")
print ("The client IP address is:", clientIP)

#Read in position(pos)
#Use code from Charlotte

#This is a filler for now
piNum = 5
init_bool = False

init_msg = pickle.dumps((piNum,clientIP))

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#enter server IP address - must be known beforehand

serverIP = "172.31.20.126"
print("The server IP address is: ", serverIP)

while(not init_bool):
    client.sendto(init_msg,(serverIP,8080))

#    client.bind((ip,8080))
#    while(not init_bool):
#        from_server = client.recvfrom(4096)
#        if(from_server.decode() == "RESET"):
#            print(from_server.decode())
#        if(from_server.decode() == pos_string):
#            init_bool = True
#            print("server matches client")
#        else:
#            print("server doesn't match client")
#            break




#test while loop to constantly read in directions from server
#while(init_bool)
#{
#    from_server = client.recv(4096)
#    if(from_server.decode() == "RESET")
#    {
#        client.close()
#    }
#    print(from_server.decode())
#
#}






#This will serve as a filler to see what we
client.close()
