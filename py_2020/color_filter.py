#!/usr/bin/env python3

import cv2
import numpy as np
import unittest


class Filter(object):

    def __init__(self, ranges):
        self.bounds = np.array(ranges)

    def apply(self, bgr_frame):
        hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv_frame, self.bounds[0,:], self.bounds[1,:])

    def apply_mask(self, bgr_frame, mask):
        return cv2.bitwise_and(bgr_frame, bgr_frame, mask=mask)


def frame_to_line_pos(frame, filter):

    # create small mask
    frame_lower = frame[120:240, 0:320] # crop
    mask_lower = filter.apply(frame_lower)
    mask_lower_small = mask_lower.reshape(5, 24, 20, 16).mean(axis=(1,3)) # reduce size

    # return max positions
    cols = mask_lower_small.shape[1]
    mask_lower_small[:,int(cols/2)] += 0.0001 # ensure middle is selected if missing
    max_pos = np.argmax(mask_lower_small, 1)
    return max_pos / (cols - 1) * 2.0 - 1.0


class TestFrameToLinePos(unittest.TestCase):

    def test_frame_to_line_pos(self):

        # create filter

        # create sample frame

        # apply function

        # check result

        self.assertAlmostEqual(fps.fps, 20.0, delta=1.0)


if __name__ == '__main__':
    unittest.main()
