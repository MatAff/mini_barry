#/usr/bin/env python3

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS
from reinforcement_learning import rl_manager

# keys
KEY_ESC = 27
KEY_P = 112

# set constants
#SENSE_HEIGHT = 400
SENSE_HEIGHT_LIST = [470, 450, 430, 410, 390, 370, 350, 330, 310]
SENSE_HEIGHT = 400
SENSE_WIDTH = 10
BATCH_SIZE = 50.0

filename = "../media/first_circle.avi"

# initialize objects
cam = Camera(filename)
disp = Display('Barry')
rec = Recorder('./barry.avi', 20, (640, 480))
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()
rl = rl_manager(len(SENSE_HEIGHT_LIST))

#green_filter = Filter([20,0,20], [70,255,255])
#green_filter = Filter([25, 30, 50], [55, 255, 255]) # Daytime
#green_filter = Filter([30, 50, 100], [65, 200, 160]) # Daytime (improved)
#green_filter = Filter([35, 50, 30], [85, 200, 160]) # Dim
green_filter = Filter([15, 15, 53], [80, 137, 137]) # later afternoon

# initialize variables
running = True
key = -1
frame_count = 0

while running:

    # SENSE - get frame
    frame = cam.get()
    print(fpss.update())

    # DECIDE - apply filter and get position
    mask_frame, mask = green_filter.apply(frame, True, False)
    pos_list = green_filter.get_block_pos(mask, SENSE_HEIGHT_LIST, SENSE_WIDTH)
    block_line_list = green_filter.get_lines()

    # DECIDE - set drive
    rotate = pos_list[3] * -0.15

    # reinforcement learning
    rl.decide(pos_list, rotate)
    twist.set_rotate(rotate)
    l = twist.as_line()

    # ACT - drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.25)

    # SHOW
    show_frame = frame
    #show_frame = mask_frame
    show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
    show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
    show_frame = Annotate.add_lines_list(show_frame, block_line_list, (0, 0, 255))
    show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 2)
    show_frame = Annotate.add_text(show_frame, twist.to_string(), (0, 255, 0), 3)
    #key = disp.show(show_frame, 5) # debug 50 for extra wait

	# SENSE - handle keys
    if key != -1:
        print(key)
        if key == KEY_P : rec.save_img(frame)
        green_filter.key_handler(key)

    # SHARE - record
    if frame_count % 5 == 0:
        rec.write(show_frame)

    # batch update
    if frame_count % BATCH_SIZE == 0:
        print('new batch')
        ada_drive.stop() # pause driving
        rl.switch_batch(int(frame_count / BATCH_SIZE))

    # check status
    if key == KEY_ESC:
        running = False

    # update frame count
    frame_count += 1
    print(frame_count)

ada_drive.stop()
cam.release()
rec.release()
disp.close()

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




