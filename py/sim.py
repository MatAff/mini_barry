#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import time
import numpy as np
import math
import matplotlib.pyplot as plt
from reinforcement_learning import RLStateAction

# Keys
ESC_KEY = 27
KEY_P = 112

# A point should be an np.array with shape (2,)

class Line(object):

    def __init__(self, p1, p2):
        self.points = np.array([p1, p2])

    def get_point(self, pos):
        return(self.points[pos,:])

    # Intersect last line segment with first line segment
    def intersect(self, other):
        CA = self.points[-2,:] - other.points[0,:]
        AB = self.points[-1,:] - self.points[-2,:]
        CD = other.points[1,:] - other.points[0,:]
        denom = np.cross(CD, AB)
        if denom != 0:
            s = np.cross(CA,AB) / denom
            i  = other.points[0,:] + s * CD
            overlap = self.in_range(i) and other.in_range(i)
            return(i, True, overlap)
        else:
            return None, False, False

    def in_range(self, p):
        return(((self.points[0,:] <= p)==(p <= self.points[1,:])).all())

class Spline(object):

    def __init__(self, l1, l2, n):
        self.points = np.zeros((n,2))
        B = l1.get_point(-1)
        C = l2.get_point(0)
        I, _, _ = l1.intersect(l2)
        for i in range(n):
            ratio = i / (n-1)
            S = self.rel_line(B, I, ratio)
            E = self.rel_line(I, C, ratio)
            P = self.rel_line(S, E, ratio)
            self.points[i,:] = P

    def rel_line(self, S, E, ratio):
        return(S + (E - S) * ratio)

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

class Course(object):

    def __init__(self):
        line_list = []
        sections = [Line(np.array([0,0]), np.array([1,0])),
                    Line(np.array([5,5]), np.array([4,6.5])),
                    Line(np.array([-4,6]), np.array([-5,5]))]

        for i, sect in enumerate(sections):
            spline = Spline(sections[i-1], sect, 25)
            line_list.append(spline.points)
            line_list.append(sect.points)

        self.points = np.concatenate(line_list)

    def draw(self, frame):
        draw_line(frame, self.points, (255,0,0))

# Function to convert cartesian coordinate into pixel coordinates
def to_pixel(cart):
    S = np.array([scale, -scale])
    T = np.array([320, 480 - 80])
    return(tuple((cart * S + T).astype(int)))

def draw_line(frame, points, color):
    for i in range(points.shape[0] - 1):
        s_pix = to_pixel(points[i+0,:])
        e_pix = to_pixel(points[i+1,:])
        try:
            cv2.line(frame, s_pix, e_pix,color,2)
        except Exception as e:
            print(points)
            print(s_pix, e_pix)
            raise e

def rotation(rad):
    return(np.matrix([[math.cos(rad), -math.sin(rad)],
                      [math.sin(rad),  math.cos(rad)]]))

class Car(object):

    def __init__(self):
        self.pos = np.array([[0],[0]])
        self.dir = np.array([[1],[0]])

    def move(self, x, rad):
        self.pos = self.pos + x * self.dir * 0.5
        self.dir = np.matmul(rotation(rad), self.dir)
        self.pos = self.pos + x * self.dir * 0.5

    def draw(self, frame):
        tl = self.pos + np.matmul(rotation(math.pi *  0.5), self.dir * 0.3)
        tr = self.pos + np.matmul(rotation(math.pi * -0.5), self.dir * 0.3)
        bl = self.pos - self.dir + np.matmul(rotation(math.pi *  0.5), self.dir * 0.3)
        br = self.pos - self.dir + np.matmul(rotation(math.pi * -0.5), self.dir * 0.3)
        points = np.array(np.concatenate([tl, tr, br, bl, tl, br, bl, tr], axis=1).transpose())
        draw_line(frame, points, (0,0,255))

    def detect(self, points, frame, dist):

        # Create detection line
        sp = self.pos + np.matmul(rotation(math.pi * -0.25), self.dir * dist)
        ep = self.pos + np.matmul(rotation(math.pi *  0.25), self.dir * dist)
        sp = np.squeeze(np.array(sp))
        ep = np.squeeze(np.array(ep))
        detect_line = Line(sp, ep)

        # Draw detection line
        draw_line(frame, detect_line.points, (0,200,0))

        # Loop through course
        for i in range(points.shape[0] - 1):
            sub_line = Line(points[i,:], points[i+1,:])
            inters, has_intersect, overlap = detect_line.intersect(sub_line)
            if overlap == True:
                pos = np.linalg.norm(inters - sp) / np.linalg.norm(ep - sp)
                return((pos - 0.5) * 2.0)

    def detect_list(self, points, frame, dist_list):
        return([self.detect(points, frame, dist) for dist in dist_list])

class Retainer(object):

    def __init__(self, data):
        self.prev = data

    def retain(self, current):
        current = current.astype('float')
        current[np.isnan(current)] = self.prev[np.isnan(current)]
        self.prev = current
        return(current)

def pos_to_reward(line_pos):
    pos = np.array(line_pos).astype('float')
    pos[np.isnan(pos)] = -3.0
    return np.abs(pos)[0] * -1.0

####################
### MAIN SECTION ###
####################

# Display settings
frame_name = 'Sim'
cv2.namedWindow(frame_name)
height = 480
width = 640
scale = 35

# Global red
glob_rec = Recorder('RL.avi', 30, (width, height))
rec_run = [0,1,2,5,10,20,50]

# Run settings
nr_runs = 10000
frames_per_run = 500
running = True

# Instantiate sim and control elements
course = Course()
dist_list = [0.5, 1.0, 1.5, 2.0, 2.5]
model_param = { 'method':'reg', 'layers':[10,5] }
rl = RLStateAction((len(dist_list),), model_param)

# Loop through runs
for run in range(nr_runs):

    # Reset
    print(run)
    car = Car()
    rl.pre(run)

    # Recored
    filename = './run_%03i.avi' % run
    rec = Recorder(filename, 30, (width, height))

    # set retainer
    ret = Retainer(np.zeros(len(dist_list))) # set retrainer

    # Main loop
    for frame_nr in range(frames_per_run):

        try:

            # Plot course and car
            frame = np.zeros((height, width,3), np.uint8)
            course.draw(frame)
            car.draw(frame)

            # Detect and plot detect
            line_pos = car.detect_list(course.points, frame, dist_list)
            reward = pos_to_reward(line_pos) # get rewards
            line_pos = ret.retain(np.array(line_pos)) # insert retained values

            # Show
            frame = cv2.putText(frame, 'Run %i' % run, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 1)
            rec.write(frame)
            if run in rec_run : glob_rec.write(frame)
            cv2.imshow(frame_name, frame)
            key = cv2.waitKey(5)
            if key != -1 : print(key)

            # Process key
            if key == ESC_KEY : raise ValueError('ESC pressed')
            if key == KEY_P : rec.save_img(frame)

            # Decide
            rotate = line_pos[1] * 0.1
            rotate = rl.decide(line_pos, reward, rotate)

            # Act
            car.move(0.2, rotate)

        except Exception as e:

            print(e)
            running = False
            break

    # Control
    rl.post()

    # Plot
    #plt.plot(rl.mean_reward_list)
    #plt.show()

    # Recorder
    rec.release()
    glob_rec.release()

    if running == False : break

cv2.destroyWindow(frame_name)

