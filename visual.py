#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

class Camera(object):
	
	def __init__(self):
		self.vc = cv2.VideoCapture(0)		

	def get(self):
		return self.vc.read()
	
	def release(self):
		self.vc.release()

class Display(object):
	 
	def __init__(self):
		self.name = "barry"
		cv2.namedWindow(self.name)		
	
	def show(self, frame):
		cv2.imshow(self.name, frame)
		key = cv2.waitKey(20)
		return key
	
	def close(self):
		cv2.destroyWindow(self.name)	