#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

class FPS(object):

    def __init__(self, sparse=None):
        self.start = time.time()
        self.fps = -1
        self.sparse=sparse
        self.sparse_count = 0.0

    def update(self, verbose=False):
        lapse = time.time() - self.start
        if self.sparse is None:
            self.fps = 1.0 / lapse
            self.start = time.time()
            if verbose : print(self.to_string())
        else:
            self.sparse_count += 1
            if lapse > self.sparse:
                self.fps = self.sparse_count / lapse
                self.start = time.time()
                self.sparse_count = 0
                if verbose : print(self.to_string())

    def to_string(self):
        return 'fps: %.2f' % self.fps
