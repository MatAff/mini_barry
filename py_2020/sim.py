#!/usr/bin/env python3

import numpy as np

import cv2

from control import EngineeredControl, TestDrive, RL
from fps import FPS
from sim_elements import Course, Car, Draw
from visual import Display, Recorder

KEY_ESC = 27

fps = FPS(20.0)

# initialize visual elements
width, height = 320, 240
display = Display('sim', True)
recorder = Recorder('sim.avi', 30, (width, height))

# initialize simulation related element
Draw.set_param(2, width, height)
course = Course()
car = Car(dist_list=[5, 10, 20, 40, 80])

# initialize controller
# controller = EngineeredControl()
# controller = TestDrive()
controller = RL()

running = True
while running:

    # Plot course and car
    frame = np.zeros((height, width, 3), np.uint8)
    course.draw(frame)
    car.draw(frame)

    # input
    line_pos = car.detect_list(course.points, frame)

    # control
    act_dict = controller.decide(line_pos)
    
    # act
    car.move(act_dict)    

    # feedback
    key = display.show(frame)
    running = (key != KEY_ESC)
    recorder.write(frame)
    fps.get_fps()

recorder.release()
display.close()
