import os
import sys
import cv2
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui, QtCore
import pandas as pd

form_class = uic.loadUiType('ui/my_ui_xray_ver3.ui')[0]
class MyMain(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.read_csv_data()
        self.show()

    def initUI(self):
        self.setWindowTitle('Image Load')
        self.btn_load.clicked.connect(self.dic_load)
        self.btn_prev.clicked.connect(self.btn_prev_clicked)
        self.btn_next.clicked.connect(self.btn_next_clicked)
        self.btn_add.clicked.connect(self.btn_add_clicked)
        self.btn_clear.clicked.connect(self.btn_clear_clicked)
        self.cbox_Sort.currentIndexChanged.connect(self.sorting)
        self.cbox_dir.currentIndexChanged.connect(self.directory_changed)
        self.flag()

    def read_csv_data(self):
        self.df = pd.read_csv('data/Data_Entry_2017.csv', encoding='CP949')
        self.bb = pd.read_csv('data/BBox_List_2017.csv', encoding='CP949')
        self.file_list = [] #조작 - def sorting(self): - (flag)
        label = list(set(self.bb['Finding Label'])) #self.cbox_Sort에 label 채워넣기
        self.cbox_Sort.addItem('All')
        for case in label:
            self.cbox_Sort.addItem(case)

    def flag(self):
        self.dname_flag = 0

#조작
########################################################################################################################

    def dic_load(self): # 최초 load 버튼
        target_path = './'
        self.dname = QFileDialog.getExistingDirectory(self, '폴더선택', target_path, QFileDialog.ShowDirsOnly)
        if self.dname:
            self.dname_flag = 1
            self.line_name.setText(self.dname)
        else:
            self.line_name.clear()

    def btn_add_clicked(self):
        cbox_dir_list = []
        for i in range(self.cbox_dir.count()):
            cbox_dir_list.append(self.cbox_dir.itemText(i))
        # 추가할 경로가 이미 self.cbox_dic에 있는지 확인, 없을 경우에만 추가
        if self.dname_flag == 1 and len(self.line_name.text()) != 0 and not self.line_name.text() in cbox_dir_list:
            dic = self.line_name.text()
            self.cbox_dir.addItem(dic)

    def btn_clear_clicked(self):
        self.cbox_dir.clear()
        self.clear_data()

    def directory_changed(self):
        if self.cbox_dir.count() > 0:
            self.cur_path = self.cbox_dir.currentText()
            self.sorting()

    def sorting(self):
        if self.cbox_dir.count() != 0:
            if self.cbox_Sort.currentText() != "All":
                self.file_list = os.listdir(self.cur_path)
                res1 = self.bb[self.bb['Finding Label'] == self.cbox_Sort.currentText()]
                self.file_list = list(set(self.file_list) & set(res1['Image Index'].values.tolist()))
                if self.file_list:
                    self.findex = 0
                    self.cur_fname = self.file_list[0]
                    self.data_load(self.cur_path + '/', self.cur_fname)
                else:
                    self.clear_data()

            elif self.cbox_Sort.currentText() == 'All':
                self.file_list = os.listdir(self.cur_path)
                if self.file_list:
                    self.findex = 0
                    self.cur_fname = self.file_list[0]
                    self.data_load(self.cur_path + '/', self.cur_fname)
                else:
                    self.clear_data()

    def btn_prev_clicked(self):
        if self.cbox_dir.count() > 0:
            if self.findex > 0:
                self.findex -= 1
                self.cur_fname = self.file_list[self.findex]
                self.data_load(self.cur_path + '/', self.cur_fname)

            else:
                self.line_index.setText('첫 번째 영상입니다.')

    def btn_next_clicked(self):
        if self.cbox_dir.count() > 0:
            if self.findex < len(self.file_list)-1:
                self.findex += 1
                self.cur_fname = self.file_list[self.findex]
                self.data_load(self.cur_path + '/', self.cur_fname)

            else:
                self.line_index.setText('마지막 영상입니다.')

#-----------------------------------------------------------------------------------------------------------------------

#작동
########################################################################################################################
    def data_load(self, path, name):
        self.image_load(path + name)
        self.load_info(name)


    def image_load(self, file_path): # load 및 좌우 버튼으로 이미지 표시
        img_array = np.fromfile(file_path, np.uint8)
        img_src = cv2.imdecode(img_array,cv2.IMREAD_COLOR)
        h, w, c = img_src.shape
        if img_src.ndim == 2: # 그래이 이미지
            qImg = QImage(img_src, w,h,img_src.strides[0], QImage.Format_Grayscale8)
        else:
            self.bbox_rectangle(img_src)
            bytes_per_line = img_src.shape[2]*w
            qImg = QImage(img_src,w,h,img_src.strides[0], QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(qImg)
        #QImage 는 입출력에 최적화되어 있으며 픽셀단위로 이미지를 다루는 용도로 사용되는 반면,
        #QPixmap 은 화면에 이미지를 출력하는 데 최적화되어 있다.

        p = pixmap.scaled(self.lbl_img.width(),
                          self.lbl_img.height(),
                          QtCore.Qt.KeepAspectRatio) # 가로세로 비율 유지
                          #QtCore.Qt.IgnoreAspectRatio) # 비율무시
        self.lbl_img.setPixmap(p)
        self.lbl_img.update()


    def bbox_rectangle(self, img_src): #병변 표시
        res2 = self.bb[self.bb['Image Index'] == self.cur_fname]
        if len(res2.index) == 0:
            pass
        elif len(res2.index) == 1:
            cv2.rectangle(img_src, (int(res2.iloc[0,2]), int(res2.iloc[0,3])),
                          (int(res2.iloc[0,2] + res2.iloc[0,4]), int(res2.iloc[0,3] + res2.iloc[0,5])),
                          (0, 255, 255), 3)
            cv2.putText(img_src, res2.iloc[0,1], (int(res2.iloc[0,2]), int(res2.iloc[0,3] + res2.iloc[0,5] + 25)),
                        cv2.FONT_ITALIC, fontScale=1, color=(0, 255, 255), thickness=3)
        else:
            for i in range(len(res2.index)):
                cv2.rectangle(img_src, (int(res2.iloc[i, 2]), int(res2.iloc[i, 3])),
                              (int(res2.iloc[i, 2] + res2.iloc[i, 4]), int(res2.iloc[i, 3] + res2.iloc[i, 5])),
                              (0, 255, 255), 3)
                cv2.putText(img_src, res2.iloc[i, 1],
                            (int(res2.iloc[i, 2]), int(res2.iloc[i, 3] + res2.iloc[i, 5] + 25)),
                            cv2.FONT_ITALIC, fontScale=1, color=(0, 255, 255), thickness=3)

    def load_info(self, filename): # 환자 정보(data_entry) 출력
        res = self.df[self.df['Image Index'] == filename]
        if len(res) != 0:
            self.line_index.setText(res.iloc[0,0])
            self.line_Labels.setText(res.iloc[0,1])
            self.line_FU.setText(str(res.iloc[0,2]))
            self.line_ID.setText(str(res.iloc[0,3]))
            self.line_Age.setText(str(res.iloc[0,4]))
            self.line_Gender.setText(res.iloc[0,5])
            self.line_View.setText(res.iloc[0,6])
            self.line_Original_Image.setText("(" + str(res.iloc[0,7]) + "  ,  " + str(res.iloc[0,8]) + ")")
            self.line_PixelSpacing.setText("(" + str(res.iloc[0,9]) + "  ,  " + str(res.iloc[0,10]) + ")")
        else:
            self.clear_data()

    def clear_data(self):
        self.lbl_img.clear()
        self.line_index.clear()
        self.line_Labels.clear()
        self.line_FU.clear()
        self.line_ID.clear()
        self.line_Age.clear()
        self.line_Gender.clear()
        self.line_View.clear()
        self.line_Original_Image.clear()
        self.line_PixelSpacing.clear()

#-----------------------------------------------------------------------------------------------------------------------

#메인
########################################################################################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMain()
    sys.exit(app.exec_())

#-----------------------------------------------------------------------------------------------------------------------
