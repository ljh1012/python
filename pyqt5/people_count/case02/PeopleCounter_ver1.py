from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *

import sys
import cv2 as cv
import numpy as np
import Person
import time

# 비디오 재생을 위해 스레드 생성, 사진 저장
import threading


form_class = uic.loadUiType('person.ui')[0]
class MyMain(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.btn_load.clicked.connect(self.btn_load_clicked)

    def btn_load_clicked(self):
        self.video_thread()

#동영상 실행
########################################################################################################################

    def video_thread(self):
        self.thread = threading.Thread(target=self.video_to_frame, args=(self,))
        self.thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        self.thread.start()
        self.run_flag = True


    def video_to_frame(self, MainWindow):
        try:
            self.log = open('log.txt', "w")
        except:
            print("No se puede abrir el archivo log")

        # Contadores de entrada y salida
        cnt_up = 0
        cnt_down = 0


        self.cap = cv.VideoCapture('Test Files/TestVideo.avi')  # cam open

        for i in range(19):
            print(i, self.cap.get(i))

        h = 480
        w = 640
        frameArea = h * w
        areaTH = frameArea / 250  # 1228
        print('Area Threshold', areaTH)


        line_up = int(2 * (h / 5))
        line_down = int(3 * (h / 5))

        up_limit = int(1 * (h / 5))
        down_limit = int(4 * (h / 5))

        print("Red line y:", str(line_down))  # 288(y)
        print("Blue line y:", str(line_up))  # 192(y)
        line_down_color = (255, 0, 0)  # Blue
        line_up_color = (0, 0, 255)  # Red
        pt1 = [0, line_down];  # [0, 288]
        pt2 = [w, line_down];  # [640, 288]
        pts_L1 = np.array([pt1, pt2], np.int32)
        pts_L1 = pts_L1.reshape((-1, 1, 2))
        pt3 = [0, line_up];  # [0, 192]
        pt4 = [w, line_up];  # [640, 192]
        pts_L2 = np.array([pt3, pt4], np.int32)
        pts_L2 = pts_L2.reshape((-1, 1, 2))

        pt5 = [0, up_limit];
        pt6 = [w, up_limit];
        pts_L3 = np.array([pt5, pt6], np.int32)
        pts_L3 = pts_L3.reshape((-1, 1, 2))
        pt7 = [0, down_limit];
        pt8 = [w, down_limit];
        pts_L4 = np.array([pt7, pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1, 1, 2))

        fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)  # 배경 추청 알고리즘


        kernelOp = np.ones((3, 3), np.uint8)
        kernelOp2 = np.ones((5, 5), np.uint8)
        kernelCl = np.ones((11, 11), np.uint8)

        # Variables
        font = cv.FONT_HERSHEY_SIMPLEX
        persons = []
        max_p_age = 5
        pid = 1

        while (self.cap.isOpened()):

            ret, frame = self.cap.read()
            if ret:
                fgmask = fgbg.apply(frame)
                fgmask2 = fgbg.apply(frame)

                try:
                    ret, imBin = cv.threshold(fgmask, 200, 255, cv.THRESH_BINARY)
                    ret, imBin2 = cv.threshold(fgmask2, 200, 255, cv.THRESH_BINARY)
                    # Opening (erode->dilate) para quitar ruido.
                    mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
                    mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
                    # Closing (dilate -> erode) para juntar regiones blancas.
                    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernelCl)  # gray
                    mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)  # gray
                except:
                    print('EOF')
                    print('UP:', cnt_up)
                    print('DOWN:', cnt_down)
                    break

                contours0, hierarchy = cv.findContours(mask2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 사람 검출
                for cnt in contours0:
                    area = cv.contourArea(cnt)
                    if area > areaTH:
                        M = cv.moments(cnt)  # 사람의 moment
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        x, y, w, h = cv.boundingRect(cnt)  #

                        new = True
                        if cy in range(up_limit, down_limit):  # 1/5 ~ 4/5
                            for i in persons:
                                if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                    # n-1프레임에 검출된 사람이 n프레임에 검출된 사람과 동일한 경우, 전 프레임과 현재 프레임에서 같은 사람임을 인식하는 방법
                                    new = False
                                    i.updateCoords(cx, cy)
                                    if i.going_UP(line_down, line_up) == True:
                                        cnt_up += 1;
                                        print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                                        self.log.write(
                                            "ID: " + str(i.getId()) + ' crossed going up at ' + time.strftime("%c") + '\n')
                                    elif i.going_DOWN(line_down, line_up) == True:
                                        cnt_down += 1;
                                        print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                                        self.log.write("ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime(
                                            "%c") + '\n')
                                    break
                                if i.getState() == '1':  # going_UP or DOWN이 실행된 사람 -> Person.py - def going_UP and DOWN 확인, self.dir, self.state
                                    if i.getDir() == 'down' and i.getY() > down_limit:
                                        i.setDone()
                                    elif i.getDir() == 'up' and i.getY() < up_limit:
                                        i.setDone()
                                if i.timedOut():
                                    index = persons.index(i)
                                    persons.pop(index)
                                    del i
                            if new == True:  # 첫 검출된 사람 인식
                                p = Person.MyPerson(pid, cx, cy, max_p_age)
                                persons.append(p)
                                pid += 1
                        cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                        img = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                for i in persons:
                    cv.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv.LINE_AA)

                str_up = 'UP: ' + str(cnt_up)
                str_down = 'DOWN: ' + str(cnt_down)
                frame = cv.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
                frame = cv.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
                frame = cv.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
                frame = cv.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
                cv.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)  # 흰 테두리에 파란 글자
                cv.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv.LINE_AA)
                cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv.LINE_AA)  # 흰 테두리에 파란 글자
                cv.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv.LINE_AA)

                self.display_output_image(frame, mode=0)
                self.display_output_image(mask, mode=1)


    def display_output_image(self, img_dst, mode):
        h, w = img_dst.shape[:2]  # 그레이영상의 경우 ndim이 2이므로 h,w,ch 형태로 값을 얻어올수 없다

        if img_dst.ndim == 2:
            qImg = QImage(img_dst, w, h, w * 1, QImage.Format_Grayscale8)
        else:
            bytes_per_line = img_dst.shape[2] * w
            qImg = QImage(img_dst, w, h, bytes_per_line, QImage.Format_BGR888)

        self.pixmap = QtGui.QPixmap(qImg)
        p = self.pixmap.scaled(600, 450, QtCore.Qt.KeepAspectRatio)  # 프레임 크기 조정
        # p = self.pixmap.scaled(600, 450, QtCore.Qt.IgnoreAspectRatio)  # 프레임 크기 조정

        if mode == 0:
            self.lbl_src.setPixmap(p)
            self.lbl_src.update()  # 프레임 띄우기
        else:
            self.lbl_dst.setPixmap(p)
            self.lbl_dst.update()  # 프레임 띄우기

        # sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임

########################################################################################################################


########################################################################################################################


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                               "종료 하시겠습니까?",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.run_flag = False  # Video_to_frame에 while문에 사용(강제종료시 에러문제)
            self.cap.release()
            self.log.flush()
            self.log.close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMain()
    sys.exit(app.exec_())