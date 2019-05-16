#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time

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
        
class Recorder(object):
    
    def __init__(self, filename, fps, size):
        self.out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    def write(self, frame):
        self.out.write(frame)
        
    def save_img(self, frame, filename=None):
        if filename is None : filename = str(time.time()) + '.png'
        cv2.imwrite(filename, frame)
        
    def release(self):
        self.out.release()
