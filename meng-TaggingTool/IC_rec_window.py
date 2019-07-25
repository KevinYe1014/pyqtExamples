# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IC_rec_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(565, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_pic = QtWidgets.QLabel(self.centralwidget)
        self.lbl_pic.setMinimumSize(QtCore.QSize(350, 400))
        self.lbl_pic.setObjectName("lbl_pic")
        self.gridLayout.addWidget(self.lbl_pic, 0, 0, 1, 1)
        self.lbl_label = QtWidgets.QLineEdit(self.centralwidget)
        self.lbl_label.setEnabled(True)
        self.lbl_label.setMinimumSize(QtCore.QSize(350, 40))
        # font = QtGui.QFont()
        # font.setFamily("Roman times")
        # font.setPointSize(22)
        # font.setBold(True)
        # font.setWeight(50)
        # self.lbl_label.setFont(font)
        self.lbl_label.setFont(QFont("Roman times", 22, QFont.Bold))
        self.lbl_label.setEnabled(True)

        self.lbl_label.setObjectName("lbl_label")
        self.gridLayout.addWidget(self.lbl_label, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.lbl_num_act = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.lbl_num_act.setFont(font)
        # self.lbl_num_act.setFont(QFont("Roman times", 10, QFont.Bold))
        # self.lbl_num_act.setEnabled(True)

        self.lbl_num_act.setObjectName("lbl_num_act")
        self.horizontalLayout_2.addWidget(self.lbl_num_act)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.lbl_num_sum = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.lbl_num_sum.setFont(font)
        # self.lbl_num_sum.setFont(QFont("Roman times", 10, QFont.Bold))
        # self.lbl_num_sum.setEnabled(True)

        self.lbl_num_sum.setObjectName("lbl_num_sum")
        self.horizontalLayout_2.addWidget(self.lbl_num_sum)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.pbt_back = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_back.setObjectName("pbt_back")
        self.horizontalLayout.addWidget(self.pbt_back)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.pbt_del = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_del.setObjectName("pbt_del")
        self.horizontalLayout.addWidget(self.pbt_del)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self.pbt_next = QtWidgets.QPushButton(self.centralwidget)
        self.pbt_next.setObjectName("pbt_next")
        self.horizontalLayout.addWidget(self.pbt_next)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 565, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "screen_image"))
        self.lbl_pic.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_num_act.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_num_sum.setText(_translate("MainWindow", "TextLabel"))
        self.pbt_back.setText(_translate("MainWindow", "back"))
        self.pbt_del.setText(_translate("MainWindow", "del"))
        self.pbt_next.setText(_translate("MainWindow", "next"))

import sys
from PyQt5.QtWidgets import  QApplication, QMainWindow
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())