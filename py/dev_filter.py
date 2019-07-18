#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from color_filter import Filter
from scipy.stats.mstats_basic import winsorize
import random

KEY_ESC = 27
KEY_SPACE = 32

### FUNCTIONS ###

def pull_video_imgs(filename):

    if not os.path.exists(filename):
        raise ValueError("file not found: " + filename)

    cap = cv2.VideoCapture(filename)

    img_list = []

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            img_list.append(frame)
            cv2.imshow('frame',frame)
            cv2.waitKey(1)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print('images found: %i' % len(img_list))

    return img_list

def random_imgs(img_list, n=32):
    size = len(img_list)
    img_nrs = random.sample(range(size), n)
    return np.array(img_list)[img_nrs]

def resize_img_list(img_list, size):
    return [cv2.resize(img, size) for img in img_list]

def crop_imgs(img_list):
    return [img[120:240, 0:320] for img in img_list]

def merge_images(img_list, nrow, ncol):
    rows = []
    for r in range(nrow):
        for c in range(ncol):
            img_nr = r * ncol + c
            if c == 0:
                row_img = img_list[img_nr]
            else:
                append_img = img_list[img_nr]
                row_img = np.concatenate((row_img, append_img), axis=1)
            if c == ncol - 1:
                rows.append(row_img)
    for r in range(nrow):
        if r == 0:
            img = rows[r]
        else:
            append_img = rows[r]
            img = np.concatenate((img, append_img), axis=0)
    return img

def show_big(img):
    plt.figure(figsize=(27,18))
    plt.imshow(img)
    plt.show()

def get_ranges(colors):
    col_arr = np.vstack(colors)
    col_arr = winsorize(col_arr, (.05, .05))
    col_arr = np.array(col_arr)
    min_hsv = col_arr.min(axis=0)
    max_hsv = col_arr.max(axis=0)
    return [min_hsv, max_hsv]

def apply_filter(img, ranges):
    filter = Filter(ranges)
    mask_frame, mask = filter.apply(img, False, False)
    return mask_frame

def interactive_explore(img):

    show_full = True
    l_colors = []
    r_colors = []

    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    masked_frame = img

    def mouse_click(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
            l_colors.append(hsv_frame[y,x])
        if event == cv2.EVENT_RBUTTONDOWN: #checks mouse left button down condition
            r_colors.append(hsv_frame[y,x])

    cv2.namedWindow('explore')
    cv2.setMouseCallback('explore',mouse_click)

    running = True
    while(running):
        if show_full:
            cv2.imshow('explore',img)
        else:
            if len(l_colors) > 4:
                ranges = get_ranges(l_colors)
                print(ranges)
                masked_frame = apply_filter(img, ranges)
            cv2.imshow('explore',masked_frame)
        key = cv2.waitKey(20)
        if key == KEY_SPACE:
            show_full = not show_full
        if key == KEY_ESC:
            running = False

    cv2.destroyAllWindows()

    print("got here")

    ranges = get_ranges(l_colors)
    print(ranges)
    return get_ranges(ranges)

def click_filter(filename):
    all_imgs = pull_video_imgs(filename)
    select_imgs = random_imgs(all_imgs, 32)
    resized_imgs = resize_img_list(select_imgs, (320,240))
    resized_imgs = crop_imgs(resized_imgs)
    img = merge_images(resized_imgs, 8, 4)
    ranges = interactive_explore(img)
    return ranges

### PROCESS ###

# steps
# get images from video
# select random images
# select image to evaluate
# resize and merge
# click process

### MAIN ###

#filename = '../media/dim.avi'
#filename = '../media/late_afternoon.avi'
#filename = '../media/late_afternoon2.avi'
#filename = '../media/late_afternoon_3.avi'
filename = "../media/first_circle.avi"

values = click_filter(filename)
print(values)
