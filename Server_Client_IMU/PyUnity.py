#PyUnityserver.py

import socket
import asyncio
import threading
import random
import time
import speech_recognition as sr

#GLOBAL CONSTANTS
# Serial Communication instantiation
BUFFER_SIZE = 1024    
# TCP Communication instantiation for unity
TCP_IP = '192.168.1.12'		#IP address on Server
TCP_PORT_UNITY = 5005		#same port number as server
TCP_PORT_IMU = 5003
NUM_THREADS = 4
CONNECTED = True


last_time_sent = 0
last_time_received = 0
imu_dict = {"1": "R1,P1", "2":"R2,P2", "3":"R3,P3"}
speech_cmd = ""
image_buf = ""
unity_connect = None
s = None
conn = None

r = None
m = None

def setupConnections():
	global unity_connect, s, conn
	if CONNECTED:
		unity_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		unity_connect.connect((TCP_IP, TCP_PORT_UNITY))
	
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((TCP_IP, TCP_PORT_IMU))
		s.listen(1)
		conn, addr = s.accept()
		print ('IMU Connection address:', addr)

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
				#print("Speaking Mode")
				with m as source: audio = r.listen(source)
				#print("Processing")
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

def thr(i):
	# we need to create a new loop for the thread, and set it as the 'default'
	# loop that will be returned by calls to asyncio.get_event_loop() from this
	# thread.
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	if (i == 0):
		loop.run_until_complete(receiveIMUData())
	elif (i == 1):
		loop.run_until_complete(receiveSpeechData())
	elif (i == 2 ):
		loop.run_until_complete(receiveImageData())
	elif (i == 3):
		loop.run_until_complete(sendToUnity())
	loop.close()


async def receiveSpeechData():
	global speech_cmd
	while True:
		command = await speak()
		msg = str(command)	
		valid = True	
		if (msg == "pause"):
			print("Player wants to PAUSE the game")
		elif (msg == "play"):
			print("Player wants to play the game")
		elif (msg == "hint"):
			print("Player wants a hint")
		else:
			print("Not a real command to send")
			valid = False
		if valid:
			speech_cmd = msg
		await asyncio.sleep(random.uniform(0.1,0.1))




async def receiveImageData():
	global image_buf
	temp_dict = {0: "T,1", 1:"R,2",2:"R,3", 3: "R,4"}
	i = 0
	while True:
		#print("image")
		#Possible Race Condition?
		image_buf += temp_dict[i%4]
		i+=1
		await asyncio.sleep(random.uniform(0.1,0.5))


async def receiveIMUData(): 
	global last_time_received, conn, s
	
	while True:  
		if CONNECTED:
			data = conn.recv(BUFFER_SIZE)
			if not data: break
			print ("received data:", data)
			index = data[0]
			imu_data = data[1:]
			imu_dict[index] = imu_data

		time_received = time.time()
		#print("Receiving :", time_received - last_time_received)
		last_time_received = time_received
		await asyncio.sleep(random.uniform(0.1,0.5))
	if CONNECTED:
		conn.close()
		s.close()




async def sendToUnity():
	global imu_dict, last_time_sent, image_buf, speech_cmd, unity_connect
	while True:		
		time_sent = time.time()
		packet = ""
		#Create Packet
		packet = "{}.{}.{}.{}.{}".format(
			imu_dict["1"],
			imu_dict["2"],
			imu_dict["3"],
			speech_cmd,
			image_buf)
		print(packet)
		#print("Send to Unity: ", time_sent-last_time_sent)
		if CONNECTED:
			unity_connect.send(packet.encode())
		image_buf = ""
		speech_cmd = ""
		last_time_sent = time_sent
		await asyncio.sleep(random.uniform(0.5,0.5))
	if CONNECTED:
		unity_connect.close()


def main():
	global last_time_sent, last_time_received
	import signal
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	last_time_sent = time.time()
	last_time_received= time.time()
	setupConnections()
	setupSpeech()
	threads = [threading.Thread(target=thr, args=(i,)) for i in range(NUM_THREADS)]
	[t.start() for t in threads]
	[t.join() for t in threads]
	print("bye")


if __name__ == "__main__":
	main()

# https://wiki.python.org/moin/UdpCommunication
# https://www.geeksforgeeks.org/socket-programming-python/
