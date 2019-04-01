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
#video.set(5, 60)
#video.set(4, 360)
#capture.set(5, 20) #set FPS
video.set(cv2.CAP_PROP_FPS, 60)

x_last = 320
y_last = 180
a = "a"#90
while True:
    successful, image = video.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #roi = hsv[200:250, 0:639] # Cortar a imagem em forma de retangulo
    linha_preta = cv2.inRange(hsv, (0, 0, 0), (75, 75, 75))
    sinal_verde = cv2.inRange(hsv, (0, 65, 0), (100, 200, 100))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=5)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=9)
    contours_preto, hierarquia_preto = cv2.findContours(linha_preta.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_verde, hierarquia_verde = cv2.findContours(sinal_verde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    lower = numpy.array([50, 50, 50])
    upper = numpy.array([0, 0, 0])
    mask = cv2.inRange(image, upper, lower)
    Verde_detectado = False
    #print(len(contours))
   # try:
    contours_preto_len = len(contours_preto)
    if contours_preto_len> 0:
        if contours_preto_len == 1:
            area_preta = cv2.minAreaRect(contours_preto[0])
        else:
            candidates = []
            botao_off = 0
            for contours_num in range(contours_preto_len):
                area_preta = cv2.minAreaRect(contours_preto[contours_num])
                (x_minimo, y_minimo), (w_minimo, h_minimo), angulo = area_preta
                area = cv2.boxPoints(area_preta)
                (x_area,y_area) = area[0]
                if y_area > 358:
                    botao_off += 1
                    candidates.append((y_area,contours_num,x_minimo,y_minimo))
            candidates = sorted(candidates)
            if botao_off > 1:
                candidates_botao_off=[]
                for contours_num in range((contours_preto_len - botao_off), contours_preto_len):
                    (y_maior,contours_maior,x_minimo,y_minimo) = candidates[contours_num]
                    distancia_total = (abs(x_minimo - x_last)**2 + abs(y_minimo - y_last)**2)**0.5
                candidates_botao_off = sorted(candidates_botao_off)
                (distancia_total,contours_maior) = candidates_botao_off[0]
                area_preta = cv2.minAreaRect(contours_preto[contours_maior])
            else:
                (y_maior,contours_maior,x_minimo,y_minimo) =  candidates[contours_preto_len-1]
                area_preta = cv2.minAreaRect(contours_preto[contours_maior])
    (x_minimo, y_minimo), (w_minimo, h_minimo), angulo = area_preta
    x_last = x_minimo
    y_last = y_minimo
    if angulo < -45:
        angulo = 90 + angulo
    if w_minimo < h_minimo and angulo > 0:
        angulo = (90 - angulo) * -1
    if w_minimo > h_minimo and angulo < 0:
        angulo = 90 + angulo
    setpoint = 320
    error = int(x_minimo - setpoint)
    angulo = int(angulo)
    area = cv2.boxPoints(area_preta)
    area = numpy.int0(area)
    Preto = True
    cv2.drawContours(image, [area], 0, (0, 0, 255), 3)
    cv2.putText(image, str(angulo), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, str(error), (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.line(image, (int(x_minimo), 200), (int(x_minimo), 250), (255, 0, 0), 3)
    x_preto, y_preto, w_preto, h_preto = cv2.boundingRect(contours_preto[0])
    centerx_preto0 = x_preto + (w_preto / 2)
    centerx_preto = (int(centerx_preto0))
    if Preto == True:
        print("Preto Detectado")
    #Verde = True
        Verde_detectado = True
        x_verde, y_verde, w_verde, h_verde = cv2.boundingRect(contours_verde[0])
        centerx_verde0 = x_verde + (w_verde / 2)
        centerx_verde = (int(centerx_verde0))
        cv2.line(image, (centerx_verde, 200), (centerx_verde, 250), (0, 255, 0), 3)
        print(centerx_verde)
    if Verde_detectado == True:
        if centerx_verde > centerx_preto:
            cv2.putText(image, "Vire a direita", (350,180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)
        else:
            cv2.putText(image, "Vire a esquerda", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            #elif len(contours_verde) == 0 and len(contours_preto) == 0
    else:
        setpoint = 320
        error = centerx_preto - setpoint
        centertext = "Erro = " + str(error)
        cv2.putText(image, centertext, (200,340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0),3)
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
    cv2.imshow('frame', image)
    cv2.imshow("mask", mask)
    #cv2.imshow("roi", roi)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
#cv2.imshow("Gravando", image)
# Pressionar qualquer tecla para saira
#key = cv2.waitKey(0)
#if key == ord("q"):
 #  sys.exit()
