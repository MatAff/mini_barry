#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob

from color_filter import *

# Select files
files = glob.glob('*png')

# Load data
images = [cv2.imread(file) for file in files]

## Show image using opencv
#cv2.imshow('image',images[0])
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
## Show image using matplotlib
#plt.imshow(images[1])

# Function to show images
def picshow(images):
	num = len(images)
	ax = np.ceil(np.sqrt(num)) 
	ay = np.rint(np.sqrt(num)) 
	fig = plt.figure()
	for i in range(num):
		sub = fig.add_subplot(ax,ay,i + 1)        
		sub.axis('off')
		sub.imshow(images[i])
	#fig.set_size_inches(np.array(fig.get_size_inches())*num)
	fig.set_size_inches(np.array(fig.get_size_inches())*3)
	plt.show(fig)

## Show images
#picshow(images)
#
## Initialize filter
#green_filter = Filter([30, 50, 0], [55, 260, 255]) # Daytime 
#
## Initialize alternative filter
#green_filter = Filter([30, 0, 0], [55, 260, 255]) # Daytime 
#
## Process images
#proc_images = [green_filter.apply(img)[0] for img in images[0:4]]
#
## Show images
#picshow(proc_images)
	
### PLAYGROUND ###

def filt(bgr_frame):
	
	# Smooth	
	bgr_frame = cv2.GaussianBlur(bgr_frame,(15,15),0)
	
	# Convert to hsv
	hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
	
	# Smooth		
	#kernel = np.ones((5,5),np.float32)/225
	#hsv_frame = cv2.filter2D(hsv_frame,-1,kernel)
	
	# hsv filter
	bounds = np.array([[25, 30, 50], [55, 255, 255]])
	mask = cv2.inRange(hsv_frame, bounds[0,:], bounds[1,:])

	# Erode
	#kernel = np.ones((5,5),np.uint8)
	#mask = cv2.erode(mask,kernel,iterations = 1)
		
	# Dilate
	#kernel = np.ones((5,5),np.uint8)
	#mask = cv2.dilate(mask,kernel,iterations = 1)
		
	bgr_frame = cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)
		
	return(bgr_frame)		
	
proc_images = [filt(img) for img in images]

# Show images
picshow(proc_images)
#picshow(images)



#
	