#!/usr/bin/env python3

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS

# keys
KEY_ESC = 27
KEY_FORWARD = 82
KEY_BACKWARD = 84
KEY_LEFT = 81
KEY_RIGHT = 83
KEY_P = 112

# set constants
SENSE_HEIGHT = 400
SENSE_WIDTH = 10

# initialize variables
running = True
key = -1

# initialize objects
cam = Camera()
disp = Display('Barry')
rec = Recorder('./barry.avi', 20, (640, 480))
twist = Twist()
ada_drive = AdaDrive()
fpss = FPS()

#green_filter = Filter([20,0,20], [70,255,255])
green_filter = Filter([25, 30, 50], [55, 255, 255]) # Daytime

while running:

    # SENSE - get frame
    frame = cam.get()

    # DECIDE - apply filter and get position
    mask_frame, mask = green_filter.apply(frame, True, False)
    pos = green_filter.get_block_pos(mask, SENSE_HEIGHT, SENSE_WIDTH)
    block_lines = green_filter.get_lines()

    # DECIDE - aet drive
    rotate = pos * -0.2
    twist.set_rotate(rotate)
    l = twist.as_line()

    # SHARE - display
    show_frame = mask_frame
    show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
    show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
    show_frame = Annotate.add_multiple_lines(show_frame, block_lines, (0, 0, 255))
    show_frame = Annotate.add_text(show_frame, 'position %.3f' % pos, (0, 255, 0), 2)
    show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 3)
    key = disp.show(show_frame)

	# SENSE - handle keys
    if key != -1:
        print(key)
        if key == KEY_P : rec.save_img(frame)
        green_filter.key_handler(key)

    # DECIDE - manual drive
    if key in [KEY_FORWARD, KEY_BACKWARD, KEY_LEFT, KEY_RIGHT] :
        twist.man(key)
        twist.print()

	# ACT - drive
    ada_drive.drive(twist) # Not available on laptop

	# SHARE - record
    rec.write(show_frame)

    # check status
    if key == KEY_ESC:
        running = False

ada_drive.stop()
cam.release()
rec.release()
disp.close()

