import  sys
import numpy as np
import cv2
import subprocess

video = cv2.VideoCapture(-1)
video.set(160, 120)
# Captura os frames
status, imagem = video.read()
# Corta a imagem
cortar_imagem = imagem
start_height = cortar_imagem
# Converter para a cor cinza
efeito_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

cv2.imshow("Oi", imagem)
key = cv2.waitKey(0)
if key == ord("q"):
    sys.exit()
capture.release()