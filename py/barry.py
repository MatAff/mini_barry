#/usr/bin/env python3

import signal

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS
#from reinforcement_learning import rl_manager

# settings
run_on_pi = True
show_frame = True
annotate = True
filename = "./day_08.avi"
display_delay = 150
#rl_batch_size = 550
filter_values = {'dusk': [[33, 42, 30],[ 98, 178, 70]],
                 'day': [[42, 43, 41],[ 76, 193, 84]],
                 'head': [[39, 71, 39], [93, 221, 221]]}
time_of_day = 'head'

if run_on_pi:
    show_frame = False
    annotate = False
    filename = None

# set constants
KEY_ESC = 27
#SENSE_HEIGHT_LIST = [470, 450, 430, 410, 390, 370, 350, 330, 310]
SENSE_HEIGHT_LIST = [350]
SENSE_WIDTH = 20

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
rec = Recorder('./barry.avi', 20, (640, 480), sparse=5)
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()
c_filter = Filter(filter_values[time_of_day])
#rl = rl_manager(len(SENSE_HEIGHT_LIST), True)

# initialize variables
running = True
key = -1
frame_count = 0
rotate = 0

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

while running:

    # get frame
    frame = cam.get()
    print(fpss.update())

    # apply filter and get position
    mask_frame, mask = c_filter.apply(frame, True, False)
    pos_list = c_filter.get_block_pos(mask, SENSE_HEIGHT_LIST, SENSE_WIDTH)
    #block_line_list = c_filter.get_lines()

    # set rotate
    if pos_list[0] is not None:
        rotate = pos_list[0] * -0.10
    else:
        rotate = 0

    # reinforcement learning
    #rotate = rl.decide(pos_list, rotate)

    # set twist
    twist.set_rotate(rotate)
    #l = twist.as_line()

    # drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.25)

    # SHARE - display
    show_frame = frame
    #if annotate:
    #    show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
    #    show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
    #    show_frame = Annotate.add_lines_list(show_frame, block_line_list, (0, 0, 255))
    #    show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 2)
    #    show_frame = Annotate.add_text(show_frame, twist.to_string(), (0, 255, 0), 3)
    #key = disp.show(show_frame, delay=display_delay)

    # record
    rec.write(show_frame)

    # batch update
    #if frame_count % rl_batch_size == 0:
    #    print('new batch')
    #    ada_drive.stop() # pause driving
    #    rl.switch_batch(int(frame_count / rl_batch_size))

    # check status
    if key == KEY_ESC:
        running = False

    # update frame count
    frame_count += 1

ada_drive.stop()
cam.release()
rec.release()
disp.close()
