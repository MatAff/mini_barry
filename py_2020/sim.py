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
dist_list = [5, 10, 20, 40, 80]
car = Car(dist_list)

# initialize controller
# controller = EngineeredControl()
# controller = TestDrive()
controller = RL(len(dist_list))

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
    print(act_dict)
    
    # act
    car.move(act_dict)    

    # feedback
    key = display.show(frame)
    running = (key != KEY_ESC)
    recorder.write(frame)
    fps.get_fps(verbose=False)

recorder.release()
display.close()

# line_pos = line_pos[0:5]
# line_pos = controller.ret.retain(np.array(line_pos))

# line_pos = np.append(line_pos, [0.2])

# rotate_range = np.arange(-0.5, 0.5, 0.05)
# res = np.repeat([line_pos], len(rotate_range), axis=0)
# res.shape
# res = np.append(res, np.array([rotate_range]).T, axis=1)

# res.shape

# pred = controller.model.predict(res)

# mu = controller.action.mean(axis=0)[1]
# sd = controller.action.std(axis=0)[0]

# import scipy

# prob = scipy.stats.norm(mu, sd).pdf(rotate_range)
# np.round(prob**0.25, 2)

# res.shape

# probs = pred / prob**0.05

# import matplotlib.pyplot as plt

# plt.plot(pred)
# plt.plot(prob)
# plt.plot(probs)

# np.argmin(probs)

#  np.array([rotate_range]).shape

