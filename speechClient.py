# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
#import fcntl
import struct
import pickle
import speech_recognition as sr

SETUP = 0
SPEAKING = 1
LISTENING = 2
CLOSED = 3

serverIP = "131.179.47.17"
port = 8888

r = None
m = None

class Client():
	def __init__(self, num):
		import signal
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.piNum= num
		print("Create")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("connect")
		self.sock.connect((serverIP,port))
		print("Sending Hello")
		#time.sleep(5)
		self.sock.send("Hello")
		print("Sent")
		data = self.sock.recv(1024)
		self.sock.close()
		print("received data:", data)
		self.state = SPEAKING


	#def get_ip_address(self, ifname):
	#	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#	return socket.inet_ntoa(fcntl.ioctl(
	#		s.fileno(),
	#		0x8915,  # SIOCGIFADDR
	#		struct.pack('256s'.encode(), ifname[:15].encode()))[20:24])
	
	def setupServer(self, serverIP):
		sock = self.sock
		clientIP = "172.31.53.64"#self.get_ip_address('wlan0')
		#Test print of IP address
		print("This is the CLIENT.")
		print ("The client IP address is:", clientIP)
		init_msg = pickle.dumps((self.piNum, clientIP))		
		print("The server IP address is: ", serverIP)

		sock.sendto(init_msg,(serverIP,8888))

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
		sock = self.sock
		ack = pickle.dumps((self.piNum))
		try:
			try:
				while True:
					while True:
						import signal
						signal.signal(signal.SIGINT, signal.SIG_DFL)
						
						
						if (self.state == SETUP):
							data,addr = sock.recvfrom(4096)
							if not data: 
								print('No data')
								break
							r_ip, r_piNum, resp =  pickle.loads(data)
							print('Pi#: ', r_piNum)
							print('Client IP: ', r_ip)
							print('Server response: ', resp)
							self.state = SPEAKING
						elif (self.state == SPEAKING):
							command = self.speak()
							msg = pickle.dumps((self.piNum, command))
							sock.sendto(msg,(serverIP,8888))
							print("Sent ", command)
							self.state = LISTENING
						elif (self.state == LISTENING):
							print("LISTENING MODE")
							data,addr = sock.recvfrom(4096)
							if not data: 
								print('No data')
								break
							resp =  pickle.loads(data)
							print("Received ", resp)	
							self.state = SPEAKING		
				#ack_msg = pickle.dumps((self.piNum, "ACK"))
				#sock.sendto(ack_msg,(serverIP,8080))
				self.state = CLOSED
				print('Client closed')
				sock.close()
			except KeyboardInterrupt:
				pass
		except KeyboardInterrupt:
				pass


	def speak(self):
		global r,m
		try:
			while True:
				print("Say something!")
				with m as source: audio = r.listen(source)
				print("Got it! Now to recognize it...")
				try:
					# recognize speech using Google Speech Recognition
					value = r.recognize_google(audio)
					# we need some special handling here to correctly print unicode characters to standard output
					if str is bytes:  # this version of Python uses bytes for strings (Python 2)
						#print(u"You said {}".format(value).encode("utf-8"))
						return value
					else:  # this version of Python uses unicode for strings (Python 3+)
						#print("You said {}".format(value))
						return value

				except sr.UnknownValueError:
					print("Oops! Didn't catch that")
				except sr.RequestError as e:
					print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		except KeyboardInterrupt:
			pass

if __name__ == "__main__":
	client = Client(0)
	client.setupServer(serverIP)
	client.setupSpeech()
	client.runClient()
