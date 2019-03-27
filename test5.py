import numpy as np
import cv2
import subprocess

video = cv2.VideoCapture(-1)
video.set(160, 120)

while(True):

    # Captura os frames
    status, imagem = video.read()
    # Corta a imagem
    cortar_imagem = imagem
    start_height = cortar_imagem
    # Converter para a cor cinza
    #efeito_cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    # Efeito de borrão na tela
    #borrao = cv2.GaussianBlur(efeito_cinza,(5,5),0)

    # Limiarização da cor
    #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    #frame_rgb = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)  # Drawing color points requires RGB image
    efeito_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    #img_blur = cv2.medianBlur(self.cropped_img, 5).astype('uint8')
    #src ksize dst
    #img_blur = cv2.medianBlur(imagem,5)
    separacao = cv2.adaptiveThreshold(efeito_cinza,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    #status, separacao = cv2.threshold(imagem,60,255,cv2.THRESH_BINARY_INV)
    signed_thresh = separacao[start_height].astype(np.int16)# select only one row
    diff = np.diff(signed_thresh)
    points = np.where(np.logical_or(diff > 200, diff < -200))
    #Achar as linhas da imagem
    #contorno, hierarquia = cv2.findContours(separacao.copy(), 1, cv2.CHAIN_APPROX_NONE)
    #cv2.line(frame_rgb, (0), (start_height), (640), (start_height), (0, 255, 0), (1))
    # Acha o maior contorno (se detectado)
    print(len(points))
    print(points)
    if len(points) > 0: #Verifica se algum contorno é detectado. Se algum contorno for detectado, ele encontrará aquele com a maior área e, em seguida, localizará a coordenada X central (cx) e a coordenada Y (cy) desse contorno.
#and len(points[0]) > 1
        middle = (points[0][0] + points[0][1]) / 2

        cv2.circle(frame_rgb, (points[0][0], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (points[0][1], start_height), 2, (255,0,0), -1)
        cv2.circle(frame_rgb, (middle, start_height), 2, (0,0,255), -1)

        if middle >= 120:
            print("Vire a esquerda! (%s)"%(middle))

        if middle < 120 and middle > 50:
            print("Na rota! (%s)"%(middle))

        if middle <= 50:
            print("Vire a direita!(%s)"%(middle))
    #Se nenhuma linha for detectada:
    else:
        print("Linha não detectada")
        print(middle)
#Mostrar o quadro
    cv2.imshow('frame',imagem)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break