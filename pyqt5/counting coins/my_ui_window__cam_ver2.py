from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *

import sys
import cv2
import numpy as np

from time import sleep, strftime, gmtime
# 비디오 재생을 위해 스레드 생성, 사진 저장
import threading

form_class = uic.loadUiType('ui/my_ui_window_cam_ver2.ui')[0]
class MyMain(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.btn_load.clicked.connect(self.btn_load_clicked)
        self.btn_run.clicked.connect(self.btn_run_clicked)
        self.btn_save.clicked.connect(self.btn_save_clicked)
        self.btn_apply.clicked.connect(self.btn_apply_clicked)
        self.setslider(self.hslider_1, self.hslider_value_th)
        self.setslider(self.hslider_2, self.hslider_value_max)
        self.cbox_scale.currentTextChanged.connect(self.fill_cbox_bin)
        self.initial_value()
        self.initial_cbox_value()

    def btn_load_clicked(self):
        self.path = self.line_load.text()
        self.video_thread()

    def btn_run_clicked(self):
        if self.run_flag != True:
            pass
        else:
            if self.out_check == 0 or self.out_check == 2:
                self.out_check = 1 #진행상태
                self.btn_run.setText("정지")
            else:
                self.out_check = 2 #정지상태
                self.btn_run.setText("진행")

    def initial_value(self):
        self.save_count = 0     #btn_save_clicked, save 횟수
        self.hslider_v = 127    #setslider, self.hslider_1.Value의 초기값
        self.hslider_m = 255    #setslider, self.hslider_2.value의 초기값
        self.run_flag = False   #flag, video_thread 시작
        self.out_check = 0  # btn_run_clicked, flag, lbl_dst 출력중 = 1, 중지 = 2
    def initial_cbox_value(self):
        self.binary = ['cv2.THRESH_BINARY', 'cv2.THRESH_BINARY_INV', 'cv2.THRESH_TRUNC', 'cv2.THRESH_TOZERO',
                       'cv2.THRESH_TOZERO_INV', 'Canny'] # cbox_bin
        self.HSV = ['H', 'S', 'V'] # cbox_bin
        self.currentText = 'GRAY' # btn_apply_clicked, currentText = cbox_scale.currentText()
        self.fill_cbox_bin()
        self.bin_cur_text = self.cbox_bin.currentText()

    def setslider(self, slider, sliderfunc):
        slider.setTickPosition(50)
        slider.setRange(0, 255)
        slider.setSingleStep(1)
        slider.valueChanged.connect(sliderfunc)

    def hslider_value_th(self, value):
        self.hslider_1.setValue = value
        self.hslider_1_v.setText(str(value))

    def hslider_value_max(self, value):
        self.hslider_2.setValue = value
        self.hslider_2_v.setText(str(value))

    def fill_cbox_bin(self):
        if self.cbox_scale.currentText() == 'GRAY':
            self.cbox_bin.clear()
            for i in self.binary:
                self.cbox_bin.addItem(i)
        if self.cbox_scale.currentText() == 'HSV':
            self.cbox_bin.clear()
            for i in self.HSV:
                self.cbox_bin.addItem(i)
#동영상 실행
########################################################################################################################

    def video_thread(self):
        self.thread = threading.Thread(target=self.video_to_frame, args=(self,))
        self.thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        self.thread.start()
        self.run_flag = True

    def video_to_frame(self, MainWindow):
        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        capture = cv2.VideoCapture(self.path)
        while self.run_flag:
            self.ret, frame = capture.read()  # 영상의 정보 저장
            frame = frame[20:, :460, :]
            self.frame = frame.copy() #line_134 오류 방지위해 .copy()
            if self.ret:
                #cut_h_start = 20
                #self.frame = self.frame[cut_h_start:self.frame.shape[0], 0:460, :]
                if self.out_check != 1:
                    self.display_output_image(self.frame, 0)
                elif self.out_check == 1:
                    self.process_result()
                    self.display_output_image(self.frame, 0)
                    self.display_output_image(self.frame_out, 1)
            else:
                break

        if self.capture.isOpened():
            self.capture.release()

    def process_result(self):
        if self.currentText == 'GRAY':
            self.frame2 = self.frame
            self.frame2 = cv2.GaussianBlur(self.frame2, (5, 5), 3)
            self.frame_out1 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)
            self.apply_binary(self.bin_cur_text)
        elif self.currentText == 'HSV':
            self.frame2 = self.frame
            self.frame_out1 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2HSV)
            self.apply_hsv(self.bin_cur_text)

    def display_output_image(self, img_dst, mode):
        h, w = img_dst.shape[:2]  # 그레이영상의 경우 ndim이 2이므로 h,w,ch 형태로 값을 얻어올수 없다
        if img_dst.ndim == 2:
            qImg = QImage(img_dst, w, h, w * 1, QImage.Format_Grayscale8)
        else:
            #bytes_per_line = img_dst.shape[2] * h
            #print(bytes_per_line)
            qImg = QImage(img_dst, w, h, img_dst.strides[0], QImage.Format_BGR888)

        self.pixmap = QtGui.QPixmap(qImg)
        p = self.pixmap.scaled(600, 450, QtCore.Qt.KeepAspectRatio)  # 프레임 크기 조정
        # p = self.pixmap.scaled(600, 450, QtCore.Qt.IgnoreAspectRatio)  # 프레임 크기 조정
        if mode == 0:
            self.lbl_src.setPixmap(p)
            self.lbl_src.update()  # 프레임 띄우기
        else:
            self.lbl_dst.setPixmap(p)
            self.lbl_dst.update()  # 프레임 띄우기

        sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임

########################################################################################################################


#편집 및 저장
########################################################################################################################

    def contour(self,img_proc):
        contours, hierarchy = cv2.findContours(img_proc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        count = 0
        money = 0
        for i, contour in enumerate(contours):
            # print(f'{i} : {cv2.contourArea(contour)}')
            area = cv2.contourArea(contour)
            if area >= 100:
                count += 1
                cv2.drawContours(self.frame, [contour], 0, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(contour)
                pt1 = (x, y)
                pt2 = (x + w, y + h)
                cv2.rectangle(self.frame, pt1, pt2, (255, 0, 0), 1)
                #### moment
                mu = cv2.moments(contour)
                cX = int(mu['m10'] / (mu['m00']) + 1e-5)
                cY = int(mu['m01'] / (mu['m00']) + 1e-5)
                cv2.circle(self.frame, (cX, cY), 5, (255, 255, 255), -1)
                cv2.putText(self.frame, f'{i}:{area}', (cX - 60, cY + 25),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 1)
                if 3000 < area < 3500:
                    #10원
                    money += 10
                elif 4200 < area < 4800:
                    #50원
                    money += 50
                elif 5200 < area < 5800:
                    #100원
                    money += 100
                elif 6500 < area < 7500:
                    #500원
                    money += 500
        cv2.rectangle(self.frame, (0, 420), (420, 460), (255, 0, 255), -1)
        cv2.putText(self.frame, f'coins : {count}, money : {money}', (0, 440), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (255, 255, 255), 1)

    def btn_apply_clicked(self):
        self.hslider_v = self.hslider_1.value()
        self.hslider_m = self.hslider_2.value()
        self.currentText = self.cbox_scale.currentText()
        self.bin_cur_text = self.cbox_bin.currentText()
        if self.out_check == 2 and self.currentText == 'GRAY':
            self.process_result()
            self.display_output_image(self.frame_out, 1)
    def apply_binary(self, state):
        if state == 'cv2.THRESH_BINARY':
            _, self.frame_out = cv2.threshold(self.frame_out1, self.hslider_v, self.hslider_m, cv2.THRESH_BINARY)
        elif state == 'cv2.THRESH_BINARY_INV':
            _, self.frame_out = cv2.threshold(self.frame_out1, self.hslider_v, self.hslider_m, cv2.THRESH_BINARY_INV)
        elif state == 'cv2.THRESH_TRUNC':
            _, self.frame_out = cv2.threshold(self.frame_out1, self.hslider_v, self.hslider_m, cv2.THRESH_TRUNC)
        elif state == 'cv2.THRESH_TOZERO':
            _, self.frame_out = cv2.threshold(self.frame_out1, self.hslider_v, self.hslider_m, cv2.THRESH_TOZERO)
        elif state == 'cv2.THRESH_TOZERO_INV':
            _, self.frame_out = cv2.threshold(self.frame_out1, self.hslider_v, self.hslider_m, cv2.THRESH_TOZERO_INV)
        elif state == 'Canny':
            frame_out = cv2.Canny(self.frame_out1, self.hslider_v, self.hslider_m)
            # dialation
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            img_dial = cv2.dilate(frame_out, kernel)
            self.frame_out = cv2.morphologyEx(img_dial,cv2.MORPH_CLOSE, kernel)
        self.contour(self.frame_out)
    def apply_hsv(self, state):
        if state =='H':
            if self.hslider_v > 180:
                self.hslider_v = 180
            if self.hslider_m > 180:
                self.hslider_m = 180
            if self.hslider_v <= self.hslider_m:
                mask = cv2.inRange(self.frame_out1, (self.hslider_v, 0, 0), (self.hslider_m, 255, 255))
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=mask)
            elif self.hslider_v > self.hslider_m:
                upper_red = cv2.inRange(self.frame_out1, (self.hslider_v, 0, 0), (180, 255, 255))
                lower_red = cv2.inRange(self.frame_out1, (0, 0, 0), (self.hslider_m, 255, 255))
                added_red = cv2.addWeighted(lower_red, 1.0, upper_red, 1.0, 0.0)
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=added_red)
        if state =='S':
            if self.hslider_v <= self.hslider_m:
                mask = cv2.inRange(self.frame_out1, (0, self.hslider_v, 0), (180, self.hslider_m, 255))
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=mask)
            if self.hslider_v > self.hslider_m:
                upper_mask = cv2.inRange(self.frame_out1, (0, self.hslider_v, 0), (180, 255, 255))
                lower_mask = cv2.inRange(self.frame_out1, (0, 0, 0), (180, self.hslider_m, 255))
                added_mask = cv2.addWeighted(lower_mask, 1.0, upper_mask, 1.0, 0.0)
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=added_mask)
        if state =='V':
            if self.hslider_v <= self.hslider_m:
                mask = cv2.inRange(self.frame_out1, (0, 0, self.hslider_v), (180, 255, self.hslider_m))
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=mask)
            if self.hslider_v > self.hslider_m:
                upper_mask = cv2.inRange(self.frame_out1, (0, 0, self.hslider_v), (180, 255, 255))
                lower_mask = cv2.inRange(self.frame_out1, (0, 0, 0), (180, 255, self.hslider_m))
                added_mask = cv2.addWeighted(lower_mask, 1.0, upper_mask, 1.0, 0.0)
                hsv = cv2.bitwise_and(self.frame_out1, self.frame_out1, mask=added_mask)
        self.frame_out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def btn_save_clicked(self):
        if self.out_check != 0:
            self.save_count += 1
            file = 'save_images/capture' + str(self.save_count) + '.png'
            cv2.imwrite(file, self.frame_out)
            file2 = file + ' saved'
            self.line_save.setText(file2)

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



    # def processing_image(self, img_gray, img_src):
    #     # 여기에 이미지 프로세싱을 진행하고 output으로 리턴하면 오른쪽에 결과 영상 출력됨
    #     # output = img_src.copy() #원본영상 그대로 리턴
    #     output = img_gray.copy()  # 그래이 영상 리턴
    #     return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMain()
    sys.exit(app.exec_())


