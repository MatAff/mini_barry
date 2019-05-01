#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

H_KEY = 104
S_KEY = 115
V_KEY = 118
PLUS_KEY = 43 
MIN_KEY = 45

class filter(object):
	
	def __init__(self, lower, upper):
		self.bounds = {'lower': np.array(lower), 'upper': np.array(upper)}
		self.change = ('lower',0)
		self.delta = 5

	def apply(self, bgr_frame, erode=False, dilate=False):    
		hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_frame, self.bounds['lower'], self.bounds['upper'])
		
		if erode == True:
			kernel = np.ones((5,5),np.uint8)
			mask = cv2.erode(mask,kernel,iterations = 1)
		
		if dilate == True:
			kernel = np.ones((5,5),np.uint8)
			mask = cv2.dilate(mask,kernel,iterations = 1)
		
		res = cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)
		
		return(res, mask)		
		
	def key_handler(self, key):		
		if key == H_KEY: 
			print('Pressed h')
			if self.change[0] == 'lower':
				self.change = ('upper', 0)
			else:
				self.change = ('lower', 0)
		if key == S_KEY: 
			print('Pressed s')
			if self.change[0] == 'lower':
				self.change = ('upper', 1)
			else:
				self.change = ('lower', 1)
		if key == V_KEY: 
			print('Pressed v')
			if self.change[0] == 'lower':
				self.change = ('upper', 2)
			else:
				self.change = ('lower', 2)		
		elif key == PLUS_KEY:
			print('Pressed +') 
			self.bounds[self.change[0]][self.change[1]] = self.bounds[self.change[0]][self.change[1]] + self.delta 
			print(self.bounds)
		elif key == MIN_KEY:
			print('Pressed -') 
			self.bounds[self.change[0]][self.change[1]] = self.bounds[self.change[0]][self.change[1]] - self.delta 
			print(self.bounds)

 
