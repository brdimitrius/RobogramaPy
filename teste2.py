import sys
import subprocess as sp
import cv2
import numpy
import time
#capture.set(3, 320) #set width of frame
#capture.set(4, 200) #set hieght of frame
#capture.set(5, 20) #set FPS
#capture.set(cv2.CAP_PROP_FPS, 60)
#cv2.CAP_PROP_FRAME_COUNT
#successful, image = capture.read()
#capture.set(10, 20) #set brightness
# Create um frame
# Criando um objeto. 0 = Camera Externa
#video = cv2.VideoCapture(0)
a = 0
capture = cv2.VideoCapture(0)
while True:
    a = a + 1
    check, frame = capture.read()
    cv2.imshow("Oi", frame)
    key = cv2.waitKey(0)
    if key == ord("q"):
        break
    capture.release()