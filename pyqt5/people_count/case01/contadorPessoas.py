#구간 내 픽셀 수 변화 감지

import cv2
import numpy as np

video = cv2.VideoCapture('escalator.mp4')
contador = 0
passing_state = False

while True:
    ret,img = video.read()
    img = cv2.resize(img,(1100,720),)
    imgGray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    x,y,w,h = 490,230,30,150
    imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((8,8), np.uint8)

    imgDil = cv2.dilate(imgTh,kernel,iterations=2)
    cv2.imshow('TH', imgDil)

    recorte = imgDil[y:y+h,x:x+w]
    brancos = cv2.countNonZero(recorte)

    if brancos > 4000 and passing_state == True: #영역 내 사람이 생겼을 때
        contador +=1
    if brancos < 4000: # 영역 내 사람 없을 때
        passing_state = True
    else: #영역 내 사람이 여전히 있을 때, 지나가는중
        passing_state =False

    if passing_state == False:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    else:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255, 0, 255),4)

    cv2.rectangle(imgTh, (x, y), (x + w, y + h), (255, 255, 255), 6)

    cv2.putText(img,str(brancos),(x-30,y-50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),1)
    cv2.rectangle(img, (575,155), (575 + 88, 155 + 85), (255, 255, 255), -1)
    cv2.putText(img, str(contador), (x+100, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5)

    #print(contador)
    cv2.imshow('video original',img)
    #cv2.imshow('video', cv2.resize(imgTh,(600,500)))
    cv2.waitKey(20)