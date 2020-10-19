
#!/usr/bin/env python3

from color_filter import Filter, frame_to_line_pos
from control import EngineeredControl
from drive import AdaDrive
from fps import FPS
from visual import Camera, Display, Recorder

KEY_ESC = 27

fps = FPS(20.0)

camera = Camera()
display = Display('robot', True)
recorder = Recorder('./robot.avi', 20, (320, 240), sparse=1)

filter_dict = { 'blue': [[100,182,83],[107,255,241]] }
filter = Filter(filter_dict['blue'])

controller = EngineeredControl()

drive = AdaDrive()

running = True
while running:
    
    # input
    frame = camera.get()
    line_pos = frame_to_line_pos(frame, filter)
    
    # control
    act_dict = controller.decide(line_pos)

    # act
    drive.set(act_dict)

    # feedback
    key = display.show(frame)
    running = (key != KEY_ESC)
    recorder.write(frame)
    fps.get_fps()

camera.release()
recorder.release()
display.close()
drive.stop()




