#!/usr/bin/env python3

import cv2
import numpy as np
import unittest

# from visual import Display

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
    mask = filter.apply(frame)
    mask_lower = mask[120:240, 0:320] # crop
    mask_lower_small = mask_lower.reshape(5, 24, 320, 1).mean(axis=(1,3)) # reduce size
    print(mask_lower_small.shape)

    # apply maxk
    masked_frame = filter.apply_mask(frame, mask)

    # return max positions
    cols = mask_lower_small.shape[1]
    mask_lower_small[:,int(cols/2)] += 0.0001 # ensure middle is selected if missing
    max_pos = np.argmax(mask_lower_small, 1)
    return max_pos / (cols - 1) * 2.0 - 1.0, masked_frame


def create_sample_frame(width, height, line_start, line_end, line_color):
    frame = np.zeros((height, width,3), np.uint8)	
    frame = cv2.line(frame, line_start, line_end, line_color, 5)
    return frame


class TestFrameToLinePos(unittest.TestCase):


    def test_frame_to_line_pos(self):

        # create filter
        filter_dict = { 'blue': [[100,182,83],[107,255,241]] }
        filter = Filter(filter_dict['blue'])

        for x, y in zip([0, 160, 320], [-1, 0, 1]):

            # create sample frame
            bgr_frame = create_sample_frame(320, 240, (x,0), (x, 240), (237, 142, 17))

            # apply filter
            line_pos, masked_frame = frame_to_line_pos(bgr_frame, filter)

            # check result
            print(line_pos)

            # display.show(masked_frame)
            # display = Display('robot', True)

            self.assertListEqual(line_pos.round(1).tolist(), [y, y, y, y, y])


if __name__ == '__main__':
    unittest.main()


# filter_dict = { 'blue': [[100,182,83],[107,255,241]] }
# filter = Filter(filter_dict['blue'])

# bgr_frame = create_sample_frame(320, 240, (160,0), (160, 240), (237, 142, 17))
# bgr_frame.shape

# mask = filter.apply(bgr_frame)
# mask.shape
# mask.reshape(10, 24, 21, 16).mean(axis=(1, 3)).shape

