import cv2
import numpy as np

RATIO = 0.5


def get_trap(img, r):
    height, width = img.shape[:2]
    b = int(height * r * 2)
    t = int(b * (3.5 / 5))
    xb = int((width - b) // 2)
    xt = int((width - t) // 2)
    h = int((b * 7 ** 0.5) // 20)
    y = int((height - h) // 2)
    tl = (xt, y)
    tr = (xt + t, y)
    bl = (xb, y + h)
    br = (xb + b, y + h)
    points = [tl, tr, bl, br]
    return points


def get_cnt(img, side, r):
    height, width = img.shape[:2]
    h = int(height * r)
    if side % 2 == 0:
        w = h
    else:
        w = h * 2
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


def draw_cnt(img, side, r):
    colour = (0, 255, 0)
    if side > 0:
        if side > 1:
            x, y, w, h = get_cnt(img, side, r)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), colour, 2)
        else:
            points = get_trap(img, r)
            for i in range(4):
                img = cv2.line(img, points[i], points[(i + 2) % 4], colour, 2)
                if i % 2 == 0:
                    img = cv2.line(img, points[i], points[(i+1)%4], colour, 2)
    return img


def transform(img, r):
    pts = np.float32(get_trap(img, r))
    w, h = get_cnt(img, 1, r)[2:]
    dst = np.float32(get_rect([0, 0, w, h]))
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped


def stitch(images):
    bottom = cv2.hconcat(images[1:])
    top = np.zeros(bottom.shape, np.uint8)
    top[0:top.shape[0], int(top.shape[1]/6):int(top.shape[1]/2)] = images[0]
    mosaic = cv2.vconcat([top, bottom])
    return mosaic


images = ['' for i in range(5)]
side = -1
#url = 'http://192.168.0.199:8080'
#cap = cv2.VideoCapture(url+'/video')
#cap = cv2.VideoCapture('./vid/test vid.mp4')
cv2.VideoCapture(0)

while True:
    ret, frame = cap.read(1)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    x, y, w, h = get_cnt(frame, side, RATIO)
    draw_cnt(frame, side, RATIO)
    cv2.imshow('cam', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('c'):
        if side >= 2:
            images[side - 1] = frame[y:y+h, x:x+w]
        elif side == 1:
            images[0] = frame
    else:
        for i in range(5):
            if k == (49 + i):
                side = i + 1

cap.release()
cv2.destroyAllWindows()

images[0] = transform(images[0], RATIO)
mosaic = stitch(images)
cv2.imshow('mosaic', mosaic)

for i in range(5):
    cv2.imshow(str(i), images[i])

cv2.waitKey(0)
cv2.destroyAllWindows()
