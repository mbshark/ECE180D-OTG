import cv2
import numpy as np
import socket
import asyncio
import random
import pickle
# from ColorLabeler import ColorLabeler
# import imutils
# TCP Communication instantiation

BUFFER_SIZE = 1024

# Creqte and connect to the socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#s.connect((TCP_IP, TCP_PORT))
cap = None
font = None
image_data = {"T": [], "R": [], "P": [], "H": []}
width = 0.0
height = 0.0
frame = None
sock = None

def nothing():
	pass


def setup():
	global cap, font, width, height
	cap = cv2.VideoCapture(0)
	cv2.namedWindow("Trackbars")
	cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
	cv2.createTrackbar("L-S", "Trackbars", 66, 255, nothing)
	cv2.createTrackbar("L-V", "Trackbars", 134, 255, nothing)
	cv2.createTrackbar("U-H", "Trackbars", 180, 180, nothing)
	cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
	cv2.createTrackbar("U-V", "Trackbars", 243, 255, nothing)

	font = cv2.FONT_HERSHEY_COMPLEX

	#cap.read()
	cap.open(0)
	while (not cap.isOpened()):
		print("Waiting")
		# get vcap property
	if True:

		width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
		height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
		print(width)
		print(height)

async def run():
	global cap, font, width, height, image_data

	while True:

		await asyncio.sleep(random.uniform(0.1,0.5))
		_, frame = cap.read()
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		l_h = cv2.getTrackbarPos("L-H", "Trackbars")
		l_s = cv2.getTrackbarPos("L-S", "Trackbars")
		l_v = cv2.getTrackbarPos("L-V", "Trackbars")
		u_h = cv2.getTrackbarPos("U-H", "Trackbars")
		u_s = cv2.getTrackbarPos("U-S", "Trackbars")
		u_v = cv2.getTrackbarPos("U-V", "Trackbars")

		lower = {'red':(100, 30, 55), 'green':(66, 122, 129), 'blue':(97, 100, 117), 'yellow':(23, 59, 119), 'orange':(0, 50, 80)}
		upper = {'red':(186,255,255), 'green':(86,255,255), 'blue':(117,255,255), 'yellow':(54,255,255), 'orange':(20,255,255)}
		colors = {'red':(0,0,255), 'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255)}

		lower_red = np.array([l_h, l_s, l_v])
		# lower_red = lower['red']
		# upper_red = upper['red']
		upper_red = np.array([u_h, u_s, u_v])

		mask = cv2.inRange(hsv, lower_red, upper_red)
		kernel = np.ones((5, 5), np.uint8)
		mask = cv2.erode(mask, kernel)

		# Contours detection
		if int(cv2.__version__[0]) > 3:
			# Opencv 4.x.x
			contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		else:
			# Opencv 3.x.x
			_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		#send data
		image_data = {"T": [], "R": [], "P": [], "H": []}
		# cl = ColorLabeler()
		for cnt in contours:

			#color = cl.label(cnt)
			#print(color)
			area = cv2.contourArea(cnt)
			approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
			x = approx.ravel()[0]
			y = approx.ravel()[1]

			if area > 300:
				if len(approx) <= 6:
					txt=""
					cv2.drawContours(frame, [approx], 0, (0, 255, 0), 10)
					if x <= width/2:
						if y<= height/2:
							#Q1
							txt = quadrantHelp(len(approx),1)
						else:
							#Q4
							txt = quadrantHelp(len(approx),4)
					else:
						if y <= height/2:
							#Q2
							txt = quadrantHelp(len(approx),2)
						else:
							#Q3
							txt = quadrantHelp(len(approx),3)
					#txt+= (" "+ str(x) +","+str(y))
					cv2.putText(frame, txt, (x, y), font, 1, (0, 255, 0))

		cv2.imshow("Frame", frame)
		#cv2.imshow("Mask", mask)

		key = cv2.waitKey(1)
		if key == 27:
			break

	cap.release()
	cv2.destroyAllWindows()

def quadrantHelp(sides, quadrant):
	shapeDict = {3:"T", 4:"R", 5:"P", 6: "H"}
	if sides in range(3,7): #>= 3 and approx < 7:
		if quadrant not in image_data[shapeDict[sides]]:
			image_data[shapeDict[sides]].append(quadrant)
		return shapeDict[sides] + "-Q"+str(quadrant)
	return None
