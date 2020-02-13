import socket
import serial

# Serial Communication instantiation
BUFFER_SIZE = 1024    
# TCP Communication instantiation for unity
TCP_IP = '131.179.46.131'    #IP address on Server
TCP_PORT_UNITY = 5005        #same port number as server
TCP_PORT = 5003
TCP_PORT_speech = 5000



 # Create and connect to the socket
unity_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
unity_connect.connect((TCP_IP, TCP_PORT_UNITY))

# create the IMU TCP Connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


# create the speech TCP Connection
a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a.bind((TCP_IP, TCP_PORT_speech))
a.listen(1)

print ("Waiting for IMU Connection.....")

conn, addr = s.accept()
conn_spe,add_spe = a.accept()
print ('IMU Connection address:', addr)
print ('speech Connection address:', add_spe)

while True:  
    
    # reads data from serial port and passes through
    # TCP connection

    data = conn.recv(BUFFER_SIZE)
    speech = conn_spe.recv(BUFFER_SIZE)
    
    data = data + speech
    if not data: break
    if not speech: break
    print ("received data:", data)
    unity_connect.send(data)
    
    print(speech)

    
unit_connect.close()
conn.close()
conn_spe.close()
