import socket
import serial

# Serial Communication instantiation
port = 'COM5'
baud = 115200
ser = serial.Serial(port, baud)
ser.flushInput()

# TCP Communication instantiation
TCP_IP = '192.168.1.67'    #IP address on Server
TCP_PORT = 5003             #same port number as server
BUFFER_SIZE = 20

 # Creqte and connect to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:  
	if(ser.in_waiting >0):
		data= ser.readline()
		#line = line.decode('utf-8')
		##line = line.replace("\n","")
		#line = line.replace("\r","")
		#data = line.encode('utf-8')
		
		print(data)
		s.send(data)
    
    # reads data from serial port and passes through
    # TCP connection
    #ser_bytes = ser.readline()
    #ser_bytes = ser_bytes.replace("\r","")
    #ser_bytes = ser_bytes.replace("\n","")
    #print(ser_bytes)
    #s.send(ser_bytes)

    
s.close()

