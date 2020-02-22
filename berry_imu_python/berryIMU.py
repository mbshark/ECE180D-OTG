#!/usr/bin/python
#
#    This program  reads the angles from the acceleromteer, gyroscope
#    and mangnetometer on a BerryIMU connected to a Raspberry Pi.
#
#    Both the BerryIMUv1 and BerryIMUv2 are supported
#
#    BerryIMUv1 uses LSM9DS0 IMU
#    BerryIMUv2 uses LSM9DS1 IMU
#
     #This program includes a number of calculations to improve the
#    values returned from BerryIMU. If this is new to you, it
#    may be worthwhile first to look at berryIMU-simple.py, which
#    has a much more simplified version of code which would be easier
#    to read.
#
#    This script is python 2.7 and 3 compatible
#
#    Feel free to do whatever you like with this code.
#    Distributed as-is; no warranty is given.
#
#    http://ozzmaker.com/

import time
import math
import IMU
import datetime
import os

'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''



IMU.detectIMU()     #Detect if BerryIMUv1 or BerryIMUv2 is connected.
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

# resolutions for accel, gyro, and mag data
aRes = 0.000263
mRes = 0.0168


'''
sumAcc = 0.0

#calculating aRes
for i in range (0,1000):
    sumAcc += IMU.readACCz()
avgSum = sumAcc/1000
print(1/avgSum)



'''
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

    ax = ACCx*aRes
    ay = ACCy*aRes
    az = ACCz*aRes

    print(GYRx)



    #slow program down a bit, makes the output more readable
    time.sleep(0.03)
    
