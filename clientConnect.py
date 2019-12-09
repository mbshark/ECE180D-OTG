# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct
import pickle
import asyncio
import time

SETUP = 0
RUNNING = 1
CLOSED = 2

ON = 1
OFF = 0

class Client():
	def __init__(self, num):
		self.piNum= num
		self.pos = "ROW_1"
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.state = SETUP
	
	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s'.encode(), ifname[:15].encode()))[20:24])

	def turnOnLED(self):
		print("This turns on LED")
		#time.sleep(5)
	def turnOffLED(self):
		print("This turns off LED")
		#time.sleep(5)

	def setupServer(self, serverIP):
		sock = self.sock
		clientIP = self.get_ip_address('wlan0')
		#Test print of IP address
		print("This is the CLIENT.")
		print ("The client IP address is:", clientIP)
		init_msg = pickle.dumps((self.piNum, self.pos, clientIP))		
		print("The server IP address is: ", serverIP)

		sock.sendto(init_msg,(serverIP,8080))

	def runClient(self):	
		sock = self.sock
		ack = pickle.dumps((self.piNum))	
		while True:
			while True:
				print("Waiting")
				#sock.settimeout(20.0)
				import signal
				signal.signal(signal.SIGINT, signal.SIG_DFL)
				data,addr = sock.recvfrom(4096)
				if not data: 
					print('No data')
					break
				if (self.state == SETUP):
					r_ip, r_piNum, resp =  pickle.loads(data)
					print('Pi#: ', r_piNum)
					print('Client IP: ', r_ip)
					print('Server response: ', resp)
					self.state = RUNNING
				elif (self.state == RUNNING):
						signal =  pickle.loads(data)
						if signal == ON:
							self.turnOnLED()

						elif signal == OFF:
							self.turnOffLED()
						else:
							print("Invalid signal received: ", signal)				
				ack_msg = pickle.dumps((self.piNum, self.pos, "ACK"))
				sock.sendto(ack_msg,(serverIP,8080))
		
			self.state = CLOSED
			print('Client closed')
			sock.close()
		

if __name__ == "__main__":
	serverIP = "192.168.1.14"
	client = Client(1)
	client.setupServer(serverIP)
	client.runClient()
