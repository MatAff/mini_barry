#!/usr/bin/env python3

import cv2
import numpy as np

from visual import *
from color_filter import *

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
		
		# Get position
		print('pos')
		avg_pos = green_filter.get_pos(mask, 240, 50)
		
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

