import cv2
from functions import *

RATIO = 0.5

images = ['' for i in range(5)]
side = -1
#url = ''
#cap = cv2.VideoCapture(url+'/video')
cap = cv2.VideoCapture(0)

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

cv2.waitKey(0)
cv2.destroyAllWindows()
