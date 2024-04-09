from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *

import sys
import cv2
import numpy as np

# 비디오 재생을 위해 스레드 생성, 사진 저장
import threading

#구간 지정 및 픽셀변화를 감지(이진화 시

class countingbox:
    up = 0 #클래스 변수
    down = 0
    def __init__(self, x, y, w, h, th, mod):
        self.initial_set()
        self.x = x #객체 변수
        self.y = y
        self.w = w
        self.h = h
        self.th = th
        self.p1 = (self.x, self.y)
        self.p2 = (self.x +self.w, self.y + self.h)
        self.mod = mod
    def initial_set(self):
        self.passing_state = False

    def counting(self, img, imgDil):
        recorte = imgDil[self.y:self.y + self.h, self.x:self.x + self.w]
        self.brancos = cv2.countNonZero(recorte)
        if self.brancos > self.th and self.passing_state == True:  # 영역 내 사람이 생겼을 때
            if self.mod == 'up':
                countingbox.up += 1
            elif self.mod == 'down':
                countingbox.down += 1
        if self.brancos < self.th:  # 영역 내 사람 없을 때
            self.passing_state = True
        else:  # 영역 내 사람이 여전히 있을 때, 지나가는중
            self.passing_state = False

        if self.passing_state == False:
            cv2.rectangle(img, self.p1, self.p2, (0, 255, 0), 4)
        else:
            cv2.rectangle(img, self.p1, self.p2, (255, 0, 255), 4)

        cv2.putText(img, str(self.brancos), (self.x - 30, self.y - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        return img, imgDil



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

        video = cv2.VideoCapture('passenger_01.mp4')
        up_l = countingbox(150, 600, 120, 30, 1000, 'up')
        down_l = countingbox(700, 600, 120, 30, 1000, 'down')
        down_r = countingbox(850, 600, 120, 30, 1000, 'down')

        kernelOp = np.ones((3, 3), np.uint8)

        while True:
            if self.run_flag:
                ret, img = video.read()
                if ret:
                    img = cv2.resize(img, (1100, 720))
                    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    # x,y,w,h = 490,230,30,150
                    # x, y, w, h = 150, 600, 120, 30
                    # x2, y2, w2, h2 = 275, 600, 120, 30
                    _, imgTh = cv2.threshold(imgGray, 100, 255, cv2.THRESH_BINARY_INV)
                    # imgTh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
                    kernel = np.ones((8, 8), np.uint8)
                    # imgDil = cv2.morphologyEx(imgTh, cv2.MORPH_OPEN, kernelOp)
                    imgDil = cv2.dilate(imgTh, kernel, iterations=2)
                    img, imgDil = up_l.counting(img, imgDil)
                    img, imgDil = down_l.counting(img, imgDil)
                    img, imgDil = down_r.counting(img, imgDil)
                    cv2.putText(img, f'up : {str(countingbox.up)}', (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
                    cv2.putText(img, f'down : {str(countingbox.down)}', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

                    self.display_output_image(img, mode=0)
                    self.display_output_image(imgDil, mode=1)
                    # cv2.imshow('video', cv2.resize(imgTh,(600,500)))
                    key = cv2.waitKey(20)
                    if key == 27:
                        break

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
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMain()
    sys.exit(app.exec_())