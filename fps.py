#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np

class FPS(object):

	def __init__(self):
		self.start = time.time()
		self.fps = -1

	def update(self):
		lapse = time.time() - self.start
		self.fps = 1.0 / lapse
		self.start = time.time()
		return self.to_string()

	def to_string(self):
		return 'fps: %.2f' % self.fps
