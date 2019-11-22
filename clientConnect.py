# Code obtained and then modified from this source
# http://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/


import socket
import fcntl
import struct
import pickle
import asyncio

class Client(Thread):
	def __init__(self, num):
		self.piNum= num
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s'.encode(), ifname[:15].encode()))[20:24])

	def turnOnLED(self):
		print("This turns on LED")

	def turnOffLED(self):
		print("This turns off LED")

	def setupServer(self, serverIP):
		sock = self.sock
		clientIP = self.get_ip_address('wlan0')
		#Test print of IP address
		print("This is the CLIENT.")
		print ("The client IP address is:", clientIP)
		init_msg = pickle.dumps((self.piNum,clientIP))		
		print("The server IP address is: ", serverIP)

		sock.sendto(init_msg,(serverIP,8080))

	def runClient(self):	
		sock = self.sock
		while True:
			while True:
				print("Waiting")
				sock.settimeout(10.0)
				data,addr = sock.recvfrom(4096)
				if not data: 
					print('No data')
					break
				r_ip, r_piNum, resp =  pickle.loads(data)
				print('Pi#: ', r_piNum)
				print('Client IP: ', r_ip)
				print('Server response: ', r_random)
				signal = int(resp)#placeholder
				if (signal == 1):
					self.turnOnLED()
					sleep(10) #asyncio
					self.turnOffLED()
					active = 1 #wait for response
			print('Client closed')
			sock.close()

if __name__ == "__main__":
	serverIP = "192.168.43.207"
	client = Client(5)
	client.setupServer(serverIP)
	client.runClient()

