# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(691, 744)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbt_selectdata = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_selectdata.setGeometry(QtCore.QRect(30, 20, 101, 31))
        self.pbt_selectdata.setObjectName("pbt_selectdata")
        self.lineEdit_csv = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_csv.setGeometry(QtCore.QRect(160, 20, 421, 31))
        self.lineEdit_csv.setObjectName("lineEdit_csv")
        self.lbl_ori = QtWidgets.QLabel(self.centralwidget)
        self.lbl_ori.setGeometry(QtCore.QRect(30, 60, 551, 251))
        self.lbl_ori.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_ori.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_ori.setObjectName("lbl_ori")
        self.lbl_new = QtWidgets.QLabel(self.centralwidget)
        self.lbl_new.setGeometry(QtCore.QRect(30, 420, 551, 251))
        self.lbl_new.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_new.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_new.setObjectName("lbl_new")
        self.pbt_analysis = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_analysis.setGeometry(QtCore.QRect(30, 370, 101, 31))
        self.pbt_analysis.setObjectName("pbt_analysis")
        self.checkBox_point = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_point.setGeometry(QtCore.QRect(50, 330, 91, 31))
        self.checkBox_point.setChecked(True)
        self.checkBox_point.setObjectName("checkBox_point")
        self.checkBox_slope = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_slope.setGeometry(QtCore.QRect(230, 330, 91, 31))
        self.checkBox_slope.setChecked(True)
        self.checkBox_slope.setObjectName("checkBox_slope")
        self.checkBox_curve = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_curve.setGeometry(QtCore.QRect(420, 330, 91, 31))
        self.checkBox_curve.setChecked(True)
        self.checkBox_curve.setObjectName("checkBox_curve")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 691, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Server Data Processing"))
        self.pbt_selectdata.setText(_translate("MainWindow", "选择数据文件"))
        self.lbl_ori.setText(_translate("MainWindow", "原始数据图像"))
        self.lbl_new.setText(_translate("MainWindow", "修正数据图像"))
        self.pbt_analysis.setText(_translate("MainWindow", "分析"))
        self.checkBox_point.setText(_translate("MainWindow", "突变点修正"))
        self.checkBox_slope.setText(_translate("MainWindow", "斜率修正"))
        self.checkBox_curve.setText(_translate("MainWindow", "二次曲线修正"))

