#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

class Filter(object):

    def __init__(self, ranges):
        self.bounds = np.array(ranges)

    def apply(self, bgr_frame):
        hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv_frame, self.bounds[0,:], self.bounds[1,:])

    def apply_small(self, bgr_frame):
        lower_frame = bgr_frame[120:240, 0:320] # crop
        hsv_frame = cv2.cvtColor(lower_frame, cv2.COLOR_BGR2HSV) # hsv
        mask = cv2.inRange(hsv_frame, self.bounds[0,:], self.bounds[1,:]) # mask
        mask_small = mask.reshape(5, 24, 20, 16).mean(axis=(1,3)) # reduce size
        return mask_small

    def apply_mask(self, bgr_frame, mask):
        return cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)

    def row_pos(self, mask):
        cols = mask.shape[1]
        mask[:,int(cols/2)] += 0.0001 # ensure middle is select if missing
        max_pos = np.argmax(mask, 1)
        return max_pos / (cols - 1) * 2.0 - 1.0
