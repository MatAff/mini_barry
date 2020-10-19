#!/usr/bin/env python3

import time
import unittest


class FPS(object):

    def __init__(self, sparse=1.0):
        self.fps = 0.0
        self.sparse = sparse
        self.count = 0.0
        self.last_time = time.time()

    def get_fps(self, verbose=False):

        lapse_time = time.time() - self.last_time

        self.count += 1.0
        if self.count >= self.sparse:
            self.fps = self.count / lapse_time
            self.last_time = time.time()
            self.count = 0
        
        if verbose:
            print(self)
        
        return self.fps

    def __str__(self):
        return 'fps: %.2f' % self.fps


class TestFPS(unittest.TestCase):

    def test_get_fps(self):

        fps = FPS()

        for i in range(10):
            time.sleep(1.0 / 20.0)
            fps.get_fps()

        print(fps)

        self.assertAlmostEqual(fps.fps, 20.0, delta=1.0)

    def test_get_fps_sparse(self):
        
        fps = FPS(10)

        for i in range(20):
            time.sleep(1.0 / 20.0)
            fps.get_fps()

        print(fps)

        self.assertAlmostEqual(fps.fps, 20.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
