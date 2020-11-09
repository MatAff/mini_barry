
#!/usr/bin/env python3

from color_filter import Filter, frame_to_line_pos
from control import EngineeredControl, TestDrive
from drive import AdaDrive
from fps import FPS
from visual import Camera, Display, Recorder

KEY_ESC = 27
KEY_SPACE = 32 

fps = FPS(1.0)

# camera = Camera(filename='robot.avi')
camera = Camera()
display = Display('robot', True)
recorder = Recorder('./robot.avi', 20, (320, 240), sparse=1)

filter_dict = { 
    'blue': [[100,182,83],[107,255,241]], 
    'night_blue': [[89,163,118],[106,247,247]] 
}
filter = Filter(filter_dict['night_blue'])

# controller = EngineeredControl()
controller = TestDrive()

drive = AdaDrive()

# frame = camera.get()
# key = 0 

running = True
while running:
    
    # input
    frame = camera.get()
    line_pos, masked_frame = frame_to_line_pos(frame, filter)
    print(line_pos)
    
    # control
    act_dict = controller.decide(line_pos)

    # act
    drive.set(act_dict)
    print(act_dict)

    # feedback
    # key = display.show(frame)
    key = display.show(masked_frame)
    running = (key != KEY_ESC)
    recorder.write(frame)
    fps.get_fps(verbose=False)

    # # step through frames
    # if key == KEY_SPACE:
    #     frame = camera.get()

camera.release()
recorder.release()
display.close()
drive.stop()





