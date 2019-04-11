import time
import math
import sys
import numpy
import cv2
#camera = 0
video = cv2.VideoCapture(-1)
#print(video)
#video = numpy.array(video, numpy.uint8)
video.set(3, 600)
video.set(4, 400)

x_last = 320
y_last = 180
tempo_inicial = time.time()
print("Tempo inicial ", tempo_inicial)
contador = 0
#print("ABCCC")
# se a camera falhar, repetir o processo de abertura
a = "a"
# only attempt to read if it is opened

while True:
    contador += 1
    sucessfullly, imagem = video.read()
    orig = (imagem.shape[1], imagem.shape[0])
    hsv = imagem
    hsv = cv2.cvtColor(imagem, cv2.COLOR_RGB2HSV)
    bgr = imagem
    bgr = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
    # cortada = imagem[140:150, 200:800]
    cortada = bgr[200:250, 0:900]
    linha_preta = cv2.inRange(imagem, (0, 0, 0), (32, 255, 21))
    sinal_verde = cv2.inRange(hsv, (32, 100, 82), (60, 255, 255))
    # sinal_verde = cv2.inRange(hsv, (23, 120, 35), (60, 255, 255))
    kernel = numpy.ones((3, 3), numpy.uint8)
    linha_preta = cv2.erode(linha_preta, kernel, iterations=2)
    linha_preta = cv2.dilate(linha_preta, kernel, iterations=9)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=5)
    sinal_verde = cv2.erode(sinal_verde, kernel, iterations=9)
    contours_preto, hierarchy_blk = cv2.findContours(linha_preta.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_verde, hierarchy_grn = cv2.findContours(sinal_verde.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # for c in contours_preto:
    #     if cv2.contourArea(c) <= 50:
    #         continue
    #     x, y, w, h = cv2.boundingRect[contours_preto[0]]
    #     cv2.rectangle(imagem, (a, b), (a + c, b + d), (0, 255, 0), 2)
    #     center = (a, b)
    #     print(center)
    print("OK")
    # print(contours_verde)
    # print(len(contours_verde))
    Verde_detectado = False
    if len(contours_verde) > 0:
        Verde_detectado = True
        x_verde, y_verde, w_verde, h_verde = cv2.boundingRect(contours_verde[0])
        pt = (x_verde, y_verde + h_verde)
        dist = math.sqrt((pt[0] - orig[0]) ** 2 + (pt[1] - orig[1]) ** 2)
        # print(dist)
        # print(contours_verde[0])
        centerx_verde0 = x_verde + (w_verde / 2)
        # print(centerx_verde0)
        centerx_verde = (int(centerx_verde0))
        # cv2.line(cortada, (centerx_verde, 200), (centerx_verde, 250), (0, 255, 0), 3)
        setpoint2 = 320
        # error2 = int(x_verde - setpoint2)
        # error22 = abs(error2)
        # print(error22)
        # print("Angulo verde: ", error2)
        # cv2.putText(image, ("Posicao verde (%s)" % (error2)), (30, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
    contours_preto_len = len(contours_preto)
    print(contours_preto_len)
    if contours_preto_len > 0:
        if contours_preto_len == 1:
            area_preta = cv2.minAreaRect(contours_preto[0])
        else:
            candidatos = []
            botao_off = 0
            for con_num in range(contours_preto_len):
                area_preta = cv2.minAreaRect(contours_preto[con_num])
                # x_bound, y_bound, w_bound, h_bound = cv2.boundingRect(contours_preto[0])
                # cv2.rectangle(imagem, (x_bound, y_bound), (x_bound + w_bound, y_bound+h_bound), (255,0,0),3)
                (x_minimo, y_minimo), (w_minimo, h_minimo), angulo = area_preta
                area_preta = cv2.minAreaRect(contours_preto[0])
                box = cv2.boxPoints(area_preta)
                box = numpy.int0(box)
                x_box, y_box = box[0]
                if y_box > 358:
                    botao_off += 1
                candidatos.append((y_box, con_num, x_minimo, y_minimo))
            candidatos = sorted(candidatos)
            if botao_off > 1:
                candidatos_botao_off = []
                for con_num in range((contours_preto_len - botao_off), contours_preto_len):
                    (y_maior, con_maior, x_minimo, y_minimo) = candidatos[con_num]
                    distancia_total = (abs(x_minimo - x_last) ** 2 + abs(y_minimo - y_last) ** 2) ** 0.5
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
        angulo = int(angulo)
        cv2.circle(imagem, (x_box, y_box), 10, (255, 0, 255), 3)
        # x_box, y_box = box[1]
        cv2.circle(imagem, (x_box, y_box), 10, (0, 0, 255), 3)
        if angulo < -45:
            angulo = 90 + angulo
        if w_minimo < h_minimo and angulo > 0:
            angulo = (90 - angulo) * -1
        if w_minimo > h_minimo and angulo < 0:
            angulo = 90 + angulo
        ag = box.flat[0]
        # cv2.circle(imagem, (ag, 200), 10, (153, 51, 153), 3)
        x_pretum, y_pretum, w_pretum, h_pretum = cv2.boundingRect(contours_preto[0])
        setpoint = 320
        error = int(x_minimo - setpoint)
        box = cv2.boxPoints(area_preta)
        box = numpy.int0(box)
        cv2.putText(imagem, str(angulo), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.drawContours(imagem, [box], 0, (0, 0, 255), 3)
        cv2.putText(imagem, ("Posicao preta (%s)" % (str(ag))), (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(imagem, (str(error)), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.drawContours(imagem, contours_preto, -1, (0, 255, 0), 3)
        cv2.line(imagem, (int(x_minimo), 200), (int(x_minimo), 250), (255, 0, 0), 3)
        # cv2.line(imagem, (int(x_minimo), 200), (int(x_minimo), 250), (211, 0, 148), 3)
        # angulo = int(angulo)

        Preto = True
        # cv2.line(imagem, (centerx_preto, 200), (centerx_preto, 250), (255, 0, 0), 3)
        if Preto == True:
            print(".....")
    # angulo = int(angulo)
    # print("AG", ag)
    # print("X pretum :", x_pretum) ## # AG = Valor da area preto
    # if error_pretum == 0:
    #    m.run_forever(speed_sp=100)
    #    n.run_forever(speed_sp=100)
    # elif error_pretum > 0:
    #    n.run_to_rel_pos(position_sp=valor_angulo, speed_sp=100, stop_action="hold")
    #    print("A")
    # elif error_pretum < 0:
    #    valor_angulo = error_pretum
    #    m.run_to_rel_pos(position_sp=valor_angulo, speed_sp=100, stop_action="hold")
    if Verde_detectado == True:
        if dist < 500:
            Esquerda = False
            Direita = True
            cv2.putText(imagem, "Vire a direita", (350, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            print("Direita Direita Direita Direita Direita")
        elif dist > 500:
            Esquerda = True
            Direita = False
            print("Esquerda")
            cv2.putText(imagem, "Vire a esquerda", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        # elif len(contours_verde) == 0 and len(contours_preto) == 0
        # else:
        #   setpoint = 320
        #      # Apenas mostrar a camera se estiver algo
        # if re:
        #   print("Imagem OK")
        #       #cv2.imshow("video output", img)
        #  # se nao tiver nada, abotar
        #  print("Erro lendo camera")
        # sleep(10)
        # sys.exit()
    # else:
    #   print( "Erro lendo camera")
    #  k = cv2.waitKey(10) & 0xFF
    # if k == 27:
    #    sys.exit()
    # else:
    #   setpoint = 320
    #  errorv = centerx_preto - setpoint
    # centertext = ("Error " + str(errorv))
    # cv2.putText(imagem, centertext, (200,340), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 3)
    cv2.imshow("Oi", imagem)
    cv2.imshow("tchau", cortada)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    elif key == ord("r"):
        getROI = False
tempo_final = time.time()
#print("Tempo final", tempo_final)
#print("ada", contador)
#print(tempo_final - tempo_inicial)
fps = contador / (tempo_final - tempo_inicial)
#rint(contador)
print("FPS = " + str(fps))
#print()
