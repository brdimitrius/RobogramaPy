import sys
import subprocess as sp
import cv2
import numpy
import time

# Criando um objeto. 0 = Camera Externa
#video = cv2.VideoCapture(0)
capture = cv2.VideoCapture(0)
#capture.set(3, 320) #set width of frame
#capture.set(4, 200) #set hieght of frame
#capture.set(5, 20) #set FPS
#capture.set(cv2.CAP_PROP_FPS, 60)
#cv2.CAP_PROP_FRAME_COUNT

#capture.set(10, 20) #set brightness
# Create um frame
#check, frame = video.read()
successful, image = capture.read()

#print(check)
# print(frame)
a = "a"
for abc in image:
    roi = image[200:250, 0:639]
    linha_preta = cv2.inRange(roi, (0, 0, 0), (50, 50, 50))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    contours, hierarchy = cv2.findContours((linha_preta.copy()), (cv2.RETR_TREE), (cv2.CHAIN_APPROX_SIMPLE))
    time.sleep(0.1)
    print(len(contours))
    if len(contours) > 0:
        x, y, w, h = cv2.boundingRect(contours[0])
        #cv2.line(image, (x + (w / 2)), (200), (x + (w / 2)), (250), (255, 0, 0), (3))
        cv2.line(image, (x + (w // 2), 200), (x + (w // 2), 250), (255, 0, 0), 3)
    #rawCapture.truncate(0)
    cv2.imshow("preview", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
#cv2.imshow("Gravando", image)
# Pressionar qualquer tecla para saira
#key = cv2.waitKey(0)
#if key == ord("q"):
 #  sys.exit()
