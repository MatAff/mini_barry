
# conditional import to suppport development on laptop

import numpy as np

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

class Twist(object):

    def __init__(self, forward=0.0, rotate=0.0):
        self.forward = forward
        self.rotate = rotate

    def to_string(self):
        return 'Twist: %.2f %.2f' % (self.forward, self.rotate)

    def set(self, forward=0.0, rotate=0.0):
        self.forward = forward
        self.rotate = rotate

    def set_forward(self, forward):
        self.forward = forward

    def set_rotate(self, rotate):
        self.rotate = rotate

    def man(self, key):
        if key == KEY_FORWARD : self.forward += 0.05
        if key == KEY_BACKWARD : self.forward -= 0.05
        if key == KEY_LEFT : self.rotate += 0.05
        if key == KEY_RIGHT : self.rotate -= 0.05

    def as_line(self):
        S = (320, 340)
        E = (int(320 - self.rotate * 100), 240)
        return S, E

class AdaDrive(object):

    def __init__(self):
        try:
            self.kit = MotorKit()
        except NameError:
            self.kit = None

    def set_throttle(self, left, right):
        if self.kit is None:
            return
        else:
	        thresh = 0.0
			# TODO: move duplicate code to separate function
	        if abs(left)  > thresh :
	            if self.kit.motor1.throttle != 0.0:
	                self.kit.motor1.throttle = left
	            else:
	                self.kit.motor1.throttle = left/abs(left)
	        else:
	            self.kit.motor1.throttle = 0.0
	        if abs(right) > thresh :
	            if self.kit.motor2.throttle != 0.0:
	                self.kit.motor2.throttle = right
	            else:
	                self.kit.motor2.throttle = right/abs(right)
	        else:
	            self.kit.motor2.throttle = 0.0

    def drive(self, twist):
        if twist.rotate < 0:
            left = twist.forward - twist.rotate
            right = twist.forward
        else:
            left = twist.forward
            right = twist.forward + twist.rotate
        self.set_throttle(left, right)

    def stop(self):
        if self.kit is not None:
            self.kit.motor1.throttle = 0.0
            self.kit.motor2.throttle = 0.0
