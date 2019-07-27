#/usr/bin/env python3

import signal

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS
from reinforcement_learning import rl_manager

# settings
run_on_pi = True
show_frame = True
show_mask_small = True
annotate = True
filename = "../media/headlamp_07.avi"
display_delay = 150
rl_batch_size = 550
filter_values = {'dusk': [[33, 42, 30],[ 98, 178, 70]],
                 'day': [[42, 43, 41],[ 76, 193, 84]],
                 'head': [[39, 71, 39], [93, 221, 221]]}
time_of_day = 'head'

if run_on_pi:
    show_frame = False
    show_mask_small = False
    annotate = False
    filename = None

# set constants
KEY_ESC = 27
SENSE_HEIGHT_LIST = [230,210,190,170,150,130]
#SENSE_HEIGHT_LIST = [175]
SENSE_WIDTH = 10

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
disp_mask = Display('Barry2', show_mask_small)
rec = Recorder('./barry.avi', 20, (320, 240), sparse=5)
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()
c_filter = Filter(filter_values[time_of_day])
rl = rl_manager(len(SENSE_HEIGHT_LIST), True)

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
    mask = c_filter.apply(frame, False, False)
    pos_list = c_filter.get_block_pos(mask, SENSE_HEIGHT_LIST, SENSE_WIDTH)
    block_line_list = c_filter.get_lines()

    # apply
    mask_small = c_filter.apply_small(frame)

    # set rotate
    if pos_list[3] is not None:
        rotate = pos_list[3] * -0.45
    else:
        rotate = 0

    # reinforcement learning
    rotate = rl.decide(pos_list, rotate)

    # set twist
    twist.set_rotate(rotate)
    #l = twist.as_line()

    # drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.30)

    # SHARE - display
    show_frame = frame
    if annotate:
        #show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
        #show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
        show_frame = Annotate.add_lines_list(show_frame, block_line_list, (0, 0, 255))
        #show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 2)
        #show_frame = Annotate.add_text(show_frame, twist.to_string(), (0, 255, 0), 3)
    key = disp.show(show_frame, delay=display_delay)
    key = disp_mask.show(mask_small, delay=display_delay)

    # record
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
disp_mask.close()
