#/usr/bin/env python3

import signal

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS
from reinforcement_learning import rl_manager

# settings
show_frame = True # toggle to switch off/on display
#show_frame = False
filename = "../media/first_circle.avi"
#filename = None
display_delay = 50
rl_batch_size = 50
#filter_values = [[15, 15, 53], [80, 137, 137]]
filter_values = [[44, 50, 26],[ 75, 222, 132]]

# keys
KEY_ESC = 27

# set constants
SENSE_HEIGHT_LIST = [470, 450, 430, 410, 390, 370, 350, 330, 310]
SENSE_WIDTH = 10

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
rec = Recorder('./barry.avi', 20, (640, 480), sparse=5)
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()
c_filter = Filter(filter_values)
rl = rl_manager(len(SENSE_HEIGHT_LIST), False)

# initialize variables
running = True
key = -1
frame_count = 0

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        global running
        running = False

signal.signal(signal.SIGINT, signal_handler)

while running:

    # SENSE - get frame
    frame = cam.get()
    fpss.update()

    # DECIDE - apply filter and get position
    mask_frame, mask = c_filter.apply(frame, True, False)
    pos_list = c_filter.get_block_pos(mask, SENSE_HEIGHT_LIST, SENSE_WIDTH)
    block_line_list = c_filter.get_lines()

    # DECIDE - set drive
    if pos_list[3] is None:
        rotate = 0
    else:
        rotate = pos_list[3] * -0.15

    # DECIDE - reinforcement learning
    rl.decide(pos_list, rotate)

    # ACT - set twist
    twist.set_rotate(rotate)
    l = twist.as_line()

    # ACT - drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.25)

    # SHARE - display
    show_frame = frame
    #show_frame = mask_frame
    show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
    show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
    show_frame = Annotate.add_lines_list(show_frame, block_line_list, (0, 0, 255))
    show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 2)
    show_frame = Annotate.add_text(show_frame, twist.to_string(), (0, 255, 0), 3)
    key = disp.show(show_frame, delay=display_delay)

    # SHARE - record
    rec.write(show_frame)

    # batch update
    if frame_count % rl_batch_size == 0:
        print('new batch')
        ada_drive.stop() # pause driving
        rl.switch_batch(int(frame_count / rl_batch_size))

    # check status
    if key == KEY_ESC:
        running = False

    # update frame count
    frame_count += 1

ada_drive.stop()
cam.release()
rec.release()
disp.close()

#print('Press Ctrl+C')
#signal.pause()


# Barry RL plan
# sense in five positions instead of 1
# still set rotate manually as done currently
# create and instance of a high level RL class
# pass in 5 sense and manual rotation
# class stores input
# return updated rotate (based on phase)

# 3 phases
# 1 manual
# 2 imitate
# 3 improve

# use batch process to stay close to original design
# every 100 frames?




