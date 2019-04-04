import sys
# import the necessary packages
import numpy as np
import imutils
import cv2

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
x_start, y_start, x_end, y_end = 0, 0, 0, 0
recorte = False #cropping
obterROI = False #getRPO
refPt = []
lower = np.array([])
upper = np.array([])

camera = cv2.VideoCapture(-1)


def obter_valor_cor(evento, x, y, flags, param): #click_and_crop # event
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, recorte, obterROI

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if evento == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        recorte = True

    elif evento == cv2.EVENT_MOUSEMOVE:
        if recorte == True:
            x_end, y_end = x, y

    # check to see if the left mouse button was released
    elif evento == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        x_end, y_end = x, y
        recorte = False
        obterROI = True


cv2.namedWindow("imagem")
cv2.setMouseCallback("imagem", obter_valor_cor)

# keep looping
while True:

    if not obterROI:

        while True:
            # grab the current frame
            (status, frame) = camera.read()

            if not status:
                break

            if not recorte and not obterROI:
                cv2.imshow("imagem", frame)

            elif recorte and not obterROI:
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                cv2.imshow("imagem", frame)

            elif not recorte and obterROI:
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
                cv2.imshow("imagem", frame)
                break

            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                sys.exit()
                #noROI = True
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        refPt = [(x_start, y_start), (x_end, y_end)]

        roi = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        #cv2.imshow("ROI", roi)

        hsvRoi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        print('minimo H = {}, minimo S = {}, minimo V = {} \nmaximo H = {}, maximo S = {}, maximo V = {}'.format(hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min(), hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()))
        lower = np.array([hsvRoi[:, :, 0].min(), hsvRoi[:, :, 1].min(), hsvRoi[:, :, 2].min()])
        upper = np.array([hsvRoi[:, :, 0].max(), hsvRoi[:, :, 1].max(), hsvRoi[:, :, 2].max()])
        minimo_H = (hsvRoi[:, :, 0].min())
        minimo_S = (hsvRoi[:, :, 1].min())
        minimo_V = (hsvRoi[:, :, 2].min())
        maximo_H = (hsvRoi[:, :, 0].max())
        maximo_S = (hsvRoi[:, :, 1].max())
        maximo_V = (hsvRoi[:, :, 2].max())

        # grab the current frame
    (status, frame) = camera.read()

    if not status:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=600)

    borrao = cv2.GaussianBlur(frame, (11, 11), 0) #blurred
    hsv = cv2.cvtColor(borrao, cv2.COLOR_BGR2HSV)

    # construct a mask for the color from dictionary`1, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    kernel = np.ones((9, 9), np.uint8)
    mascara = cv2.inRange(hsv, lower, upper)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    linha = cv2.findContours(mascara.copy(), cv2.RETR_EXTERNAL, #cnts
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    centro = None

    # only proceed if at least one contour was found
    if len(linha) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(linha, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size. Correct this value for your obect's size
        if radius > 0.5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.putText(frame, 'center: {}, {}'.format(int(x), int(y)), (int(x - radius), int(y - radius)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the frame to our screen
    lower_verde = np.array([minimo_H, minimo_S, minimo_V])
    upper_verde = np.array([maximo_V, maximo_S, maximo_V])
    mask = cv2.inRange(hsvRoi, lower_verde, upper_verde)
    res = cv2.bitwise_and(hsvRoi, hsvRoi, mask=mask)
    cv2.imshow("mask", mask)
    cv2.imshow("res", res)
    cv2.imshow("resultado", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    elif key == ord("r"):
        getROI = False

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
