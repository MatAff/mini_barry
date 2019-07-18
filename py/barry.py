#/usr/bin/env python3

from visual import Camera, Display, Recorder, Annotate
from color_filter import Filter
from drive import Twist, AdaDrive
from fps import FPS

# settings
show_frame = True # toggle to switch off/on display
filename = "../media/first_circle.avi"
display_delay = 50

# keys
KEY_ESC = 27
KEY_FORWARD = 82
KEY_BACKWARD = 84
KEY_LEFT = 81
KEY_RIGHT = 83
KEY_P = 112

# set constants
SENSE_HEIGHT_LIST = [400]
SENSE_WIDTH = 10

# initialize objects
cam = Camera(filename)
disp = Display('Barry', show_frame)
rec = Recorder('./barry.avi', 20, (640, 480), sparse=5)
twist = Twist(forward=0.5)
ada_drive = AdaDrive()
fpss = FPS()

#c_filter = Filter([20,0,20], [70,255,255])
#c_filter = Filter([25, 30, 50], [55, 255, 255]) # Daytime
#c_filter = Filter([30, 50, 100], [65, 200, 160]) # Daytime (improved)
#c_filter = Filter([35, 50, 30], [85, 200, 160]) # Dim
c_filter = Filter([15, 15, 53], [80, 137, 137]) # later afternoon

# initialize variables
running = True
key = -1

while running:

    # SENSE - get frame
    frame = cam.get()
    print(fpss.update())

    # DECIDE - apply filter and get position
    mask_frame, mask = c_filter.apply(frame, True, False)
    pos_list = c_filter.get_block_pos(mask, SENSE_HEIGHT_LIST, SENSE_WIDTH)
    block_line_list = c_filter.get_lines()

    # DECIDE - set drive
    rotate = pos_list[0] * -0.15
    twist.set_rotate(rotate)
    l = twist.as_line()

    # ACT - drive
    ada_drive.drive(twist) # Not available on laptop
    twist.set_forward(0.25)

    # SHARE - display
    print(fpss.to_string())
    show_frame = frame
    #show_frame = mask_frame
    show_frame = Annotate.add_text(show_frame, fpss.to_string(), (0, 255, 0), 1)
    show_frame = Annotate.add_line(show_frame, l, (0, 255, 0))
    show_frame = Annotate.add_lines_list(show_frame, block_line_list, (0, 0, 255))
    show_frame = Annotate.add_text(show_frame, 'position %.3f' % pos_list[0], (0, 255, 0), 2)
    show_frame = Annotate.add_text(show_frame, 'rotate: %.3f' % rotate, (0, 255, 0), 3)
    show_frame = Annotate.add_text(show_frame, twist.to_string(), (0, 255, 0), 4)
    key = disp.show(show_frame, delay=display_delay)

	# SENSE - handle keys
    if key != -1:
        print(key)
        if key == KEY_P : rec.save_img(frame)
        c_filter.key_handler(key)

    # DECIDE - manual drive
    if key in [KEY_FORWARD, KEY_BACKWARD, KEY_LEFT, KEY_RIGHT] :
        twist.man(key)

    # SHARE - record
    rec.write(show_frame)

    # check status
    if key == KEY_ESC:
        running = False

ada_drive.stop()
cam.release()
rec.release()
disp.close()

