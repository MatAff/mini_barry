#import time
from adafruit_motorkit import MotorKit

KEY_FORWARD = 0
KEY_BACKWARD = 0
KEY_LEFT = 0
KEY_RIGHT = 0

class Twist(object):
	
	def __init__(self, forward=0.0, rotate=0.0):
		self.foward = forward
		self.rotate = rotate

	def set(self, forward=0.0, rotate=0.0):
		self.foward = forward
		self.rotate = rotate
		
	def man(self, key):
		if key == KEY_FORWARD : self.foward += 0.2
		if key == KEY_BACKWARD : self.foward -= 0.2
		if key == KEY_LEFT : self.rotate += 0.2
		if key == KEY_RIGHT : self.rotate -= 0.2

class AdaDrive(object):
	
	def __init__(self): #, swap=False, m1=1.0, m2=1.0):
		self.kit = kit = MotorKit()
		#self.swap = swap
		#self.m1=m1
		#self.m2=m2
  
    def set_throttle(self, left, right):
		self.kit.motor1.throttle = left
		self.kit.motor1.throttle = right
		
	def drive(self, twist):
		left = self.driveSpeed - self.rotateSpeed
        right = self.driveSpeed + self.rotateSpeed
		self.set_throttle(left, right)
    
	def stop(self)
		self.kit.motor1.throttle = 0.0
		self.kit.motor1.throttle = 0.0


