# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
#import fcntl
import struct
import speech_recognition as sr

SETUP = 0
SPEAKING = 1
LISTENING = 2
CLOSED = 3

serverIP = "131.179.46.131"
port = 5000

connected = True
r = None
m = None

class Client():
	def __init__(self, num):
		import signal
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.piNum= num
		self.clientIP = "131.179.3.78"
		if connected:			
			print("Setting up server")
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((serverIP,port))
			msg = "Hello my IP is: "+ self.clientIP
			self.sock.send(msg.encode())
		self.state = SETUP

	#def get_ip_address(self, ifname):
	#	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#	return socket.inet_ntoa(fcntl.ioctl(
	#		s.fileno(),
	#		0x8915,  # SIOCGIFADDR
	#		struct.pack('256s'.encode(), ifname[:15].encode()))[20:24])
	
	def setupServer(self, serverIP):
		if connected:
			sock = self.sock#self.get_ip_address('wlan0')
		#Test print of IP address
		print("This is the CLIENT.")
		print ("The client IP address is:", self.clientIP)
		#init_msg = pickle.dumps((self.piNum, clientIP))		
		print("The server IP address is: ", serverIP)

		#sock.sendto(init_msg,(serverIP,8888))

	def setupSpeech(self):
		global r, m 
		r = sr.Recognizer()
		m = sr.Microphone()
		try:
			print("A moment of silence, please...")
			with m as source: r.adjust_for_ambient_noise(source)
			print("Set minimum energy threshold to {}".format(r.energy_threshold))
		except:
			print("Setting up failed")

	def runClient(self):
		if connected:
			sock = self.sock
		ack = str(self.piNum)
		try:
			try:
				while True:
					while True:
						import signal
						signal.signal(signal.SIGINT, signal.SIG_DFL)
						
						
						if (self.state == SETUP):
							'''data,addr = sock.recvfrom(4096)
							if not data: 
								print('No data')
								break
							r_ip, r_piNum, resp =  pickle.loads(data)
							print('Pi#: ', r_piNum)
							print('Client IP: ', r_ip)
							print('Server response: ', resp)'''
							self.state = SPEAKING
						elif (self.state == SPEAKING):
							command = self.speak()
							msg = str(command)#pickle.dumps((self.piNum, command))
							m = "S,"+ msg
							if (msg == "pause"):
								print("Player wants to PAUSE the game")
								if connected:
									sock.send(m.encode())
								print("Sent ", msg)
							elif (msg == "play"):
								print("Player wants to play the game")
								if connected:
									sock.send(m.encode())
								print("Sent ", msg)
							elif (msg == "hint"):
								print("Player wants a hint")
								if connected:
									sock.send(m.encode())
								print("Sent ", msg)
							else:
								print("Not a real command to send")
							self.state = SPEAKING
						elif (self.state == LISTENING):
							print("LISTENING MODE")
							data,addr = sock.recv(1024)
							if not data: 
								print('No data')
								break
							#resp =  pickle.loads(data)
							print("Received ", resp)	
							self.state = SPEAKING	
				#ack_msg = pickle.dumps((self.piNum, "ACK"))
				#sock.sendto(ack_msg,(serverIP,8080))
				self.state = CLOSED
				print('Client closed')
				if connected:
					sock.close()
			except KeyboardInterrupt:
				pass
		except KeyboardInterrupt:
				pass


	def speak(self):
		global r,m
		try:
			while True:
				print("Speaking Mode")
				with m as source: audio = r.listen(source)
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

if __name__ == "__main__":
	client = Client(0)
	client.setupServer(serverIP)
	client.setupSpeech()
	client.runClient()

'''
self-generate labels
T->Player 1
R -> Player 2
Star -> Play 3
Shape4 -> Play 4
Triangle,Square 5
(T, 1)
image_msg = ()

msg = "({},{},{}, {},{})".format(IMU2,IMU2, IMU3, speech, image_data)
'''