# ECE180D-OTG

### Fall - Grad Cap Project
Please refer to Fall/ folder for all materials related to the Grad Cap solution. This includes our server/client scripts, Google form parsing, and letter recognition.

### Winter - Escape Room
Please refer to the following folders/files relevant to this project:
IMUcontrol.cs : Unity Server, Game Flow for Escape Room
Server-Client-branch
	-PyUnity.py : Python Server that creates and sends packet to MacUnity.py
	-MacUnity.py : Python Server receiving packets and sending to Unity server
	-realtime_shape_detection.py : Vision script for shape and quadrant detection
	-berry_imu_python : Folder containing IMU related scripts
		-berryIMU.py : Convert raw IMU readings, format values, and send to PyUnity.py
		-IMU.py : Module for accelerometer, gyroscope, and magnetometer
		-Config files
	-Mock testing scripts
Finger_Counting : Related to future work, extensions of Escape Room
	-finger-counting.py : main script
Server_Client_MockIMU :
	- PyUnity in testing/development mode with IMU
	- berry_imu : copy of contents from Server-Client-branch/berry_imu
	- mock_IMU_client[1-4].py : Mock IMU client scripts


