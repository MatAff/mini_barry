#!/usr/bin/env python3

import numpy as np

import cv2

from control import EngineeredControl
from fps import FPS
from sim_elements import Course, Car
from visual import Display, Recorder

KEY_ESC = 27

fps = FPS(20.0)

width, height = 640, 480
display = Display('sim', True)
recorder = Recorder('sim.avi', 30, (width, height))

course = Course()
car = Car(dist_list=[0.5, 1.0, 1.5, 2.0, 2.5])

controller = EngineeredControl()

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
