import sys
import subprocess as sp
import cv2
import numpy
import time

# Criando um objeto. 0 = Camera Externa
#video = cv2.VideoCapture(0)
video = cv2.VideoCapture(-1)
video.set(3, 640)
video.set(4, 360)
video.set(5, 60)
#video.set(4, 360)
#capture.set(5, 20) #set FPS
#capture.set(cv2.CAP_PROP_FPS, 60)
#cv2.CAP_PROP_FRAME_COUNT

#capture.set(10, 20) #set brightness
# Create um frame
#check, frame = video.read()
#print(check)
# print(frame)
a = "a"#90
while True:
    successful, image = video.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    roi = hsv[200:250, 0:639] # Cortar a imagem em forma de retangulo
    linha_preta = cv2.inRange(roi, (0, 0, 0), (50, 50, 50))
    sinal_verde = cv2.inRange(roi, (0, 65, 0), (100, 200, 100))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=5)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=9)
    contours_preto, hierarquia_preto = cv2.findContours(linha_preta.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_verde, hierarquia_verde = cv2.findContours(sinal_verde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    try:
        if len(contours_verde) > 0:
            Verde = True
            x_verde, y_verde, w_verde, h_verde = cv2.boundingRect(contours_preto[0])
            centerx_verde0 = x_verde + (w_verde / 2)
            centerx_verde = (int(centerx_verde0))
            cv2.line(image, (centerx_verde, 200), (centerx_verde, 250), (0, 0, 255), 3)
            print("Verde Detectado")
    except:
        Verde = False
        print("Verde : (%s)" % (Verde))
    if len(contours_preto) > 0:
        Preto = True
        x_preto, y_preto, w_preto, h_preto = cv2.boundingRect(contours_preto[0])
        centerx_preto0 = x_preto + (w_preto / 2)
        centerx_preto = (int(centerx_preto0))
        cv2.line(image, (centerx_preto, 200), (centerx_preto, 250), (0, 0, 255), 3)
        print(Preto)
        lower = numpy.array([50,50,50])
        upper = numpy.array([0,0,0])
        mask = cv2.inRange(image, upper, lower)
    #if len(contours_preto) > 0:
        #c = max(contours, key=cv2.contourArea) ## CODIGO DE DESENHO 1
        #M = cv2.moments(c) ## CODIGO DE DESENHO 1

        #cx = int(M['m10']/M['m00']) ## CODIGO DE DESENHO 1
        #cy = int(M['m01']/M['m00']) ## CODIGO DE DESENHO 1
        #cv2.line(hsv,(cx,0),(cx,720),(255,0,0),1) #Linha Vertical
        #cv2.line(hsv,(0,cy),(1280,cy),(255,0,0),1) #Linha horizontal   ## CODIGO DE DESENHO 1
        #cv2.drawContours(hsv, contours, -1, (0,255,0), 1) # Desenhar a area detectada
     #   x,y,w,h = cv2.boundingRect(contours_preto[0])
      #  cv2.line(image, (x + (w // 2), 200), (x + (w // 2), 200), (255, 0, 0), 3)
       # print(len(contours_preto))
        #x, y, w, h = cv2.boundingRect(contours[0])
        #cv2.line(image, (x + (w / 2)), (200), (x + (w / 2)), (250), (255, 0, 0), (3))
        ##cv2.line(image, (x + (w // 2),  200), (x + (w // 2), 250), (255, 0, 0), 3)
        #lower = numpy.array([50,50,50])
        #upper = numpy.array([0,0,0])
        #mask = cv2.inRange(image, upper, lower)
    #rawCapture.truncate(0)
    cv2.imshow('frame', sinal_verde)
    cv2.imshow("mask", mask)
    cv2.imshow("roi", roi)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#cv2.imshow("Gravando", image)
# Pressionar qualquer tecla para saira
#key = cv2.waitKey(0)
#if key == ord("q"):
 #  sys.exit()
