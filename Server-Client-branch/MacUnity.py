import socket

# Serial Communication instantiation
BUFFER_SIZE = 1024   
# TCP Communication instantiation for unity
#TCP_IP = 'localhost'#192.168.1.12'    #IP address on Server
#TCP_IP = '192.168.1.184'
TCP_IP= '192.168.43.44'
TCP_IP_WINDOWS = '192.168.43.44'
TCP_PORT_UNITY = 50000
TCP_WINDOWs = 50005        #same port number as server

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)



#create the unity tcp connection

unity_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
unity_connect.connect((TCP_IP, TCP_PORT_UNITY))


# create the windows TCP Connection
windows = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Bind")
windows.bind((TCP_IP_WINDOWS, TCP_WINDOWs))
print("Listen")
windows.listen(1)




print("Accept")
conn, addr = windows.accept()
print ('Packet Connection address:', addr)

while True:  
    
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print ("received data:", data.decode())
    unity_connect.send(data)

unity_connect.close()
windows.close()