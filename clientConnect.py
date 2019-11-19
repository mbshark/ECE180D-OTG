# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct
import pickle
import asyncio


def turnOnLED():
    print("This turns on LED")

def turnOffLED():
    print("This turns off LED")

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

def runClient():
    #This is a filler for now
    piNum = 5
    active = True
    init_msg = pickle.dumps((piNum,clientIP))
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #enter server IP address - must be known beforehand

    serverIP = "192.168.43.190"
    print("The server IP address is: ", serverIP)
    #client.connect((serverIP,8080))

    client.sendto(init_msg,(serverIP,8080))

    while(active):
        print("Waiting")
        data,addr = client.recvfrom(4096);
        if (data):
            print("Received something")
            print('Received: ', pickle.loads(data))
            signal = 0 #placeholder
            if (signal == 1){        
                turnOnLED()
                sleep(10) #asyncio
                turnOffLED()
            }
        active = 1 #wait for response
    #This will serve as a filler to see what we
    client.close()

if __name__ == "__main__":
    runClient()