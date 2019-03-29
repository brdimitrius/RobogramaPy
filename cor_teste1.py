import cv2
import numpy as np

## Read
img = cv2.VideoCapture(0)
while True:
    successful, image = img.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
## mask of green (36,25,25) ~ (86, 255,255)
# mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))

## slice the green
    imask = mask>0
    green = np.zeros_like(image, np.uint8)
    cv2.imwrite("green.png", green)
    #print("A")
    cv2.imshow('frame', hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break