#PyUnityserver.py

import socket
import asyncio
import threading
import random
import time
import speech_recognition as sr
import realtime_shape_detection as rt

dir(sr)

#GLOBAL CONSTANTS
# Serial Communication instantiation
BUFFER_SIZE = 1024
# TCP Communication instantiation for unity

#TCP_IP = 'localhost'#'192.168.1.12'		#IP address on Server
#TCP_IP = '192.168.43.3'

# TCP connection to connect to unity server
TCP_IP = '192.168.43.44'
#TCP_IP = '172.20.10.4' #ericks hotspot
TCP_PORT_UNITY = 50005		#same port number as server

# TCP connection for IMUs to connect to
TCP_IP_IMU = '192.168.43.9' 
#TCP_IP_IMU = '192.168.1.184'
TCP_PORT_IMU = 50006

NUM_THREADS = 5
UNITY_CONNECTED = False#True
IMU_CONNECTED = False

NUM_IMUS = 4
last_time_sent = 0
last_time_received = 0
imu_dict = {"1": "R1,P1", "2":"R2,P2", "3":"R3,P3", "4":"R4,P4"}
conns = []
speech_cmd = ""
image_buf = ""
unity_connect = None
s = None
imus_available = False
server_available = False

r = None
m = None

async def setupConnections():
	global unity_connect, s, imus_available, server_available
	if UNITY_CONNECTED:
		print("Connect to Unity")
		unity_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		unity_connect.connect((TCP_IP, TCP_PORT_UNITY))
		server_available = True

	if IMU_CONNECTED:
		imus = 0
		while imus != NUM_IMUS:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((TCP_IP_IMU, TCP_PORT_IMU))
			s.listen(1)
			conn, addr = s.accept()
			print("New IMU addr: ", addr)
			conns.append(conn)
			imus_available = True
			imus+=1
			await asyncio.sleep(random.uniform(0.1,0.2))

async def receiveIMUData():
	global last_time_received, s

	while True:
		if IMU_CONNECTED and imus_available:
				for conn in conns:
					data = conn.recv(BUFFER_SIZE)
					data = data.decode('utf-8')             # decodes data from byte to string
					data = data.replace("\r\n","")      	# cleans data as it contains "\r\n"
					# checks identifier of data type
					if (data[0] >= '1' and data[0] <='4'):
						data_splt = data.split(",")
						#print(data_splt)
						index = data_splt[0]
						imu_data_splt = data_splt[1]+ "," + data_splt[2]
						imu_data = imu_data_splt
						#print(imu_data)
						imu_dict[index] = imu_data
						#print(imu_dict)

		time_received = time.time()
		#print("Receiving :", time_received - last_time_received)
		last_time_received = time_received
		await asyncio.sleep(random.uniform(0.1,0.2))
	if IMU_CONNECTED:
		conn.close()
		s.close()

def setupSpeech():
		global r, m
		r = sr.Recognizer()
		m = sr.Microphone()
		try:
			print("A moment of silence, please...")
			with m as source: r.adjust_for_ambient_noise(source)
			print("Set minimum energy threshold to {}".format(r.energy_threshold))
		except:
			print("Setting up failed")

async def speak():
		global r,m
		try:
			while True:
				print("Speaking Mode")
				with m as source: 
					#audio = r.listen(source)
					audio = r.listen(source,phrase_time_limit=3)
				print("Processing")
				try:
					# recognize speech using Google Web Speech
					value = r.recognize_google(audio)
					if str is bytes:
						print(u"You said {}".format(value).encode("utf-8"))
						return value
					else:
						print("You said {}".format(value))
						return value

				except sr.UnknownValueError:
					print("Unrecognized Value")
				except sr.RequestError as e:
					print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		except KeyboardInterrupt:
			pass

async def receiveSpeechData():
	global speech_cmd
	commands = ["pause", "play", "hint", "unlock", \
	"bruin", "banana", "ring","umbrella", "ironing", "iron", "notebook"]
	while True:
		command = await speak()
		msg_arr= (str(command)).split(" ")
		#msg_arr = str(command)
		for msg in msg_arr:
			if msg.lower() in commands:
				
				print("Player said ", msg)
				if (msg.lower() == "iron" or msg.lower() == "ironing"):
					speech_cmd = "iron"
				else:
					speech_cmd = msg
				break
		await asyncio.sleep(random.uniform(0.1,0.2))


async def receiveImageData():
	global image_buf
	
	i = 0
	#try:
	rt.setup()
	#except:
	#	print("Setting up failed")
	await rt.run()
	
	'''
	while True:
		#print("image")
		#Possible Race Condition?
		#data = rt.image_data
		print()
		image_buf += temp_dict[i%4]
		i+=1
	'''

async def sendToUnity():
	global imu_dict, last_time_sent, image_buf, speech_cmd, unity_connect
	while True:
		time_sent = time.time()
		packet = ""
		#Create Packet
		#print(imu_dict["1"])
		'''
		set image buf to what you need it to be
		avoid *

		'''
		msg = ""
		#print(rt.image_data)
		#quads = [1, 2, 3, 4]
		quad_shp = {1:[],2:[],3:[],4:[]}

		for shape in rt.image_data:
			key = rt.image_data[shape]
			for q in key:
				quad_shp[q].append(shape)
		#print(quad_shp)
		
		for quad in quad_shp:
			shapes = quad_shp[quad]
			if len(shapes) == 0:
				shp = "({},{})$".format("N", quad)
				image_buf+=shp
			else:
				for shape in shapes:
					shp = "({},{})$".format(shape, quad)
					image_buf+=shp
		'''
		for key in rt.image_data:
			for quad in rt.image_data[key]:
				shp = "({},{})$".format(key, quad)
				image_buf+=shp
				if quad in quads:
					quads.remove(quad)

		'''
		#print(quads)
		#for unused in quads:
		#	shp = "({},{})$".format("N", unused)
		#	image_buf+=shp
		
		packet = "{}*{}*{}*{}*{}*{}".format(
			imu_dict["1"],
			imu_dict["2"],
			imu_dict["3"],
			imu_dict["4"],
			speech_cmd,
			image_buf)
		#print("Send to Unity: ", time_sent-last_time_sent)
		print(packet)
		if UNITY_CONNECTED and server_available:
			unity_connect.send(packet.encode())
		image_buf = ""
		speech_cmd = ""
		last_time_sent = time_sent
		await asyncio.sleep(random.uniform(0.2,0.5))
	if UNITY_CONNECTED:
		unity_connect.close()

def thr(i):
	# we need to create a new loop for the thread, and set it as the 'default'
	# loop that will be returned by calls to asyncio.get_event_loop() from this
	# thread.
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	if (i==0):
		loop.run_until_complete(setupConnections())
	elif (i == 1):
		loop.run_until_complete(receiveIMUData())
	elif (i == 2):
		loop.run_until_complete(receiveSpeechData())
	elif (i == 3 ):
		loop.run_until_complete(receiveImageData())
	elif (i == 4):
		loop.run_until_complete(sendToUnity())

	loop.close()


def main():
	global last_time_sent, last_time_received
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	last_time_sent = time.time()
	last_time_received= time.time()
	setupSpeech()
	threads = [threading.Thread(target=thr, args=(i,)) for i in range(NUM_THREADS)]
	[t.start() for t in threads]
	[t.join() for t in threads]
	print("bye")


if __name__ == "__main__":
	main()

# https://wiki.python.org/moin/UdpCommunication
# https://www.geeksforgeeks.org/socket-programming-python/