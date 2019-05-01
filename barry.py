#!/usr/bin/env python3

import cv2
import numpy as np
from color_filter import *

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


ESC_KEY = 27

running = True
key = ESC_KEY

cam = camera()
disp = display()

green_filter = filter([20,50,20], [70,255,255])

while running:
	
	# Get frame
	rval, frame = cam.get()
	
	if rval == True:
		
		# Apply filter
		frame, mask = green_filter.apply(frame, True, False)
		
		# Display
		key = disp.show(frame)
		
		# Handle keys
		if key != -1: print(key)
		green_filter.key_handler(key)
	
	# Check status
	if key == ESC_KEY:
		running = False

cam.release()
disp.close()	
		

