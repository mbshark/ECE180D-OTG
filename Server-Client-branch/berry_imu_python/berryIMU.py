#!/usr/bin/python

import time
import math
import IMU
import datetime
import os
import socket



# TCP Communication instantiation
TCP_IP = '192.168.43.9'    #IP address on Server
#TCP_IP = '172.20.10.7'
#TCP_IP = '131.179.47.232'
TCP_PORT = 50006             #same port number as server
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("connected")

RASBPERRYPI_NUM = 1 #be sure to change these per device

start_time = int(round(time.time() * 1000))

# global constants for quaternion update 
GyroMeasError = math.pi*(float(40.0) / float(180.0))
GyroMeasDrift = math.pi*(float(0.0) / float(180.0))
beta = math.sqrt(float(3.0) / float(4.0)) * GyroMeasError
zeta = math.sqrt(float(3.0) / float(4.0)) * GyroMeasDrift
deltat = float(0.0)
lastUpdate = 0
Now = 0
q = [float(1.0),float(0.0),float(0.0),float(0.0)]




IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

# resolutions for accel, gyro, and mag data
aRes = 0.00021
gxRes = 0.023
gyRes = 0.038
gzRes = 0.00787
mRes = 0.0003





def MadgwickQuaternionUpdate(ax,ay,az,gx,gy,gz,mx,my,mz):
    q1 = q[0]
    q2 = q[1]
    q3 = q[2]
    q4 = q[3]
    norm = float(0.0)
    hx = float(0.0)
    hy = float(0.0)
    _2bx = float(0.0)
    _2bz = float(0.0)
    s1 = float(0.0)
    s2 = float(0.0)
    s3 = float(0.0)
    s4 = float(0.0)
    qDot1 = float(0.0)
    qDot2 = float(0.0)
    qDot3 = float(0.0)
    qDot4 = float(0.0)


    # Auxiliary variables to avoid repeated arithmetic
    _2q1mx = float(0.0)
    _2q1mx = float(0.0)
    _2q1mz = float(0.0)
    _2q2mx = float(0.0)
    _4bx = float(0.0)
    _4bz = float(0.0)
    _2q1 = float(float(2.0) * q1)
    _2q2 = float(float(2.0) * q2)
    _2q3 = float(float(2.0) * q3)
    _2q4 = float(float(2.0) * q4)
    _2q1q3 = float(float(2.0) * q1 * q3)
    _2q3q4 = float(float(2.0) * q3 * q4)
    q1q1 = float(q1 * q1)
    q1q2 = float(q1 * q2)
    q1q3 = float(q1 * q3)
    q1q4 = float(q1 * q4)
    q2q2 = float(q2 * q2)
    q2q3 = float(q2 * q3)
    q2q4 = float(q2 * q4)
    q3q3 = float(q3 * q3)
    q3q4 = float(q3 * q4)
    q4q4 = float(q4 * q4)
    

    
       
    # Normalise accelerometer measurement
    norm = math.sqrt(ax * ax + ay * ay + az * az)

    if (norm == float(0.0)):
        return #handle NaN

    
    norm = float(1.0)/norm
    ax *= norm
    ay *= norm
    az *= norm

    # Normalise magnetometer measurement
    norm = math.sqrt(mx * mx + my * my + mz * mz)
    if (norm == float(0.0)):
         return  # handle NaN
    norm = float(1.0)/norm
    mx *= norm
    my *= norm
    mz *= norm

    # Reference direction of Earth's magnetic field
    _2q1mx = float(2.0) * q1 * mx
    _2q1my = float(2.0) * q1 * my
    _2q1mz = float(2.0) * q1 * mz
    _2q2mx = float(2.0) * q2 * mx

    
    hx = mx * q1q1 - _2q1my * q4 + _2q1mz * q3 + mx * q2q2 + _2q2 * my * q3 + _2q2 * mz * q4 - mx * q3q3 - mx * q4q4
    hy = _2q1mx * q4 + my * q1q1 - _2q1mz * q2 + _2q2mx * q3 - my * q2q2 + my * q3q3 + _2q3 * mz * q4 - my * q4q4
    _2bx = math.sqrt(hx * hx + hy * hy)
    _2bz = -_2q1mx * q3 + _2q1my * q2 + mz * q1q1 + _2q2mx * q4 - mz * q2q2 + _2q3 * my * q4 - mz * q3q3 + mz * q4q4
    _4bx = float(2.0) * _2bx
    _4bz = float(2.0) * _2bz

    # Gradient decent algorithm corrective step
    s1 = -_2q3 * (float(2.0) * q2q4 - _2q1q3 - ax) + _2q2 * (float(2.0) * q1q2 + _2q3q4 - ay) - _2bz * q3 * (_2bx * (float(0.5) - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q4 + _2bz * q2) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q3 * (_2bx * (q1q3 + q2q4) + _2bz * (float(0.5) - q2q2 - q3q3) - mz)
    s2 = _2q4 * (float(2.0) * q2q4 - _2q1q3 - ax) + _2q1 * (float(2.0) * q1q2 + _2q3q4 - ay) - float(4.0) * q2 * (float(1.0) - float(2.0) * q2q2 - float(2.0) * q3q3 - az) + _2bz * q4 * (_2bx * (float(0.5) - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q3 + _2bz * q1) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q4 - _4bz * q2) * (_2bx * (q1q3 + q2q4) + _2bz * (float(0.5) - q2q2 - q3q3) - mz)
    s3 = -_2q1 * (float(2.0) * q2q4 - _2q1q3 - ax) + _2q4 * (float(2.0) * q1q2 + _2q3q4 - ay) - float(4.0) * q3 * (float(1.0) - float(2.0) * q2q2 - float(2.0) * q3q3 - az) + (-_4bx * q3 - _2bz * q1) * (_2bx * (float(0.5) - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (_2bx * q2 + _2bz * q4) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + (_2bx * q1 - _4bz * q3) * (_2bx * (q1q3 + q2q4) + _2bz * (float(0.5) - q2q2 - q3q3) - mz)
    s4 = _2q2 * (float(2.0) * q2q4 - _2q1q3 - ax) + _2q3 * (float(2.0) * q1q2 + _2q3q4 - ay) + (-_4bx * q4 + _2bz * q2) * (_2bx * (float(0.5) - q3q3 - q4q4) + _2bz * (q2q4 - q1q3) - mx) + (-_2bx * q1 + _2bz * q3) * (_2bx * (q2q3 - q1q4) + _2bz * (q1q2 + q3q4) - my) + _2bx * q2 * (_2bx * (q1q3 + q2q4) + _2bz * (float(0.5) - q2q2 - q3q3) - mz)
    norm = math.sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4) # normalise step magnitude
    norm = float(1.0)/norm
    s1 *= norm
    s2 *= norm
    s3 *= norm
    s4 *= norm

    # Compute rate of change of quaternion
    qDot1 = float(0.5) * (-q2 * gx - q3 * gy - q4 * gz) - beta * s1
    qDot2 = float(0.5) * (q1 * gx + q3 * gz - q4 * gy) - beta * s2
    qDot3 = float(0.5) * (q1 * gy - q2 * gz + q4 * gx) - beta * s3
    qDot4 = float(0.5) * (q1 * gz + q2 * gy - q3 * gx) - beta * s4

    # Integrate to yield quaternion
    q1 += qDot1 * deltat
    q2 += qDot2 * deltat
    q3 += qDot3 * deltat
    q4 += qDot4 * deltat
    norm = math.sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4);    # normalise quaternion
    norm = float(1.0)/norm
    q[0] = q1 * norm
    q[1] = q2 * norm
    q[2] = q3 * norm
    q[3] = q4 * norm
    

currmax = 0.0
currmin = 0.0


while True:


    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    MAGx = IMU.readMAGx()
    MAGy = IMU.readMAGy()
    MAGz = IMU.readMAGz()
    

    #Scales the data based off precalculated values 
    ax = ACCx*aRes
    ay = ACCy*aRes
    az = -1*ACCz*aRes

    gx = -1*GYRx*gxRes
    gy = -1*GYRy*gyRes
    gz = GYRz*gzRes

    mx = -1*MAGx*mRes
    my = MAGy*mRes - 0.35 # without offset range is [-0.11,1.2] when it is sppose to be [-0.5,0.5]
    mz = MAGz*mRes

    '''
    val = ax
    if (val > 0):
        print("++")
    else:
        print("--")

    if (currmax < val):
        currmax = val
    if (currmin > val):
        currmin = val
    print(str(currmax)+","+str(currmin))
    '''

    
    #time vector
    Now = int(round(time.time() * 1000))-start_time
    deltat=((Now - lastUpdate)/float(1000.0))
    lastUpdate = Now
    MadgwickQuaternionUpdate(ax,ay,az,gx*math.pi/float(180.0),gy*math.pi/float(180.0),gz*math.pi/float(180.0),mx,my,mz)
    
    yaw   = math.atan2(float(2.0) * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3]) 
    pitch = -math.asin(float(2.0) * (q[1] * q[3] - q[0] * q[2]))
    roll  = math.atan2(float(2.0) * (q[0] * q[1] + q[2] * q[3]), q[0] * q[0] - q[1] * q[1] - q[2] * q[2] + q[3] * q[3])
    pitch *= float(180.0) / math.pi
    yaw   *= float(180.0) / math.pi; 
    yaw   -= 13.8; # Declination at Danville, California is 13 degrees 48 minutes and 47 seconds on 2014-04-04
    roll  *= float(180.0) / math.pi

    packet = str(RASBPERRYPI_NUM)+","+str(roll) + "," + str(pitch)
    print(packet)
    s.send(packet)



    #slow program down a bit, makes the output more readable
    time.sleep(0.01)



    
    
