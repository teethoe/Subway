from functionsOdered import *

ZOOM = 0.5
rhw = 1.00
y24 = 100
rtb = 1.00
rhb = 0.50
y1 = 100
ratios = [rhw, y24, rtb, rhb, y1]
images = ['' for i in range(5)]
side = -1
shape = -1


def nothing():
    pass


url = 'https://192.168.0.106:8080'
cap = cv2.VideoCapture(url+'/video')
#cap = cv2.VideoCapture('./vid/test vid.mp4')
#cap = cv2.VideoCapture(4)

cv2.namedWindow('ratios')
cv2.createTrackbar('h:w', 'ratios', 0, 200, nothing)
cv2.createTrackbar('y2:4', 'ratios', 0, 500, nothing)
cv2.createTrackbar('t:b', 'ratios', 0, 50, nothing)
cv2.createTrackbar('h:b', 'ratios', 0, 40, nothing)
cv2.createTrackbar('y1', 'ratios', 0, 400, nothing)

while True:
    ret, frame = cap.read(1)
    frame = cv2.resize(frame, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_CUBIC)
    ratios[0] = (cv2.getTrackbarPos('h:w', 'ratios') + 100) / 100
    ratios[1] = cv2.getTrackbarPos('y2:4', 'ratios')
    ratios[2] = (cv2.getTrackbarPos('t:b', 'ratios') + 50) / 100
    ratios[3] = (cv2.getTrackbarPos('h:b', 'ratios') + 5) / 100
    ratios[4] = cv2.getTrackbarPos('y1', 'ratios') + 100
    if side > 0:
        if side == 1:
            shape = 2
        else:
            shape = side % 2
    x, y, w, h = get_cnt(frame, shape, ZOOM, ratios)
    draw_cnt(frame, shape, ZOOM, ratios)
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

images[0] = transform(images[0], ZOOM, ratios)
mosaic = stitch(images)
cv2.imshow('mosaic', mosaic)

cv2.waitKey(0)
cv2.destroyAllWindows()
