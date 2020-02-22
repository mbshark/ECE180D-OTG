import socket
import serial

# Serial Communication instantiation
BUFFER_SIZE = 1024   
# TCP Communication instantiation for unity
#TCP_IP = 'localhost'#192.168.1.12'    #IP address on Server
#TCP_IP = '192.168.1.184'
TCP_IP = '172.20.10.7'
TCP_PORT_UNITY = 50000        #same port number as server

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)



# create the IMU TCP Connection
unity = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Bind")
unity.bind((TCP_IP, TCP_PORT_UNITY))
print("Listen")
unity.listen(1)


print("Accept")
conn, addr = unity.accept()
print ('Packet Connection address:', addr)

while True:  
    
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print ("received data:", data.decode())

conn.close()
