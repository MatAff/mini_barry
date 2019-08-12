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
filename = "../media/bl_07.avi"
display_delay = 5
rl_batch_size = 1500
filter_values = {'dusk': [[33, 42, 30],[ 98, 178, 70]],
                 'day': [[42, 43, 41],[ 76, 193, 84]],
                 'day_light': [[39, 10, 39], [93, 125, 125]],
                 'night_light': [[39, 71, 39], [93, 221, 221]],
                 'night_light2': [[47,52,84],[90,165,254]],
                 'blue': [[100,182,83],[107,255,241]]
                 }
time_of_day = 'blue'
min_mask_sum = 50

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
rl = RLStateAction(100, layers=[10,5])

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

    # apply filter
    mask = c_filter.apply_small(frame)
    mask_flat = mask.flatten()
    reward = mask[2,9:12].sum() + mask[2,10:11].sum()

    # set twist
    rotate = c_filter.row_pos(mask)[3] * -0.45
    rotate = rl.decide(mask_flat, reward, rotate)
    twist.set_rotate(rotate)

    # reverse if no line
    print(rev.count)
    b = mask.sum() < min_mask_sum
    print(b)
    if rev.update(mask.sum() < min_mask_sum):
        twist.set(-0.55, 0.05)
        print('reversing!')

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






