#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import os


class Camera(object):

    def __init__(self, width=320, height=240, filename=None):
        self.width = width
        self.height = height

        if filename is None:
            self.vc = cv2.VideoCapture(0)
            self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        else:
            assert os.path.exists(filename), "file not found: " + filename
            print("running from recording: " + filename)
            self.vc = cv2.cv2.VideoCapture(filename)

    def get(self):
        rval, frame = self.vc.read()
        if rval:
            return frame
        else:
            print('frame not captured')
            return np.zeros((self.height, self.width, 3))

    def release(self):
        self.vc.release()


class Display(object):

    def __init__(self, window_name, show_frame=True):
        self.show_frame = show_frame
        if self.show_frame:
            self.name = window_name
            cv2.namedWindow(self.name)

    def show(self, frame, delay=5):
        if self.show_frame:
            cv2.imshow(self.name, frame)
            key = cv2.waitKey(delay)
            return key

    def close(self):
        if self.show_frame:
            cv2.destroyWindow(self.name)


class Recorder(object):

    def __init__(self, filename, fps, size, sparse=1):
        self.sparse = sparse
        self.count = 0
        self.out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    def write(self, frame):
        if self.count % self.sparse == 0:
            self.out.write(frame)
        self.count += 1

    def save_img(self, frame, filename=None):
        if filename is None : filename = str(time.time()) + '.png'
        cv2.imwrite(filename, frame)

    def release(self):
        self.out.release()


class Annotate(object):

    @staticmethod
    def add_lines_list(frame, lines_list, color):
        for lines in lines_list:
            for l in lines:
                frame = Annotate.add_line(frame, l, color)
        return frame

    @staticmethod
    def add_multiple_lines(frame, lines, color):
        for l in lines:
            frame = Annotate.add_line(frame, l, color)
        return frame

    @staticmethod
    def add_line(frame, line, color):
        S, E = line
        frame = cv2.line(frame, S, E, color, 2)
        return frame

    @staticmethod
    def add_text(frame, text, color, line_nr):
        font = cv2.FONT_HERSHEY_SIMPLEX
        pos = (10, line_nr * 20)
        frame = cv2.putText(frame, text, pos, font, 0.5, color, 1)
        return frame
