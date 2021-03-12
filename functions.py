import cv2
import numpy as np


def get_trap(img, z, ratios):
    height, width = img.shape[:2]
    b = int(height * z * ratios[0])
    t = int(b * ratios[1])
    xb = int((width - b) // 2)
    xt = int((width - t) // 2)
    h = int(b * ratios[2])
    y = ratios[3]
    tl = (xt, y)
    tr = (xt + t, y)
    bl = (xb, y + h)
    br = (xb + b, y + h)
    points = [tl, tr, bl, br]
    return points


def get_cnt(img, side, z, rxy):
    height, width = img.shape[:2]
    h = int(height * z)
    if side % 2 == 0:
        w = h
    else:
        w = int(h * rxy)
    x = int((width - w) // 2)
    y = int((height - h) // 2)
    return x, y, w, h


def get_rect(cnt):
    x, y, w, h = cnt
    tl = (x, y)
    tr = (x+w, y)
    bl = (x, y+h)
    br = (x+w, y+h)
    return tl, tr, bl, br


def draw_cnt(img, side, z, ratios):
    colour = (0, 255, 0)
    if side > 0:
        if side > 1:
            x, y, w, h = get_cnt(img, side, z, ratios[0])
            img = cv2.rectangle(img, (x, y), (x + w, y + h), colour, 2)
        else:
            points = get_trap(img, z, ratios)
            for i in range(4):
                img = cv2.line(img, points[i], points[(i + 2) % 4], colour, 2)
                if i % 2 == 0:
                    img = cv2.line(img, points[i], points[(i+1) % 4], colour, 2)
    return img


def transform(img, z, ratios):
    pts = np.float32(get_trap(img, z, ratios))
    w, h = get_cnt(img, 1, z, ratios[0])[2:]
    dst = np.float32(get_rect([0, 0, w, h]))
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped


def stitch(images):
    bottom = cv2.hconcat(images[1:])
    top = np.zeros(bottom.shape, np.uint8)
    top[0:top.shape[0], images[1].shape[1]:(images[1].shape[1]+images[2].shape[1])] = images[0]
    mosaic = cv2.vconcat([top, bottom])
    return mosaic
