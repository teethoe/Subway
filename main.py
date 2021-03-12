from functions import *

ZOOM = 0.5
rxy = 1.00
rtb = 1.00
rhb = 0.50
y1 = 100
ratios = [rxy, rtb, rhb, y1]
images = ['' for i in range(5)]
side = -1


def nothing(x):
    pass


#url = 'https://192.168.0.199:8080'
#cap = cv2.VideoCapture(url+'/video')
cap = cv2.VideoCapture(4)

cv2.namedWindow('ratios')
cv2.createTrackbar('y:x', 'ratios', 0, 200, nothing)
cv2.createTrackbar('t:b', 'ratios', 0, 50, nothing)
cv2.createTrackbar('h:b', 'ratios', 0, 40, nothing)
cv2.createTrackbar('y1', 'ratios', 0, 400, nothing)

while True:
    ret, frame = cap.read(1)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    ratios[0] = (cv2.getTrackbarPos('y:x', 'ratios') + 100) / 100
    ratios[1] = (cv2.getTrackbarPos('t:b', 'ratios') + 50) / 100
    ratios[2] = (cv2.getTrackbarPos('h:b', 'ratios') + 5) / 100
    ratios[3] = cv2.getTrackbarPos('y1', 'ratios') + 100
    x, y, w, h = get_cnt(frame, side, ZOOM, ratios[0])
    draw_cnt(frame, side, ZOOM, ratios)
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
