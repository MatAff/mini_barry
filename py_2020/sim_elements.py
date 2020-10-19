
import math 
import numpy as np

import cv2

scale = 30

def to_pixel(cart):
    # convert cartesian coordinate into pixel coordinates
    S = np.array([scale, -scale])
    T = np.array([320, 480 - 80])
    return(tuple((cart * S + T).astype(int)))

def draw_line(frame, points, color):
    for i in range(points.shape[0] - 1):
        s_pix = to_pixel(points[i+0,:])
        e_pix = to_pixel(points[i+1,:])
        try:
            cv2.line(frame, s_pix, e_pix,color,2)
        except Exception as e:
            print(points)
            print(s_pix, e_pix)
            raise e

def rotation(rad):
    return(np.matrix([[math.cos(rad), -math.sin(rad)],
                      [math.sin(rad),  math.cos(rad)]]))


class Line(object):

    def __init__(self, p1, p2):
        self.points = np.array([p1, p2])

    def get_point(self, pos):
        return(self.points[pos,:])

    # Intersect last line segment with first line segment
    def intersect(self, other):
        CA = self.points[-2,:] - other.points[0,:]
        AB = self.points[-1,:] - self.points[-2,:]
        CD = other.points[1,:] - other.points[0,:]
        denom = np.cross(CD, AB)
        if denom != 0:
            s = np.cross(CA,AB) / denom
            i  = other.points[0,:] + s * CD
            overlap = self.in_range(i) and other.in_range(i)
            return(i, True, overlap)
        else:
            return None, False, False

    def in_range(self, p):
        return(((self.points[0,:] <= p)==(p <= self.points[1,:])).all())


class Spline(object):

    def __init__(self, l1, l2, n):
        self.points = np.zeros((n,2))
        B = l1.get_point(-1)
        C = l2.get_point(0)
        I, _, _ = l1.intersect(l2)
        for i in range(n):
            ratio = i / (n-1)
            S = self.rel_line(B, I, ratio)
            E = self.rel_line(I, C, ratio)
            P = self.rel_line(S, E, ratio)
            self.points[i,:] = P

    def rel_line(self, S, E, ratio):
        return(S + (E - S) * ratio)


class Course(object):

    def __init__(self):
        line_list = []
        sections = [Line(np.array([0,0]), np.array([1,0])),
                    Line(np.array([5,5]), np.array([4,6.5])),
                    Line(np.array([-4,6]), np.array([-5,5]))]

        for i, sect in enumerate(sections):
            spline = Spline(sections[i-1], sect, 25)
            line_list.append(spline.points)
            line_list.append(sect.points)

        self.points = np.concatenate(line_list)

    def draw(self, frame):
        draw_line(frame, self.points, (255,0,0))


class Car(object):

    def __init__(self, dist_list):
        self.dist_list = dist_list
        self.pos = np.array([[0],[0]])
        self.dir = np.array([[1],[0]])

    def move(self, act_dict):
        x = act_dict['forward']
        rad = act_dict['rotate']
        self.pos = self.pos + x * self.dir * 0.5
        self.dir = np.matmul(rotation(rad), self.dir)
        self.pos = self.pos + x * self.dir * 0.5

    def draw(self, frame):
        tl = self.pos + np.matmul(rotation(math.pi *  0.5), self.dir * 0.3)
        tr = self.pos + np.matmul(rotation(math.pi * -0.5), self.dir * 0.3)
        bl = self.pos - self.dir + np.matmul(rotation(math.pi *  0.5), self.dir * 0.3)
        br = self.pos - self.dir + np.matmul(rotation(math.pi * -0.5), self.dir * 0.3)
        points = np.array(np.concatenate([tl, tr, br, bl, tl, br, bl, tr], axis=1).transpose())
        draw_line(frame, points, (0,0,255))

    def detect(self, points, frame, dist):

        # Create detection line
        sp = self.pos + np.matmul(rotation(math.pi * -0.25), self.dir * dist)
        ep = self.pos + np.matmul(rotation(math.pi *  0.25), self.dir * dist)
        sp = np.squeeze(np.array(sp))
        ep = np.squeeze(np.array(ep))
        detect_line = Line(sp, ep)

        # Draw detection line
        draw_line(frame, detect_line.points, (0,200,0))

        # Loop through course
        for i in range(points.shape[0] - 1):
            sub_line = Line(points[i,:], points[i+1,:])
            inters, has_intersect, overlap = detect_line.intersect(sub_line)
            if overlap == True:
                pos = np.linalg.norm(inters - sp) / np.linalg.norm(ep - sp)
                return((pos - 0.5) * 2.0)

    def detect_list(self, points, frame):
        return([self.detect(points, frame, dist) for dist in self.dist_list])
