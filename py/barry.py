#/usr/bin/env python3

import signal
from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS
from reinforcement_learning import rl_manager

# settings
run_on_pi = False
show_frame = True
filename = "../media/day_light_02.avi"
display_delay = 150
rl_batch_size = 550
filter_values = {'dusk': [[33, 42, 30],[ 98, 178, 70]],
                 'day': [[42, 43, 41],[ 76, 193, 84]],
                 'day_light': [[39, 10, 39], [93, 125, 125]],
                 'night_light': [[39, 71, 39], [93, 221, 221]]}
time_of_day = 'day_light'

if run_on_pi:
    show_frame = False
    filename = None

# set constants
KEY_ESC = 27

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
disp_mask = Display('Barry2', show_frame)
rec = Recorder('./barry.avi', 20, (320, 240), sparse=5)
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()
c_filter = Filter(filter_values[time_of_day])
rl = rl_manager(5, True)

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

    # apply filter
    mask = c_filter.apply_small(frame)
    pos_list = c_filter.row_pos(mask)

    # set twist
    rotate = pos_list[3] * -0.45
    rotate = rl.decide(pos_list, rotate)
    twist.set_rotate(rotate)

    # drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.30)

    # display and record
    key = disp.show(frame, delay=display_delay)
    key = disp_mask.show(mask, delay=display_delay)
    rec.write(frame)

    # batch update
    if frame_count % rl_batch_size == 0:
        print('new batch')
        ada_drive.stop() # pause driving
        rl.switch_batch(int(frame_count / rl_batch_size))

    # check status
    if key == KEY_ESC : running = False

    # update frame count
    frame_count += 1

ada_drive.stop()
cam.release()
rec.release()
disp.close()
disp_mask.close()
