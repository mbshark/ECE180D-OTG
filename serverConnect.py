# Uses Mark Geha's code https://github.com/markgeha8/CapstoneProject180D/blob/master/Server/serverConnect.py
# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You don’t install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import numpy as np
import socket
import fcntl
import struct
import pickle
import asyncio
import threading
import random
import time
#from seatArrangement import arrange
#from serverConnect import connect

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(
		s.fileno(),
		0x8915,  # SIOCGIFADDR
		struct.pack('256s', ifname[:15].encode())
	)[20:24])

#Test/Demo Purposes
# Assigns a port for the server that listens to clients connecting to this port.
'''
try:
	portno = int(input("What port would you like to use for the server? "))
except ValueError:
	print("This is not a valid number.")
'''


serv = None
arrangement = None
ipDict = dict()
addrDict = dict()
posDict = dict()
portno = 8080
k = 0

TOP = 0
BOTTOM = 1
state = 0

ON = 1
OFF = 0

def thr(i):
	# we need to create a new loop for the thread, and set it as the 'default'
	# loop that will be returned by calls to asyncio.get_event_loop() from this
	# thread.
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	#loop.run_until_complete(do_stuff(i))
	if (i == 1):
		loop.run_until_complete(connect())
	else:
		loop.run_until_complete(arrange())    
	loop.close()

async def connect():	
	global serv, ipDict, portno
	serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverIP = get_ip_address('wlan0')
	print("This is the SERVER.")
	print("The server IP address is:", serverIP)
	serv.bind((serverIP, portno))
	while True:
		while True:
			await asyncio.sleep(random.uniform(0.1, 0.5))
			print("connect")
			data, addr = serv.recvfrom(4096)
			if not data: 
				break
			piNum,pos, ip = pickle.loads(data) 
			ipDict[piNum] = ip
			addrDict[piNum] = addr
			posDict[piNum] = pos
			# ip/addr
			print("Data provided is: ", piNum, "   ", ip)
			#Verification of server-side logic
			rand = {5:"dino", 6:"apple", 7:"computadora"}
			

			try:		
				serv.sendto(pickle.dumps((piNum,ip,rand[piNum])), (addrDict[piNum]))
			except:
				print("Cound not send")

		await asyncio.sleep(random.uniform(0.1, 0.5))
		
def LED_state_machine():
	global state
	if (state == TOP):
		return BOTTOM
	if (state == BOTTOM):
		return TOP


def sendToClients(state):
	if (state == TOP):
		for pi in addrDict:
			if (posDict[pi] == "TOP"):
				print("Turn {} on", pi)
				try:		
					serv.sendto(pickle.dumps(ON), (addrDict[pi]))
				except:
					print("Cound not send")

			else:
				print("Turn {} off", pi)
				try:		
					serv.sendto(pickle.dumps(OFF), (addrDict[pi]))
				except:
					print("Cound not send")
	if (state == BOTTOM):
		for pi in addrDict:
			if (posDict[pi] == "BOTTOM"):
				print("Turn {} on", pi)
				try:		
					serv.sendto(pickle.dumps(ON), (addrDict[pi]))
				except:
					print("Cound not send")

			else:
				print("Turn {} off", pi)
				try:		
					serv.sendto(pickle.dumps(OFF), (addrDict[pi]))
				except:
					print("Cound not send")
		


async def arrange():
	global arrangements, state
	while True:
		await asyncio.sleep(random.uniform(0.1, 0.5))
		state = LED_state_machine()
		print("State is ", state)
		sendToClients(state)




def main():
	num_threads = 2
	threads = [ threading.Thread(target = thr, args=(i,)) for i in range(num_threads) ]
	[ t.start() for t in threads ]
	[ t.join() for t in threads ]
	print("bye")


if __name__ == "__main__":
	main()

#https://wiki.python.org/moin/UdpCommunication
#https://www.geeksforgeeks.org/socket-programming-python/
