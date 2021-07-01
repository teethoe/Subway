import cv2
import numpy as np
import matplotlib.pyplot as plt
from functions import stitch
from process import Process
from identify import Identify


fixed = [0 for i in range(5)]
colour_pos = [0 for i in range(5)]
ordered = [0 for i in range(5)]

for i in range(5):
    img = cv2.imread('./img/samples/official/sample 2/{}.png'.format(i+1))
    img = Process(img).fix()
    fixed[i] = img

    x = Identify(img)

    cv2.imshow('img', img)
    x.pie()
    cv2.waitKey(0)
    colour_pos[i] = x.get_position()
    print(colour_pos[i])

found = False
i = 0
while not found and i < 5:
    n = sum(x != 0 for x in colour_pos[i])[0]
    print(n)
    if n == 4:
        side = i
        ordered[0] = fixed[i]
        found = True
    i += 1

for i in range(1, 5):
    val = colour_pos[side][4-i][0]
    print(val)
    for j in range(5):
        if j != side:
            if val-5 <= colour_pos[j][0][0] <= val+5:
                ordered[i] = fixed[j]

mosaic = stitch(ordered)
mosaic = cv2.cvtColor(mosaic, cv2.COLOR_BGR2RGB)

#cv2.imshow('stitch', mosaic)

plt.imshow(mosaic)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
