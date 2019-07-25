# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TaggingTool.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(928, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbt_selectDirectory = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_selectDirectory.setGeometry(QtCore.QRect(40, 20, 131, 31))
        self.pbt_selectDirectory.setObjectName("pbt_selectDirectory")
        self.lineEdit_Directory = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Directory.setGeometry(QtCore.QRect(190, 20, 581, 31))
        self.lineEdit_Directory.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lineEdit_Directory.setObjectName("lineEdit_Directory")
        self.lbl_picOriginName = QtWidgets.QLabel(self.centralwidget)
        self.lbl_picOriginName.setGeometry(QtCore.QRect(70, 130, 321, 16))
        self.lbl_picOriginName.setText("")
        self.lbl_picOriginName.setObjectName("lbl_picOriginName")
        self.lbl_pic = QtWidgets.QLabel(self.centralwidget)
        self.lbl_pic.setGeometry(QtCore.QRect(70, 160, 481, 311))
        self.lbl_pic.setText("")
        self.lbl_pic.setObjectName("lbl_pic")
        self.textEdit_introduction = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_introduction.setGeometry(QtCore.QRect(600, 160, 231, 341))
        self.textEdit_introduction.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEdit_introduction.setObjectName("textEdit_introduction")
        self.pbt_back = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_back.setGeometry(QtCore.QRect(70, 560, 131, 31))
        self.pbt_back.setObjectName("pbt_back")
        self.pbt_next = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_next.setGeometry(QtCore.QRect(450, 560, 131, 31))
        self.pbt_next.setObjectName("pbt_next")
        self.lbl_introduction = QtWidgets.QLabel(self.centralwidget)
        self.lbl_introduction.setGeometry(QtCore.QRect(610, 120, 71, 20))
        self.lbl_introduction.setObjectName("lbl_introduction")
        self.lbl_currentCount = QtWidgets.QLabel(self.centralwidget)
        self.lbl_currentCount.setGeometry(QtCore.QRect(70, 510, 131, 21))
        self.lbl_currentCount.setText("")
        self.lbl_currentCount.setObjectName("lbl_currentCount")
        self.lbl_counts = QtWidgets.QLabel(self.centralwidget)
        self.lbl_counts.setGeometry(QtCore.QRect(280, 510, 141, 21))
        self.lbl_counts.setText("")
        self.lbl_counts.setObjectName("lbl_counts")
        self.pbt_start = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_start.setGeometry(QtCore.QRect(40, 70, 131, 31))
        self.pbt_start.setObjectName("pbt_start")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 928, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "标注工具"))
        self.pbt_selectDirectory.setText(_translate("MainWindow", "选择标注文件夹"))
        self.pbt_back.setText(_translate("MainWindow", "上一张"))
        self.pbt_next.setText(_translate("MainWindow", "下一张"))
        self.lbl_introduction.setText(_translate("MainWindow", "标注说明："))
        self.pbt_start.setText(_translate("MainWindow", "开始标注"))

