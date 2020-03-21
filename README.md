# ECE180D-OTG

### Fall - Grad Cap Project
Please refer to Fall/ folder for all materials related to the Grad Cap solution. This includes our server/client scripts, Google form parsing, and letter recognition.

### Winter - Escape Room
Please refer to the following folders/files relevant to this project:
<ul>
<li>IMUcontrol.cs : Unity Server, Game Flow for Escape Room</li>
<li>Server-Client-branch</li>
	<ul>
	<li>PyUnity.py : Python Server that creates and sends packet to MacUnity.py</li>
	<li>MacUnity.py : Python Server receiving packets and sending to Unity server</li>
	<li>realtime_shape_detection.py : Vision script for shape and quadrant detection</li>
	<li>berry_imu_python : Folder containing IMU related scripts</li>
		<ul>
		<li>berryIMU.py : Convert raw IMU readings, format values, and send to PyUnity.py</li>
		<li>IMU.py : Module for accelerometer, gyroscope, and magnetometer</li>
		<li>Config files</li>
		</ul>
	<li>Mock testing scripts</li>
	</ul>
<li>Finger_Counting : Related to future work, extensions of Escape Room</li>
	<ul>
	<li>finger-counting.py : main script</li>
	</ul>
<li>Server_Client_MockIMU :</li>
	<ul>
	<li>PyUnity in testing/development mode with IMU</li>
	<li>berry_imu : copy of contents from Server-Client-branch/berry_imu</li>
	<li>mock_IMU_client[1-4].py : Mock IMU client scripts</li>
	</ul>
<li>BerryIMU_Script_Automation- Final Revision</li>
	<ul>
	<li>Same contents as others. Uses script to automate connection/running of IMUs</li>
	</ul>	
</ul>

