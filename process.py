import cv2
from functions import *
from itertools import groupby, product, combinations
import matplotlib.pyplot as plt


'''
https://www.pyimagesearch.com/2016/03/21/ordering-coordinates-clockwise-with-python-and-opencv/
https://www.mathopenref.com/coordpolygonareacalc.html
'''


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def centroid(arr):
    l = len(arr)
    sum_x = np.sum([pt[0] for pt in arr])
    sum_y = np.sum([pt[1] for pt in arr])
    return int(sum_x/l), int(sum_y/l)


def area(x, y):
    area = 0
    j = len(x) - 1
    for i in range(len(x)):
        area += (x[j] + x[i]) * (y[i] - y[j])
        j = i
    return int(abs(area/2))


def order_pts(points):
    pts = list(points)
    pts.sort(key=lambda x: x[0])
    tl, tr = sorted(pts[:2], key=sum)
    bl, br = sorted(pts[2:], key=sum)
    return tl, tr, br, bl


def get_ratio(points):
    dx = points[1][0] - points[0][0]
    dy = points[0][1] - points[3][1]
    if abs(dy/dx) < 0.7:
        return 2
    else:
        return 1


class Process:
    def __init__(self, img):
        self.img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    def fix(self):
        kernel = np.ones((7, 7), np.uint8)
        kernel2 = np.ones((2, 2), np.uint8)

        grey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        ret, th = cv2.threshold(grey, 120, 255, cv2.THRESH_BINARY)
        # th2 = cv2.adaptiveThreshold(grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 2)
        # th2 = cv2.morphologyEx(th2, cv2.MORPH_OPEN, kernel2)
        th = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel2)

        h, w = th.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        flood = th.copy()
        cv2.floodFill(flood, mask, (0, 0), 255)
        filled = cv2.bitwise_xor(th, flood)
        filled = cv2.bitwise_not(filled)
        filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, kernel)

        dst = cv2.cornerHarris(filled, 5, 15, 0.04)
        # dst = cv2.dilate(dst, None)
        # img[dst > 0.01*dst.max()] = (0, 0, 255)
        dst_norm = np.empty(dst.shape, dtype=np.float32)
        cv2.normalize(dst, dst_norm, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        dst_norm_scaled = cv2.convertScaleAbs(dst_norm)
        # print(dst.max())
        # self.img[dst_norm_scaled > 100] = (0, 0, 255)
        points = []
        for i in range(dst_norm.shape[0]):
            for j in range(dst_norm.shape[1]):
                if dst_norm_scaled[i][j] > 120:
                    points.append((i, j))

        adj = [sorted(sub) for sub in product(points, repeat=2) if dist(*sub) <= 2]
        grp_dict = {ele: {ele} for ele in points}
        for a, b in adj:
            grp_dict[a] |= grp_dict[b]
            grp_dict[b] = grp_dict[a]
        grp = [[*next(val)] for key, val in groupby(sorted(grp_dict.values(), key=id), id)]

        corners = []
        for corner in grp:
            corners.append(centroid(corner))

        cnrComb = list(combinations(corners, 4))
        maxArea = 0
        maxComb = []
        for cnr in cnrComb:
            c = order_pts(cnr)
            x = [pt[1] for pt in c]
            y = [pt[0] for pt in c]
            a = area(x, y)
            if a > maxArea:
                maxArea = a
                maxComb = c

        maxComb = list(maxComb)

        for i in range(4):
            y = maxComb[i][0]
            x = maxComb[i][1]
            maxComb[i] = (x, y)

        temp = maxComb[2]
        maxComb[2] = maxComb[3]
        maxComb[3] = temp

        ratio = get_ratio(maxComb)

        trans = transform(self.img, maxComb, ratio)
        return trans
