import socket
import time
# TCP Communication instantiation
TCP_IP = 'localhost'#''192.168.1.12'	#IP address on Server
TCP_PORT_IMU = 50005			 #same port number as server
BUFFER_SIZE = 1024		  
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

 # Creqte and connect to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT_IMU))

f = open("FakeIMU.txt", "r")
print(f.readline())
Pi_num = 2
while True:  
	
	# reads data from serial port and passes through
	# TCP connection
	#ser_bytes = ser.readline()
	#print(ser_bytes)
	for ser_bytes in f:
		print(ser_bytes)
		msg = str(Pi_num) + "," + ser_bytes[0:len(ser_bytes)-1]
		s.send(msg.encode())
		time.sleep(0.5)

	
s.close()
