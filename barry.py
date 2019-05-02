#!/usr/bin/env python3

import cv2
import numpy as np

from visual import *
from color_filter import *
from drive import * # Not available on laptop

ESC_KEY = 27

KEY_FORWARD = 0
KEY_BACKWARD = 0
KEY_LEFT = 0
KEY_RIGHT = 0

running = True
key = ESC_KEY

cam = Camera()
disp = Display()
twist = Twist()
ada_drive = AdaDrive() # Not available on laptop

#green_filter = Filter([20,0,20], [70,255,255])
green_filter = Filter([30, 135, 0], [55, 260, 55]) # Daytime 

while running:
	
	# Get frame
	rval, frame = cam.get()
	
	if rval == True:
		
		# Apply filter
		frame, mask = green_filter.apply(frame, True, False)
		
		# Get position
		avg_pos = green_filter.get_pos(mask, 240, 50)
		
		# Display
		key = disp.show(frame)
		
		# Handle keys
		if key != -1: print(key)
		green_filter.key_handler(key)
		
		# Manual drive
		if key == [KEY_FORWARD, KEY_BACKWARD, KEY_LEFT, KEY_RIGHT] :
			twist.man(key)
				
		# Drive
		ada_drive.drive(twist) # Not available on laptop
			
	# Check status
	if key == ESC_KEY:
		running = False

cam.release()
disp.close()	

