import numpy as np
import cv2


video = cv2.VideoCapture(-1)
video.set(3, 160)
video.set(4, 120)

while(True):

    # Captura os frames
    status, imagem = video.read()
    # Corta a imagem
    cortar_imagem = imagem[60:120, 0:160]

    # Converter para a cor cinza
    efeito_cinza = cv2.cvtColor(cortar_imagem, cv2.COLOR_BGR2GRAY)

    # Efeito de borrão na tela
    borrao = cv2.GaussianBlur(efeito_cinza,(5,5),0)

    # Limiarização da cor
    status, separacao = cv2.threshold(borrao,60,255,cv2.THRESH_BINARY_INV)

    #Achar as linhas da imagem
    contorno, hierarquia = cv2.findContours(separacao.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Acha o maior contorno (se detectado)
    if len(contorno) > 0: #Verifica se algum contorno é detectado. Se algum contorno for detectado, ele encontrará aquele com a maior área e, em seguida, localizará a coordenada X central (cx) e a coordenada Y (cy) desse contorno.
        c = max(contorno, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    #Desenha o contorno nas aréas obtidas
        cv2.line(cortar_imagem,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(cortar_imagem,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(cortar_imagem, contorno, -1, (0,255,0), 1)

        if cx >= 120:
            print("Vire a esquerda! (%s)"%(cx))

        if cx < 120 and cx > 50:
            print("Na rota! (%s)"%(cx))

        if cx <= 50:
            print("Vire a direita!(%s)"%(cx))
    #Se nenhuma linha for detectada:
    else:
        print("Linha não detectada")

#Mostrar o quadro
    cv2.imshow('frame',cortar_imagem)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break