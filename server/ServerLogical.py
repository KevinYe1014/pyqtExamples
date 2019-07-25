import os, re, sys, shutil
import numpy as np, pandas as pd
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from server import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import ServerUtils



class ServerMain(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(ServerMain,self).__init__()
        self.setupUi(self)
        self.all_widget_init()
        self.flag = False


    def all_widget_init(self):
        '''控件初始化'''
        self.pbt_selectdata.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_selectdata.clicked.connect(self.pbt_selectdata_click)

        self.pbt_analysis.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_analysis.clicked.connect(self.pbt_analysis_click)


    def pbt_selectdata_click(self):
        '''选取csv文件'''
        filename, filetype = QFileDialog.getOpenFileName(self, '选取文件', './', 'CsvFile(*.csv)')
        if filename != '' and filename != None:
            self.lineEdit_csv.setText(filename)
            self.sourceData = pd.read_csv(filename)
            self.sourceData.columns.values[0] = 'flr'
            data = list(self.sourceData.iloc[:, 0])
            ServerUtils.PlotAndSave(data, 'Original Data Picture', 'source')
            self.image = ServerUtils.cv_imread('./{}.jpg'.format('source'))
            self.lbl_ori.setPixmap(QPixmap.fromImage(ServerUtils.QIM_From_Numpy(self.image)))
            self.flag = True



    def pbt_analysis_click(self):
        if self.flag == True:
            isAoTu, isSlope, isSecondCurve = self.checkBox_point.isChecked(), self.checkBox_slope.isChecked(), self.checkBox_curve.isChecked()
            count = self.sourceData.shape[0]
            data = list(self.sourceData.iloc[:, 0])
            self.inten = ServerUtils.program(data, count, isAoTu, isSlope, isSecondCurve)
            # self.inten = pd.Series(self.inten)
            data = self.inten
            ServerUtils.PlotAndSave(data, 'Fitting Data Picture', 'fitting')
            self.newimage = ServerUtils.cv_imread('./{}.jpg'.format('fitting'))
            self.lbl_new.setPixmap(QPixmap.fromImage(ServerUtils.QIM_From_Numpy(self.newimage)))

    def closeEvent(self, event):
        '''关闭工具'''
        QtWidgets.QMessageBox.about(self, '提示', '分析结束 ... ')

import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ServerMain()
    window.setFocus()
    window.show()
    sys.exit(app.exec_())