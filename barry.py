#!/usr/bin/env python3

import cv2
import numpy as np

from visual import *
from color_filter import *
from drive import * # Not available on laptop 

ESC_KEY = 27

KEY_FORWARD = 82
KEY_BACKWARD = 84
KEY_LEFT = 81
KEY_RIGHT = 83

KEY_P = 112

running = True
key = ESC_KEY

cam = Camera()
disp = Display()
rec = Recorder('./barry.avi', 20, (640, 480))
twist = Twist()
ada_drive = AdaDrive() # Not available on laptop

#green_filter = Filter([20,0,20], [70,255,255])
green_filter = Filter([30, 50, 0], [55, 260, 255]) # Daytime 

while running:
    
    # Get frame
    rval, frame = cam.get()
    
    if rval == True:
        
        # Record
        rec.write(frame)
        ori_frame = frame
        
        # Apply filter
        frame, mask = green_filter.apply(frame, True, False)
        print(frame.shape)
        
        # Get position
        avg_pos = green_filter.get_pos(mask, 300, 50)
        print(avg_pos)

        # Set drive
        rotate = (avg_pos - 320.0) / -320.0 * 0.02
        print(rotate)
        twist.set_rotate(rotate)
        
        # Display
        key = disp.show(frame)
        
        # Handle keys
        if key != -1: 
            print(key)
            if key == KEY_P : rec.save_img(ori_frame)
            green_filter.key_handler(key)
        
        # Manual drive
        if key in [KEY_FORWARD, KEY_BACKWARD, KEY_LEFT, KEY_RIGHT] :
            twist.man(key)
            twist.print()
                
        # Drive
        ada_drive.drive(twist) # Not available on laptop
            
    # Check status
    if key == ESC_KEY:
        running = False

ada_drive.stop()
cam.release()
rec.release()
disp.close()    

