import socket
import serial

# Serial Communication instantiation
BUFFER_SIZE = 2048    
# TCP Communication instantiation for unity
TCP_IP = '192.168.1.12'    #IP address on Server
TCP_PORT_UNITY = 5005        #same port number as server
TCP_PORT = 5003
TCP_PORT_speech = 5000

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)



# create the IMU TCP Connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT_UNITY))
s.listen(1)



conn, addr = s.accept()
print ('Packet Connection address:', addr)

while True:  
    
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print ("received data:", data)

conn.close()
