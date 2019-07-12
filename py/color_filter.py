#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

H_KEY = 104
S_KEY = 115
V_KEY = 118
PLUS_KEY = 171 #43
MIN_KEY = 173 # 45

class Filter(object):

    def __init__(self, lower, upper):
        self.bounds = np.array([lower, upper])
        self.change = [0,0]
        self.delta = 5

    def apply(self, bgr_frame, erode=False, dilate=False):
        hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, self.bounds[0,:], self.bounds[1,:])

        if erode == True:
            kernel = np.ones((5,5),np.uint8)
            mask = cv2.erode(mask,kernel,iterations = 1)

        if dilate == True:
            kernel = np.ones((5,5),np.uint8)
            mask = cv2.dilate(mask,kernel,iterations = 1)

        res = cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)

        return(res, mask)

    def key_handler(self, key):
        if key == H_KEY: self.change = [1 - self.change[0], 0]
        if key == S_KEY: self.change = [1 - self.change[0], 1]
        if key == V_KEY: self.change = [1 - self.change[0], 2]
        elif key == PLUS_KEY:
            self.bounds[tuple(self.change)] = self.bounds[tuple(self.change)] + self.delta
            print(self.bounds)
        elif key == MIN_KEY:
            self.bounds[tuple(self.change)] = self.bounds[tuple(self.change)] - self.delta
            print(self.bounds)

    def get_block_pos(self, mask, height, stroke=10):
        top = int(height - stroke / 2)
        bottom = int(height + stroke / 2)
        nr_blocks = 21.0
        block_width = mask.shape[1] / nr_blocks
        block_counts = np.zeros(int(nr_blocks))
        for b in range(int(nr_blocks)):
            count = np.sum(mask[int(top): int(bottom),
                          int(b * block_width):int((b + 1) * block_width)])
            block_counts[b] = count
        block_counts[10] += 10
        max_b = np.argmax(block_counts)

        left, right = int(max_b * block_width), int((max_b + 1) * block_width)
        self.lines = [((0, top), (640, top)), ((0, bottom),
                       (640, bottom)),((left, top), (left, bottom)), ((right, top), (right, bottom))]

        return max_b / nr_blocks * 2.0 - 1.0

    def get_pos(self, mask, height, stroke=10):
        sum = 0
        count = 0
        width = mask.shape[1]
        for x in range(width):
            block_count = np.sum(mask[int(height - stroke / 2): int(height + stroke / 2), x: x+1])
            sum = sum + block_count * x
            count = count + block_count

        if count > 0:
            return float(sum) / count
        else:
            return -1

    def get_lines(self):
        return self.lines

