import socket
import serial

# Serial Communication instantiation
port = 'COM3'
baud = 115200
ser = serial.Serial(port, baud)
ser.flushInput()

# TCP Communication instantiation
TCP_IP = '192.168.1.184'    #IP address on Server
TCP_PORT = 5005             #same port number as server
BUFFER_SIZE = 1024          

 # Creqte and connect to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:  
    
    # reads data from serial port and passes through
    # TCP connection
    ser_bytes = ser.readline()
    print(ser_bytes)
    s.send(ser_bytes)

    
s.close()

