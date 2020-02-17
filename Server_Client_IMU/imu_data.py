import socket
import serial
import time

#*********************************************************
# TCP Communication instantiation for unity
#*********************************************************
#TCP_IP = '192.168.1.184'         # IP address on Server
TCP_IP = '172.20.10.7'
TCP_PORT_UNITY = 5005           # same port number as server
BUFFER_SIZE = 20                # Serial Communication instantiation

# ********************************************************
# Connection for IMUs PORTs
# ********************************************************
player_1_PORT = 5003




# ********************************************************
# Player Helper Function
# ********************************************************
def TCPConnectInit(port):
    # create the IMU TCP Connection
    player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    player.bind((TCP_IP, port))
    player.listen(1)

    return player

#Connects to players 
def player_connect(player):
    print ("Waiting for IMU Connection.....")
    player_conn, player_addr = player.accept()

    return player_conn, player_addr






if __name__ == "__main__":
    # init TCP connections 
    #unity = TCPConnectInit(TCP_PORT_UNITY)
    player_1 = TCPConnectInit(player_1_PORT)

    # connect to players
    player_1_conn, player_1_addr = player_connect(player_1)
    print("Player 1 connected")

    while True:          
        # reads data from serial port and passes through
        # TCP connection
        data = player_1_conn.recv(BUFFER_SIZE)
        data = data.decode('utf-8')             # decodes data from byte to string
        data = data.replace("\r\n","")      # cleans data as it contains "\r\n"
        # non latency data
        data_splt = data.split(",")
        #print(data_splt[0])
        #print(type(data_splt[0]))
        if (len(data_splt)==3 and data_splt[0]=='1'):
            #data = data.replace("\r\n","")      # cleans data as it contains "\r\n"
            data_bytes = data.encode('utf-8')
            print(data_bytes)
            #unity_connect.send(data)   
        
    #unit_connect.close()
    player_1_conn.close()
