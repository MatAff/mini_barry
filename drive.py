#import time
from adafruit_motorkit import MotorKit

KEY_FORWARD = 82
KEY_BACKWARD = 84
KEY_LEFT = 81
KEY_RIGHT = 83

class Twist(object):
    
    def __init__(self, forward=0.0, rotate=0.0):
        self.forward = forward
        self.rotate = rotate

    def print(self):
        #print('Twist: ' + self.forward + ' ' + self.rotate)
        print(self.forward)
        print(self.rotate)

    def set(self, forward=0.0, rotate=0.0):
        self.forward = forward
        self.rotate = rotate

    def set_rotate(self, rotate):
        self.rotate = rotate
        
    def man(self, key):
        if key == KEY_FORWARD : self.forward += 0.05
        if key == KEY_BACKWARD : self.forward -= 0.05
        if key == KEY_LEFT : self.rotate += 0.05
        if key == KEY_RIGHT : self.rotate -= 0.05

class AdaDrive(object):

    def __init__(self): #, swap=False, m1=1.0, m2=1.0):
        self.kit = kit = MotorKit()
        #self.swap = swap
        #self.m1=m1
        #self.m2=m2
  
    def set_throttle(self, left, right):
        thresh = 0.00
        if abs(left)  > thresh : 
            self.kit.motor1.throttle = left
        else: 
            self.kit.motor1.throttle = 0.0
        if abs(right) > thresh : 
            self.kit.motor2.throttle = right
        else:
            self.kit.motor2.throttle = 0.0
        
    def drive(self, twist):
        left = twist.forward - twist.rotate
        right = twist.forward + twist.rotate
        self.set_throttle(left, right)
    
    def stop(self):
        self.kit.motor1.throttle = 0.0
        self.kit.motor2.throttle = 0.0


