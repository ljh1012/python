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




form_class = uic.loadUiType('ui/my_ui_window_video_ver2.ui')[0]
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
        path = ''
        filter = "All Videos(*.mp4; *.mov; *.avi);;MOV (*.mov);;MP4(*.mp4);;AVI(*.avi)"
        fname = QFileDialog.getOpenFileName(self, "파일로드", path, filter)
        self.filename = str(fname[0])
        self.line_load.setText(self.filename)
        self.video_thread()

    def btn_run_clicked(self):
        if self.run_flag != True:
            pass
        else:
            if self.out_check == 0 or self.out_check == 2:
                self.out_check = 1
                self.btn_run.setText("정지")
            else:
                self.out_check = 2
                self.btn_run.setText("진행")

    def initial_value(self):
        self.save_count = 0     #btn_save_clicked, save 횟수
        self.hslider_v = 127    #setslider, self.hslider_1.Value의 초기값
        self.hslider_m = 255    #setslider, self.hslider_2.value의 초기값
        self.run_flag = False   #flag, video_thread 시작
        self.out_check = 0  # btn_run_clicked, flag, lbl_dst 출력중 = 1, 중지 = 2
    def initial_cbox_value(self):
        self.binary = ['cv2.THRESH_BINARY', 'cv2.THRESH_BINARY_INV', 'cv2.THRESH_TRUNC', 'cv2.THRESH_TOZERO',
                       'cv2.THRESH_TOZERO_INV'] # cbox_bin
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
        cap = cv2.VideoCapture(self.filename)  # 저장된 영상 가져오기 프레임별로 계속 가져오는 듯
        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        while self.run_flag:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.ret, self.frame = cap.read()  # 영상의 정보 저장
            if self.ret:
                self.display_output_image(self.frame, 0)
                if self.out_check == 1:
                    self.process_result()
                    self.display_output_image(self.frame_out, 1)
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_result(self):
        if self.currentText == 'GRAY':
            self.frame2 = self.frame
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

        sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임

########################################################################################################################


#편집 및 저장
########################################################################################################################

    def btn_apply_clicked(self):
        self.hslider_v = self.hslider_1.value()
        self.hslider_m = self.hslider_2.value()
        self.currentText = self.cbox_scale.currentText()
        self.bin_cur_text = self.cbox_bin.currentText()
        if self.out_check == 2 and self.currentText == 'GRAY':
            self.frame_out1 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2GRAY)
            self.apply_binary(self.bin_cur_text)
            self.display_output_image(self.frame_out, 1)
        elif self.out_check == 2 and self.currentText == 'HSV':
            self.frame_out1 = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2HSV)
            self.apply_hsv(self.bin_cur_text)
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