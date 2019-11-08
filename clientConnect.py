# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct

#Read in IP
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s'.encode(), ifname[:15].encode())
    )[20:24])

ip = get_ip_address('wlan0')
#Test print of IP address
print(ip)

#Read in position(pos)
#Use code from Charlotte

#This is a filler for now
pos = 5
pos_string = str(pos)
init_msg = pos_string + "," + ip
init_bool = False


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#enter server IP address - must be known beforehand

while(not init_bool):
    client.sendto(init_msg.encode(),('172.20.10.5',8080))

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
