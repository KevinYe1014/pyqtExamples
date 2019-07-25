import os, re, sys, shutil
import numpy as np, pandas as pd
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from server1 import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import ServerUtils1



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

        self.pbt_cls.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_cls.clicked.connect(self.pbt_cls_click)

    def pbt_selectdata_click(self):
        '''选取csv文件'''
        filename, filetype = QFileDialog.getOpenFileName(self, '选取文件', './', 'CsvFile(*.csv)')
        self.datalist = []
        self.statelist = []
        if filename != '' and filename != None:
            self.lineEdit_csv.setText(filename)
            self.sourceData = pd.read_csv(filename)
            self.sourceData.columns.values[0] = 'flr'
            data = list(self.sourceData.iloc[:, 0])
            self.datalist.append(np.array(data))
            self.statelist.append('origin data')
            ServerUtils1.PlotAndSave(self.datalist, self.statelist)
            self.image = ServerUtils1.cv_imread()
            self.lbl_new.setPixmap(QPixmap.fromImage(ServerUtils1.QIM_From_Numpy(self.image)))
            self.flag = True

    def AnalysisState(self, isAoTu, isSlope, isSecondCurve):
        '''解析状态'''
        str = 'Peak-' if isAoTu else ''
        str += 'Slope-' if isSlope else ''
        str += '2ndCurve-' if isSecondCurve else ''
        if '-' in str:
            str = str[: -1]
        return str




    def pbt_analysis_click(self):
        if self.flag == True:
            isAoTu, isSlope, isSecondCurve = self.checkBox_point.isChecked(), self.checkBox_slope.isChecked(), self.checkBox_curve.isChecked()
            count = self.sourceData.shape[0]
            data = list(self.sourceData.iloc[:, 0])
            self.inten = ServerUtils1.program(data, count, isAoTu, isSlope, isSecondCurve)
            # self.inten = pd.Series(self.inten)
            data = self.inten
            self.datalist.append(np.array(data))
            str = self.AnalysisState(isAoTu, isSlope, isSecondCurve)
            if str not in self.statelist:
                self.statelist.append(str)
                ServerUtils1.PlotAndSave(self.datalist, self.statelist)
                self.newimage = ServerUtils1.cv_imread()
                self.lbl_new.setPixmap(QPixmap.fromImage(ServerUtils1.QIM_From_Numpy(self.newimage)))

    def pbt_cls_click(self):
        '''清屏按钮触发事件'''
        if self.flag == True:
            self.datalist = self.datalist[: 1]
            self.statelist = self.statelist[: 1]
            ServerUtils1.PlotAndSave(self.datalist, self.statelist)
            self.newimage = ServerUtils1.cv_imread()
            self.lbl_new.setPixmap(QPixmap.fromImage(ServerUtils1.QIM_From_Numpy(self.newimage)))







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