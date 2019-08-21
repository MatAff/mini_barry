#/usr/bin/env python3

import signal
from visual import Camera, Display, Recorder
from color_filter import Filter
from drive import Twist, Reverse, AdaDrive
from fps import FPS
from reinforcement_learning import RLStateAction

# settings
run_on_pi = False
show_frame = True
filename = "../media/bl_08.avi"
display_delay = 5
rl_batch_size = 1000
filter_values = { 'blue': [[100,182,83],[107,255,241]] }
time_of_day = 'blue'
min_mask_sum = 50
mimic_param = { 'method':'nn', 'layers':[10,5] }
state_action_param = { 'method':'nn', 'layers':[10,5] }
#state_action_param = { 'method':'cnn' }

if run_on_pi:
    show_frame = False
    filename = None

KEY_ESC = 27

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
disp_mask = Display('Barry2', show_frame)
rec = Recorder('./barry.avi', 20, (320, 240), sparse=1)
twist = Twist(forward=0.5)
rev = Reverse(10,30)
ada_drive = AdaDrive()
fpss = FPS(1.0)
c_filter = Filter(filter_values[time_of_day])
#rl = RLStateAction((5, 20), mimic_param, state_action_param)
rl = RLStateAction((5, ), mimic_param, state_action_param)

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
    fpss.update(verbose=True)

    # features
    mask = c_filter.apply_small(frame)
    reward = (mask[2,0:20].sum() + mask[2,1:19].sum() + mask[2,2:18].sum() + mask[2,3:17].sum() +
              mask[2,4:16].sum() + mask[2,5:15].sum() + mask[2,6:14].sum() + mask[2,7:13].sum() +
              mask[2,8:12].sum() + mask[2,9:11].sum())
    row_pos = c_filter.row_pos(mask)

    # set twist
    rotate = row_pos[3] * -0.45

    # reverse if no line
    b = mask.sum() < min_mask_sum
    if rev.update(mask.sum() < min_mask_sum):
        twist.set(-0.55, 0.05)
        print('reversing!')
    else:
        rotate = rl.decide(row_pos, reward, rotate)
        twist.set_rotate(rotate)

    # drive
    ada_drive.drive(twist)
    twist.set_forward(0.35)

    # display and record
    key = disp.show(frame, delay=display_delay)
    key = disp_mask.show(mask, delay=display_delay)
    rec.write(frame)

    # batch update
    if frame_count % rl_batch_size == 0:
        print('new batch')
        ada_drive.stop() # pause driving
        if frame_count > 0 :
            rl.post()
            rl.pre(int(frame_count / rl_batch_size))
    frame_count += 1

    if key == KEY_ESC : running = False

ada_drive.stop()
cam.release()
rec.release()
disp.close()
disp_mask.close()






