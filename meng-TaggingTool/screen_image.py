import os
import re
import cv2
import sys
import shutil
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from IC_rec_window import Ui_MainWindow

#2019/02/11
import configparser

if getattr(sys,'frozen',False):
    file_dir = r'./image'
    file_dir_change = r'./image_qualified'
    file_dir_del = r'./image_unqualified'
    if not os.path.exists(file_dir_change):
        os.makedirs(file_dir_change)
    if not os.path.exists(file_dir_del):
        os.makedirs(file_dir_del)
elif __file__:
    # file_dir = r'../wrong_check/IC_gtdiff'
    file_dir = r'E:\youdunshuju\61daifen'
    file_dir_change = r'C:\Users\maoying\Desktop\real-rename\61real_tupian'
    file_dir_del = r'C:\Users\maoying\Desktop\replay-rename\61fanpai'
    if not os.path.exists(file_dir_change):
        os.makedirs(file_dir_change)
    if not os.path.exists(file_dir_del):
        os.makedirs(file_dir_del)


def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype = np.uint8),1)
    ##2019/02/11
    height,width=cv_img[:2]
    size=(600,350)
    cv_img=cv2.resize(cv_img,size,interpolation=cv2.INTER_AREA)

    return cv_img


def cv_imwrite(filename,src):
    cv2.imencode('.jpg',src)[1].tofile(filename)


# 2019/02/11   123
if getattr(sys,'frozen',False):
    config_dir = r'./config.ini'
    cf = configparser.ConfigParser()
    cf.read(config_dir)
    re_ori = cf.get("Re-IDCARD", "_re")
elif __file__:
    config_dir=r'.\config.ini'
    cf=configparser.ConfigParser()
    cf.read(config_dir)
    re_ori=cf.get("Re-IDCARD","_re")


class ID_CARD_UI(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ID_CARD_UI,self).__init__()
        self.setupUi(self)
        self.lbl_pic.setText('')
        self.lbl_label.setText('')

        self.index = 0
        self.files = []

        self.files_temp=[]

        self.file_name = ''
        self.base_file_name = ''
        self.new_file_name = ''

        self.image = np.array([])

        self.file_dir = file_dir
        self.file_dir_change = file_dir_change
        self.file_dir_del = file_dir_del


        self.stack_len = 4

        self.file_name_stack = []
        self.new_file_name_stack = []
        self.image_stack = []
        self.var_stack = []           #0对应delete,1对应next

        # 20190107新增
        self.file_name_stack_temp = ''
        self.new_file_name_stack_temp = ''

        self.lbl_num_act.setText('')
        self.lbl_num_sum.setText('')

        self.all_widget_init()

    def read_all_files(self):
        self.files = os.listdir(self.file_dir)
        self.files = [file for file in self.files if str(file).lower().endswith(('.jpg','.png'))]
        self.files_temp = self.files.copy()


    def QIM_From_Numpy(self,base_img):
        image_height, image_width, image_depth = base_img.shape  # 获取图像的高，宽以及深度。
        QIm = cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
        QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                     image_width * image_depth,
                     QImage.Format_RGB888)
        return QIm

    # 2019/02/11
    def Analysis_re(self,string):
        _file_name = str(eval(re_ori.replace('str', repr(string))))
        str_list=[]
        str_list.append(string[0:string.index(_file_name)])
        str_list.append(_file_name)
        str_list.append(string[string.index(_file_name)+len(_file_name):])
        return str_list



    def all_widget_init(self):
        self.read_all_files()
        if len(self.files) == 0 or self.files is None:
            # print("该文件夹没有目标文件.......")
            QtWidgets.QMessageBox.about(self,'提示','该文件夹没有目标文件......')
            sys.exit(0)
        else:
            self.file_name = self.files[self.index]
            self.image = cv_imread(os.path.join(self.file_dir, self.file_name))

            # print(self.image.shape)
            # cv2.imshow('pic',self.image)
            # cv2.waitKey(2)

            self.lbl_pic.setFocusPolicy(QtCore.Qt.NoFocus)
            ##
            # a=r'C:\Users\maoying\Desktop\address'
            # b='1430_ONEPLUSA50008.1.0_11545975065420_f@430723198911204012@胡安安@汉@杭州市余杭区闲林街道西市街竹海水韵竹邻间12幢2单元502室.jpg'
            # c=os.path.join(a,b)
            self.lbl_pic.setPixmap(QPixmap.fromImage(self.QIM_From_Numpy(self.image)))
            # self.lbl_pic.setPixmap(QPixmap(c))
            # self.lbl_label.setFocusPolicy(QtCore.Qt.NoFocus)

            # 2019/02/11
            # self.lbl_label.setText(os.path.splitext(self.file_name)[0].split('@')[1])
            str_list=self.Analysis_re(self.file_name)
            self.lbl_label.setText(str_list[1])

            self.lbl_num_sum.setFocusPolicy(QtCore.Qt.NoFocus)
            self.lbl_num_sum.setText('总张数：%s'%str(len(self.files)))
            self.lbl_num_act.setFocusPolicy(QtCore.Qt.NoFocus)
            self.lbl_num_act.setText('当前张数：%s'%str(self.index+1))

            self.pbt_next.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pbt_next.clicked.connect(self.pbt_next_click)

            self.pbt_back.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pbt_back.clicked.connect(self.pbt_back_click)

            self.pbt_del.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pbt_del.clicked.connect(self.pbt_del_click)


    def pbt_del_click(self):
        if len(self.file_name_stack) >= self.stack_len:
            self.image_stack.pop(0)
            self.file_name_stack_temp = self.file_name_stack.pop(0)
            self.new_file_name_stack_temp = self.new_file_name_stack.pop(0)

            # 2019/02/11
            str_list = self.Analysis_re(self.file_name_stack_temp)

            # 2019/02/11
            if self.var_stack.pop(0) == 0:
                shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_del,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))

            else:
                shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_change,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))


        self.file_name_stack.append(self.file_name)
        self.new_file_name_stack.append(self.lbl_label.text())
        self.image_stack.append(self.image)
        self.var_stack.append(0)

        self.files_temp[self.index] = self.lbl_label.text()

        if self.index == len(self.files) - 1:
            while len(self.file_name_stack) > 0:
                self.image_stack.pop(0)

                # 20190107新增
                self.file_name_stack_temp = self.file_name_stack.pop(0)
                self.new_file_name_stack_temp = self.new_file_name_stack.pop(0)

                # 2019/02/11
                str_list = self.Analysis_re(self.file_name_stack_temp)

                # 2019/02/11
                if self.var_stack.pop(0) == 0:
                    shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_del,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))

                else:
                    shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp),os.path.join(self.file_dir_change,'{0}{1}{2}'.format(str_list[0], self.new_file_name_stack_temp,str_list[2])))

            self.close()
        else:
            self.index += 1
            self.file_name = self.files[self.index]

            self.image = cv_imread(os.path.join(self.file_dir, self.file_name))
            self.lbl_pic.setPixmap(QPixmap.fromImage(self.QIM_From_Numpy(self.image)))

            # 2019/02/11
            # self.lbl_label.setText(os.path.splitext(self.file_name)[0].split('@')[1])
            str_list = self.Analysis_re(self.file_name)
            self.lbl_label.setText(str_list[1] if self.files_temp[self.index] == self.file_name else self.files_temp[self.index])

            self.lbl_num_act.setText('当前张数：%s' % str(self.index + 1))


    def pbt_back_click(self):
        if len(self.file_name_stack) > 0:
            self.file_name = self.file_name_stack.pop()
            self.new_file_name = self.new_file_name_stack.pop()
            self.image = self.image_stack.pop()
            self.var_stack.pop()

            self.lbl_pic.setPixmap(QPixmap.fromImage(self.QIM_From_Numpy(self.image)))
            self.lbl_label.setText(self.new_file_name)

            self.index = max(0,self.index-1)
            self.lbl_num_act.setText('当前张数：%s' % str(self.index + 1))


    def pbt_next_click(self):
        if len(self.file_name_stack) >= self.stack_len:
            self.image_stack.pop(0)
            # 20190107新增
            self.file_name_stack_temp = self.file_name_stack.pop(0)
            self.new_file_name_stack_temp = self.new_file_name_stack.pop(0)


            #2019/02/11
            str_list=self.Analysis_re(self.file_name_stack_temp)

           #2019/02/11
            if self.var_stack.pop(0) == 0:
                shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_del,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))

            else:
                shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_change,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))

        self.file_name_stack.append(self.file_name)
        self.new_file_name_stack.append(self.lbl_label.text())
        self.image_stack.append(self.image)
        self.var_stack.append(1)

        self.files_temp[self.index] = self.lbl_label.text()

        if self.index == len(self.files)-1:
            while len(self.file_name_stack) > 0:
                self.image_stack.pop(0)
                # 20190107新增
                self.file_name_stack_temp = self.file_name_stack.pop(0)
                self.new_file_name_stack_temp = self.new_file_name_stack.pop(0)

                # 2019/02/11
                str_list = self.Analysis_re(self.file_name_stack_temp)

                # 2019/02/11
                if self.var_stack.pop(0) == 0:
                    shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp), os.path.join(self.file_dir_del,'{0}{1}{2}'.format(str_list[0],self.new_file_name_stack_temp,str_list[2])))

                else:
                    shutil.move(os.path.join(self.file_dir, self.file_name_stack_temp),os.path.join(self.file_dir_change,'{0}{1}{2}'.format(str_list[0], self.new_file_name_stack_temp,str_list[2])))

            self.close()
        else:
            self.index += 1
            self.file_name = self.files[self.index]
            self.image = cv_imread(os.path.join(self.file_dir, self.file_name))
            self.lbl_pic.setPixmap(QPixmap.fromImage(self.QIM_From_Numpy(self.image)))

            #2019/02/11
            # self.lbl_label.setText(os.path.splitext(self.file_name)[0].split('@')[1])
            str_list = self.Analysis_re(self.file_name)
            a=self.files_temp[self.index]
            self.lbl_label.setText(str_list[1] if self.files_temp[self.index] == self.file_name else self.files_temp[self.index])


            self.lbl_num_act.setText('当前张数：%s' % str(self.index + 1))


    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_PageDown):
            self.pbt_next_click()
        if (event.key() == QtCore.Qt.Key_Escape):
            self.pbt_del_click()
        if (event.key() == QtCore.Qt.Key_PageUp):
            self.pbt_back_click()


    def closeEvent(self, event):
        QtWidgets.QMessageBox.about(self,'提示','标注辛苦了......')


import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ID_CARD_UI()
    window.setFocus()
    window.show()
    sys.exit(app.exec_())