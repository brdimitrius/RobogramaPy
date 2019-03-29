import sys
import subprocess as sp
import cv2
import numpy
import time

# Criando um objeto. 0 = Camera Externa
#video = cv2.VideoCapture(0)
video = cv2.VideoCapture(-1)
video.set(3, 251)
video.set(4, 251)
#capture.set(5, 20) #set FPS
#capture.set(cv2.CAP_PROP_FPS, 60)
#cv2.CAP_PROP_FRAME_COUNT

#capture.set(10, 20) #set brightness
# Create um frame
#check, frame = video.read()
#print(check)
# print(frame)
a = "a"
while True:
    successful, image = video.read()
    #roi = image[200:250, 0:639]
    linha_preta = cv2.inRange(image, (0, 0, 0), (50, 50, 50))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    contours, hierarchy = cv2.findContours((linha_preta.copy()), (cv2.RETR_TREE), (cv2.CHAIN_APPROX_SIMPLE))
    #print(len(contours))
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea) ## CODIGO DE DESENHO 1
        M = cv2.moments(c) ## CODIGO DE DESENHO 1

        cx = int(M['m10']/M['m00']) ## CODIGO DE DESENHO 1
        cy = int(M['m01']/M['m00']) ## CODIGO DE DESENHO 1
        cv2.line(image,(cx,0),(cx,720),(255,0,0),1) #Linha Vertical
        cv2.line(image,(0,cy),(1280,cy),(255,0,0),1) #Linha horizontal   ## CODIGO DE DESENHO 1
        cv2.drawContours(image, contours, -1, (0,255,0), 1) # Desenhar a area detectada


        #x, y, w, h = cv2.boundingRect(contours[0])
        #cv2.line(image, (x + (w / 2)), (200), (x + (w / 2)), (250), (255, 0, 0), (3))
        ##cv2.line(image, (x + (w // 2),  200), (x + (w // 2), 250), (255, 0, 0), 3)
    #rawCapture.truncate(0)
    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#cv2.imshow("Gravando", image)
# Pressionar qualquer tecla para saira
#key = cv2.waitKey(0)
#if key == ord("q"):
 #  sys.exit()
