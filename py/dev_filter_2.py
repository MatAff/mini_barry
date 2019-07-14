#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import math
from color_filter import Filter

# steps
# load possible images
# select image to evaluate
# merge image into one
# apply filter

# TODO: create class for this work?
# TODO: add method to load images from folder

def imgs_from_video(filename):
    # TODO

    cap = cv2.VideoCapture(filename)

    img_list = []

    while(cap.isOpened()):
        ret, frame = cap.read()

        if ret == True:
            img_list.append(frame)
            cv2.imshow('frame',frame)
            cv2.waitKey(100)
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print('images found: %i' % len(img_list))

    return img_list

def show_numbered_imgs(img_list):
    for i, img in enumerate(img_list):
        print(i)
        plt.imshow(img)
        plt.show()

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

def multiplot(imgs, n_row, n_col, size):
    n = n_row * n_col
    imgs = imgs[0:n]
    _, axs = plt.subplots(n_row, n_col, figsize=size)
    axs = axs.flatten()
    for img, ax in zip(imgs, axs):
        ax.imshow(img)
    plt.show()

def show_filtered_imgs(green_filter, img_list):
    count = 0
    for img in img_list:
        count += 1
        print(count)
        mask_frame, mask = green_filter.apply(img, False, False)
        masked_imgs.append(mask_frame)
        plt.imshow(mask_frame)
        plt.show()

def mouse_explore(image, display_img):
    # code reference: https://pastebin.com/MJfWmD6W

    hsv_frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def mouseRGB(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
            colorsB = image[y,x,0]
            colorsG = image[y,x,1]
            colorsR = image[y,x,2]
            colors = image[y,x]
            print("Red: ",colorsR)
            print("Green: ",colorsG)
            print("Blue: ",colorsB)
            print("BRG Format: ",colors)
            print("HSV Format: ", hsv_frame[y,x])
            print("Coordinates of pixel: X: ",x,"Y: ",y)

    # Read an image, a window and bind the function to window
    cv2.namedWindow('mouseRGB')
    cv2.setMouseCallback('mouseRGB',mouseRGB)

    #Do until esc pressed
    while(1):
        cv2.imshow('mouseRGB',display_img)
        if cv2.waitKey(20) & 0xFF == 27:
            break
    #if esc pressed, finish.
    cv2.destroyAllWindows()

# set file name
os.listdir('../media')
#filename = '../media/daylight_short.avi'
filename = '../media/dim.avi'

# load all images
img_list = imgs_from_video(filename)

# show images
show_numbered_imgs(img_list)

# select images
select_img_nrs = [0,5, 10, 20, 25, 30, 40, 50, 60]
print(len(select_img_nrs))
select_imgs = np.array(img_list)[select_img_nrs]
print(len(select_imgs))

# crop
select_imgs = [img[240:480, 0:640] for img in select_imgs]

# merge images
img = merge_images(select_imgs, 3, 3)
show_big(img)

# apply filter
green_filter = Filter([30, 50, 100], [65, 200, 160]) # Daytime
green_filter = Filter([35, 50, 30], [85, 200, 160]) # Dim
mask_frame, mask = green_filter.apply(img, False, False)

# show filtered img
show_big(mask_frame)

# mouse exploration
mouse_explore(img, mask_frame)















