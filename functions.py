import cv2
import numpy as np


def get_rect(cnt):
    x, y, w, h = cnt
    tl = (x, y)
    tr = (x+w, y)
    bl = (x, y+h)
    br = (x+w, y+h)
    return tl, tr, bl, br


def transform(img, pts, ratio):
    pts = np.float32(pts)
    h = 200
    if ratio == 1:
        w = 200
    else:
        w = 400
    dst = np.float32(get_rect([0, 0, w, h]))
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped


def stitch(images):
    bottom = cv2.hconcat(images[1:])
    top = np.zeros(bottom.shape, np.uint8)
    top[0:top.shape[0], images[1].shape[1]:(images[1].shape[1]+images[0].shape[1])] = images[0]
    mosaic = cv2.vconcat([top, bottom])
    return mosaic
