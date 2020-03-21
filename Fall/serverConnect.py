# Uses Mark Geha's code https://github.com/markgeha8/CapstoneProject180D/blob/master/Server/serverConnect.py
# Reminder: This is a comment. The first line imports a default library "socket" into Python.
# You don’t install this. The second line is initialization to add TCP/IP protocol to the endpoint.
import numpy as np
import socket
import struct
import pickle
import asyncio
import threading
import random
import time
from seatArrangement import getSeatArr
from letter import findL
from quickstart import getFormResponses

def get_ip_address(ifname):
    try:
        import fcntl
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15].encode())
        )[20:24])
    except:
        try:
            host_name = socket.gethostname()
            host_ip = socket.gethostbyname(host_name)
            print(host_ip)
            return host_ip
        except:
            print("Unable to get Hostname and IP")

    # Test/Demo Purposes


# Assigns a port for the server that listens to clients connecting to this port.
'''
try:
    portno = int(input("What port would you like to use for the server? "))
except ValueError:
    print("This is not a valid number.")
'''

serv = None
arrangement = dict()
seats = []
ipDict = dict()
addrDict = dict()
posDict = dict()

ackDict = dict()
waitTime = dict()
picontot = 3

portno = 8080
k = 0
seed = 0

ROW_1 = 0
ROW_2 = 1
state = 0

ON = 1
OFF = 0
ACK = 0


def thr(i):
    # we need to create a new loop for the thread, and set it as the 'default'
    # loop that will be returned by calls to asyncio.get_event_loop() from this
    # thread.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop.run_until_complete(do_stuff(i))
    if (i == 0):
        loop.run_until_complete(connect())
    elif (i == 1):
        loop.run_until_complete(arrange())
    elif (i == 2):
        loop.run_until_complete(checkACK())
    loop.close()


async def connect():
    global serv, ipDict, portno, seats, arrangement, ACK, picontot
    serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv.settimeout(10)
    serverIP = "192.168.43.4"
    print("This is the SERVER.")
    print("The server IP address is:", serverIP)
    serv.bind((serverIP, portno))
    while True:
        while True:
            await asyncio.sleep(random.uniform(0.1, 0.5))
            # serv.settimeout(20)
            try:
                data, addr = serv.recvfrom(4096)
                if not data:
                    print("No Data")
                    break
                piNum, pos, ip = pickle.loads(data)
                if (ip == "ACK"):
                    # print("ACK from ",piNum)
                    ackDict[piNum] = piNum
                else:
                    ipDict[piNum] = ip
                    addrDict[piNum] = addr
                    print(addr)
                    posDict[piNum] = pos
                    # ip/addr
                    print("Data provided is: ", piNum, "   ", ip)
                    # Verification of server-side logic
                    rand = {1: "dino", 2: "apple", 3: "computadora", 4: "brains"}
                    try:
                        serv.sendto(pickle.dumps((piNum, ip, rand[piNum])), (addrDict[piNum]))
                    except:
                        print("Error Sending")
            except:

                print("Client Closed")

            if len(posDict) >= 4 and len(posDict) > picontot:
                picontot += 1
                seats = getSeatArr()
                # arrangement['U'] = letter.findU(seats)
                # arrangement['C'] = letter.findC(seats)
                arrangement['L'] = findL(seats)

        # arrangement['A'] = letter.findA(seats)
        await asyncio.sleep(random.uniform(0.1, 0.5))


def LED_state_machine():
    global state
    if (state == ROW_1):
        return ROW_2
    if (state == ROW_2):
        return 'L'
    if (state == 'U'):
        return 'C'
    if (state == 'C'):
        return 'L'
    if (state == 'L'):
        return ROW_1
    if (state == 'A'):
        return 'U'


async def sendClient(msg, pi):
    global serv, addrDict, ackDict, waitTime
    if (msg == ON):
        print("Turn on", pi)
    elif (msg == OFF):
        print("Turn off", pi)
    else:
        print("Error")

    try:
        serv.sendto(pickle.dumps(msg), (addrDict[pi]))
        ackDict[pi] = -1
        waitTime[pi] = 0
    except:
        print("Cound not send")
    wait = 0


async def sendToClients(state):
    global seed

    if (state == ROW_1):
        for pi in addrDict:
            if pi <= 2:
                await sendClient(ON, pi)
            else:
                await sendClient(OFF, pi)

    elif (state == ROW_2):
        for pi in addrDict:
            if pi > 2:
                await sendClient(ON, pi)
            else:
                await sendClient(OFF, pi)
    elif state == 'L':
        if len(arrangement) > 0:
            # seed = random.randint(0, len(arrangement['L']) - 1)
            for pi in addrDict:
                if pi in arrangement['L'][0] or pi in arrangement['L'][1]:
                    await sendClient(ON, pi)

                else:
                    await sendClient(OFF, pi)
        else:
            for pi in addrDict:
                if pi != 2:
                    await sendClient(ON, pi)

                else:
                    await sendClient(OFF, pi)

    else:  # unknown state turn off
        for pi in addrDict:
            await sendClient(OFF, pi)


async def checkACK():
    global ackDict, waitTime
    while True:
        # print("Check")
        delete = []
        for pi in ackDict:
            if ackDict[pi] == pi:
                # print("ACK!!!")
                delete.append(pi)
            else:
                waitTime[pi] += 1
                if (waitTime[pi] > len(addrDict) + 20):
                    print("Client does not exist: ", pi)
                    addrDict[pi] = -1
                    posDict[pi] = -1
                    ipDict[pi] = -1
                    delete.append(pi)
        if (len(delete) != 0):
            for key in delete:
                ackDict.pop(key, None)
                waitTime.pop(key, None)
        cleanClients()

        await asyncio.sleep(random.uniform(0.1, 0.5))


async def arrange():
    global arrangement, state
    try:
        while True:
            # if seats:
            # for i in range(5 * 60 / 5):
            await asyncio.sleep(random.uniform(3, 5))
            if (not len(ipDict) == 0):
                state = LED_state_machine()
            print("State is ", state)
            await sendToClients(state)
    except KeyboardInterrupt:
        print('interrupted!')


def cleanClients():
    global addrDict, posDict, ipDict
    delete = [pi for pi in addrDict if addrDict[pi] == -1]
    for key in delete:
        addrDict.pop(key, None)
        posDict.pop(key, None)
        ipDict.pop(key, None)


def main():
    num_threads = 3
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    threads = [threading.Thread(target=thr, args=(i,)) for i in range(num_threads)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    print("bye")


if __name__ == "__main__":
    main()

# https://wiki.python.org/moin/UdpCommunication
# https://www.geeksforgeeks.org/socket-programming-python/
