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
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV )
    cortada = hsv[200:250, 0:639] # Cortar a imagem em forma de retangulo
    linha_preta = cv2.inRange(image, (0, 0, 0), (50, 50, 50))
    sinal_verde = cv2.inRange(cortada, (37, 246, 43), (60, 255, 255))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=5)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=5)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=9)
    contours_preto, hierarquia_preto = cv2.findContours(linha_preta.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_verde, hierarquia_verde = cv2.findContours(sinal_verde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    Verde_detectado = False
    if len(contours_verde) > 0:
        Verde_detectado = True
        x_verde, y_verde, w_verde, h_verde = cv2.boundingRect(contours_verde[0])
        centerx_verde0 = x_verde + (w_verde / 2)
        print(centerx_verde0)
        centerx_verde = (int(centerx_verde0))
        cv2.line(cortada, (centerx_verde, 200), (centerx_verde, 250), (0, 255, 0), 3)
        setpoint2 = 320
        error2 = int(x_verde - setpoint2)
        cv2.putText(image,("Posicao verde (%s)" %(error2)), (30, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    contours_preto_len = len(contours_preto)
    if contours_preto_len > 0:
        if contours_preto_len == 1:
            area_preta = cv2.minAreaRect(contours_preto[0])
        else:
            candidatos = []
            botao_off = 0
            for con_num in range(contours_preto_len):
                area_preta = cv2.minAreaRect(contours_preto[con_num])
                (x_minimo, y_minimo), (w_minimo, h_minimo), angulo = area_preta
                box = cv2.boxPoints(area_preta)
                (x_box, y_box) = box[0]
                x_preto, y_preto, w_preto, h_preto = cv2.boundingRect(contours_preto[0])
                centerx_preto0 = x_preto + (w_preto / 2)
                centerx_preto = (int(centerx_preto0))
                if y_box > 358:
                    botao_off += 1
                candidatos.append((y_box, con_num, x_minimo, y_minimo))
            candidatos = sorted(candidatos)
            if botao_off > 1:
                candidatos_botao_off = []
                for con_num in range((contours_preto_len - botao_off),  contours_preto_len):
                    (y_maior, con_maior, x_minimo, y_minimo) = candidatos[con_num]
                    distancia_total = (abs(x_minimo - x_last)** 2 + abs(y_minimo - y_last) ** 2) ** 0.5
                    candidatos_botao_off.append((distancia_total, con_maior))
                candidatos_botao_off = sorted(candidatos_botao_off)
                (distancia_total, con_maior) = candidatos_botao_off[0]
                area_preta = cv2.minAreaRect(contours_preto[con_maior])
            else:
                (y_maior, con_maior, x_minimo, y_minimo) = candidatos[contours_preto_len - 1]
                area_preta = cv2.minAreaRect(contours_preto[con_maior])
        (x_minimo, y_minimo), (w_minimo, h_minimo), angulo = area_preta
        x_last = x_minimo
        y_last = y_minimo
        if angulo < -45:
            angulo = 90 + angulo
        if w_minimo < h_minimo and angulo > 0:
            angulo = (90-angulo) * -1
        if w_minimo > h_minimo and angulo < 0:
            angulo = 90 + angulo
        setpoint = 320
        error = int(x_minimo - setpoint)
        angulo = int(angulo)
        box = cv2.boxPoints(area_preta)
        box = numpy.int0(box)
        Preto = True
        cv2.drawContours(image, [box], 0, (0,0,255), 3)
        cv2.putText(image, str(angulo), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, ("Posicao preta (%s)" %(error)), (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.line(image, (int(x_minimo), 200), (int(x_minimo), 250), (255, 0, 0), 3)
        #cv2.line(image, (centerx_preto, 200), (centerx_preto, 250), (255, 0, 0), 3)
        if Preto == True:
            print("")
    if Verde_detectado == True:
        if error2 > 0:
            Direita = True
            cv2.putText(image, "Vire a direita", (350,180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)
        elif error2 < 0:
            Esquerda = True
            cv2.putText(image, "Vire a esquerda", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            #elif len(contours_verde) == 0 and len(contours_preto) == 0
    else:
        setpoint = 320
        #error = centerx_preto - setpoint
    cv2.imshow('Imagem sem hsv', image)
    #cv2.imshow("Mascara preta", mask_black)
    #cv2.imshow("Imagem cortada em hsv", cortada)
    cv2.imshow("roi", cortada)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
