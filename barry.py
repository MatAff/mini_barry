#!/usr/bin/env python3

import cv2
import numpy as np

class camera(object):
	
	def __init__(self):
		self.vc = cv2.VideoCapture(0)		

	def get(self):
		return self.vc.read()
	
	def release(self):
		self.vc.release()

class display(object):
	 
	def __init__(self):
		self.name = "barry"
		cv2.namedWindow(self.name)		
	
	def show(self, frame):
		cv2.imshow(self.name, frame)
		key = cv2.waitKey(20)
		return key
	
	def close(self):
		cv2.destroyWindow(self.name)		

class filter(object):
	
	def __init__(self, lower, upper):
		self.lower = np.array(lower)
		self.upper = np.array(upper)

	def apply(self, bgr_frame, erode=False, dilate=False):    
		hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_frame, self.lower, self.upper)
		
		if erode == True:
			kernel = np.ones((5,5),np.uint8)
			mask = cv2.erode(mask,kernel,iterations = 1)
		
		if dilate == True:
			kernel = np.ones((5,5),np.uint8)
			mask = cv2.dilate(mask,kernel,iterations = 1)
		
		res = cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)
		
		return(res, mask)		

ESC_KEY = 27

running = True
key = ESC_KEY

cam = camera()
disp = display()

yellow_filter = filter([5,0,0], [75,255,255])

while running:
	rval, frame = cam.get()
	if rval == True:
		frame, mask = yellow_filter.apply(frame, False, True)
		key = disp.show(frame)
	if key == ESC_KEY:
		break

cam.release()
disp.close()	
		

