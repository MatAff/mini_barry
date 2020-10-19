
import numpy as np

# conditional import to suppport development on laptop
try:
     from adafruit_motorkit import MotorKit
except ModuleNotFoundError:
    print("adafruit_motorkit module not found, no motors will move")
except NotImplementedError:
     print("Not running on correct board, no motors will move")

KEY_FORWARD = 82
KEY_BACKWARD = 84
KEY_LEFT = 81
KEY_RIGHT = 83


class AdaDrive(object):

    def __init__(self):
        try:
            self.kit = MotorKit()
        except NameError:
            self.kit = None
        self.forward = 0.0
        self.rotate = 0.0

    def set(self, act_dict):

        # check input
        keys = list(act_dict.keys())
        assert len(set(keys, ['forward', 'rotate'])) == len(keys), 'unknown keys present'
        
        # update
        self.forward = act_dict.get('forward', self.forward)
        self.rotate = act_dict.get('rotate', self.rotate)
        
        self.act()

    def manual(self, key):

        # update
        if key == KEY_FORWARD : self.forward += 0.05
        if key == KEY_BACKWARD : self.forward -= 0.05
        if key == KEY_LEFT : self.rotate += 0.05
        if key == KEY_RIGHT : self.rotate -= 0.05
        
        self.act()

    def act(self):
        
        # early return 
        if self.kit is None : return

        # calculate left - right        
        if self.rotate < 0:
            left = self.forward - self.rotate
            right = self.forward
        else:
            left = self.forward
            right = self.forward + self.rotate
        left = np.clip(left, -1.0, 1.0)
        right = np.clip(right, -1.0, 1.0)

        # apply threshold requirement
        thresh=0.0
        if abs(left) < thresh : left = 0.0
        if abs(right) < thresh : right = 0.0

        # set motors
        self.kit.motor1.throttle = left
        self.kit.motor2.throttle = left
        self.kit.motor3.throttle = right
        self.kit.motor4.throttle = right

    def stop(self):
        if self.kit is not None:
            self.kit.motor1.throttle = 0.0
            self.kit.motor2.throttle = 0.0
            self.kit.motor3.throttle = 0.0
            self.kit.motor4.throttle = 0.0
