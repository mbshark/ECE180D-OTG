import socket
import random
import time
# Serial Communication instantiation
BUFFER_SIZE = 1024   
# TCP Communication instantiation for unity
#TCP_IP = 'localhost'#192.168.1.12'    #IP address on Server
#TCP_IP = '192.168.1.184'
TCP_IP= '192.168.43.44'
TCP_IP_WINDOWS = '192.168.43.44'
TCP_PORT_UNITY = 50000
TCP_WINDOWs = 50005        #same port number as server
imu_dict = {"1": "R1,P1", "2":"R2,P2", "3":"R3,P3", "4":"R4,P4"}
mock_rate = 0.5

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


WINDOWS_CONNECTED = False
UNITY_CONNECTED = False

if UNITY_CONNECTED:
	#create the unity tcp connection
	unity_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	unity_connect.connect((TCP_IP, TCP_PORT_UNITY))

if WINDOWS_CONNECTED:
	# create the windows TCP Connection
	windows = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Bind")
	windows.bind((TCP_IP_WINDOWS, TCP_WINDOWs))
	print("Listen")
	windows.listen(1)


	print("Accept")
	conn, addr = windows.accept()
	print ('Packet Connection address:', addr)

speech = ["bruin", "banana", "ring","umbrella", "ironing board", "notebook"]
while True:  
    if WINDOWS_CONNECTED:
	    data = conn.recv(BUFFER_SIZE)
	    if not data: break
	    print ("received data:", data.decode())
    else:
    	speech_cmd = speech[random.randint(0,len(speech)-1)]
    	image_buf = '(R,1)'
    	packet = "{}*{}*{}*{}*{}*{}".format(
			imu_dict["1"],
			imu_dict["2"],
			imu_dict["3"],
			imu_dict["4"],
			speech_cmd,
			image_buf)
    	print(packet)
    	data = packet.encode()
    	time.sleep(mock_rate)

    if UNITY_CONNECTED:
    	unity_connect.send(data)


if UNITY_CONNECTED:
	unity_connect.close()

if WINDOWS_CONNECTED:
	windows.close()