import sys
import subprocess as sp
import cv2
import numpy
import time

# Criando um objeto. 0 = Camera Externa
#video = cv2.VideoCapture(0)
video = cv2.VideoCapture(-1)
video.set(3, 360)
video.set(4, 640)
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
    roi = image[200:250, 0:639]
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    linha_preta = cv2.inRange(image, (0, 0, 0), (50, 50, 50))
    linha_verde = cv2.inRange(hsv, (36, 0, 0), (86, 255, 255))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)

    linha_verde = cv2.erode(linha_verde, kernel, iterations=5)
    linha_verde = cv2.dilate(linha_verde, kernel, iterations=9)
    contorno_preto, hierarquia_preta = cv2.findContours((linha_preta.copy()), (cv2.RETR_TREE), (cv2.CHAIN_APPROX_SIMPLE))
    contorno_verde, hierarquia_verde = cv2.findContours((linha_verde.copy()), (cv2.RETR_TREE), (cv2.CHAIN_APPROX_SIMPLE))
    #print(contorno_verde[0] > 1)
    #print(len(contorno_verde[0]))
    #print("Contorno preto = ", contorno_preto[0])
    try:
        if (len(contorno_verde[0])) > 1:
            x_verde, y_verde, w_verde, h_verde = cv2.boundingRect(contorno_verde[0])
            conversao_float_verde = int((w_verde / 2))
            centrox_verde = x_verde + conversao_float_verde
            #if centrox_verde >= 240 and centrox_verde <= 260:
             #   print("Verde (%s)"%(centrox_verde))
            print(w_verde)
            cv2.line(hsv, (centrox_verde, 200), (centrox_verde, 250), (0, 255, 0), 3)
    except:
        print("Nada")

    #x_preto, y_preto, w_preto, h_preto = cv2.boundingRect(contorno_preto[0])
    #conversao_float_preto = int(w_preto / 2)
    #print(conversao_float_preto)
    #cv2.line(image, (conversao_float_preto, 200), (conversao_float_preto, 250), (0, 0, 0), 3)
    #if verde_detectado == True:
     #   if conversao_float_verde > conversao_float_preto:
      #      cv2.putText(image, "Turn Right", (350, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
       # else:
        #    cv2.putText(image, "Turn Left", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
    #else:
     #   setpoint = 320
      #  error = conversao_float_preto - setpoint
       # textoCentral = ("Error: " + str(error))
        #\cv2.putText(image, textoCentral, (200, 340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
    cv2.imshow('frame', hsv)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #contours, hierarchy = cv2.findContours((linha_preta.copy()), (cv2.RETR_TREE), (cv2.CHAIN_APPROX_SIMPLE))
    #print(len(contours))
    #if len(contours) > 0:
     #   c = max(contours, key=cv2.contourArea) ## CODIGO DE DESENHO 1
      #  M = cv2.moments(c) ## CODIGO DE DESENHO 1

       # cx = int(M['m10']/M['m00']) ## CODIGO DE DESENHO 1
       # cy = int(M['m01']/M['m00']) ## CODIGO DE DESENHO 1
       # cv2.line(image,(cx,0),(cx,720),(255,0,0),1) #Linha Vertical
       # cv2.line(image,(0,cy),(1280,cy),(255,0,0),1) #Linha horizontal   ## CODIGO DE DESENHO 1
       # cv2.drawContours(image, contours, -1, (0,255,0), 1) # Desenhar a area detectada


        #x, y, w, h = cv2.boundingRect(contours[0])
        #cv2.line(image, (x + (w / 2)), (200), (x + (w / 2)), (250), (255, 0, 0), (3))
        ##cv2.line(image, (x + (w // 2),  200), (x + (w // 2), 250), (255, 0, 0), 3)
    #rawCapture.truncate(0)

#cv2.imshow("Gravando", image)
# Pressionar qualquer tecla para saira
#key = cv2.waitKey(0)
#if key == ord("q"):
 #  sys.exit()
