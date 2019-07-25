import os, re, sys, shutil
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from TaggingTool import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import DB, TaggingUtils


class taggingToolMain(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(taggingToolMain,self).__init__()
        self.setupUi(self)
        self.all_widget_init()
        self.AnalysisIntroduction()
        self.CreateTargetDiretory()


    def all_widget_init(self):
        '''控件初始化'''
        self.pbt_selectDirectory.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_selectDirectory.clicked.connect(self.pbt_selectDirectory_click)

        self.pbt_next.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_next.clicked.connect(self.pbt_next_click)

        self.pbt_back.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_back.clicked.connect(self.pbt_back_click)

        self.pbt_start.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pbt_start.clicked.connect(self.pbt_start_click)

        self.flag = False
        self.directory = ''
        self.DBSaveLength = 5


    def AnalysisIntroduction(self):
        '''写说明文档'''
        self.refileNameList, self.classificationLabels = TaggingUtils.AnalysisConfig('123456')
        self.classificationLabels = ['uncertain'] + self.classificationLabels
        self.classificationSum = len(self.classificationLabels)
        zipIndex =[i for i in range(self.classificationSum)]
        self.label_to_int = dict(zip(self.classificationLabels, zipIndex))
        self.int_to_label = dict(zip(zipIndex, self.classificationLabels))
        text = '   根据配置文件{0}里面的参数{1}，将图片分为{2}类。现将标注时的按键对应关系说明如下：' \
               '\n'.format((TaggingUtils.config_dir), 'ClassificationLabel', str(self.classificationSum))
        for i in range(self.classificationSum):
            text += '（{0}）如果分为：{1}， 请按：{2}\n'.format(str(i), self.classificationLabels[i], str(i))
        self.textEdit_introduction.setText(text)


    def pbt_selectDirectory_click(self):
        directory = QFileDialog.getExistingDirectory(self, "选取文件夹",'./')
        self.lineEdit_Directory.setText(directory)
        self.directory = self.lineEdit_Directory.text()
        self.DBUpdateAndMoveFiles(False)
        self.DB_Create()
        self.flag = False


    def CreateTargetDiretory(self):
        '''创建文件夹'''
        self.moveTargetBaseDir = './'
        for i in range(self.classificationSum):
            moveTargetDir = os.path.join(self.moveTargetBaseDir, self.int_to_label[i])
            if not os.path.exists(moveTargetDir):
                os.makedirs(moveTargetDir)


    def pbt_start_click(self):
        '''开始标注触发事件'''
        if self.directory != '':
            self.flag = True
            self.readFiles()


    def DB_Create(self):
        '''创建数据库表'''
        self.conn = DB.get_conn(DB.TaggingToolInfoDB)
        DB.drop_table(self.conn, DB.TaggingDetailTable)
        DB.CreateTaggingDetailTable(self.conn)
        DB.drop_table(self.conn, DB.TaggingIndexTable)
        DB.CreateTaggingIndexTable(self.conn)


    def readFiles(self):
        '''读取文件'''
        self.fileNameList = []
        self.index = 0
        self.files = TaggingUtils.read_all_files(self.directory)
        if self.files is None or len(self.files) == 0:
            QtWidgets.QMessageBox.about(self, '提示', '该文件夹没有目标文件！')
            # sys.exit(0)
        else:
            self.CountSum = len(self.files)
            self.lbl_currentCount.setText('当前张数：{}'.format(str(self.index + 1)))
            self.lbl_counts.setText('总张数：{}'.format(str(self.CountSum)))

            self.fileName = self.files[self.index]
            self.fileNameList.append(self.fileName)
            self.lbl_picOriginName.setText(self.fileName)
            self.image = TaggingUtils.cv_imread(os.path.join(self.directory, self.fileName))
            self.lbl_pic.setPixmap(QPixmap.fromImage(TaggingUtils.QIM_From_Numpy(self.image)))


    def pbt_next_click(self):
        '''next键触发事件'''
        if self.flag == True:
            self.index += 1
            if self.index == len(self.fileNameList) - 1:
                self.ShowNextPic()
            elif self.index < len(self.fileNameList) - 1:
                fetchone_sql = '''SELECT * FROM TaggingDetail WHERE id = ?'''
                data = self.index
                result = DB.fetchone(self.conn, fetchone_sql, data)
                self.backNewFileName = result[0][3]
                self.ShowNextPic()
            else:
                QtWidgets.QMessageBox.about(self, '提示', '请选择类别！')
                self.index -= 1


    def pbt_back_click(self):
        '''back按键触发事件'''
        # 读取数据库
        if self.flag == True:
            if self.index > 0:
                fetchall_sql_minid = '''SELECT min(id) FROM TaggingDetail '''
                result = DB.fetchall(self.conn, fetchall_sql_minid)
                if self.index > result[0][0]:
                    self.index -= 1
                    fetchone_sql = '''SELECT * FROM TaggingDetail WHERE id = ?'''
                    data = self.index
                    result = DB.fetchone(self.conn, fetchone_sql, data)
                    self.backNewFileName = result[0][3]
                    self.ShowNextPic()


    def ShowNextPic(self):
        '''显示下一张图片'''
        self.lbl_currentCount.setText('当前张数：{}'.format(str(self.index + 1)))
        self.fileName = self.files[self.index]
        if self.index == len(self.fileNameList) -1:
            self.lbl_picOriginName.setText(self.fileName)
        else:
            self.lbl_picOriginName.setText(self.backNewFileName)
        self.image = TaggingUtils.cv_imread(os.path.join(self.directory, self.fileName))
        self.lbl_pic.setPixmap(QPixmap.fromImage(TaggingUtils.QIM_From_Numpy(self.image)))

    def DBUpdateAndMoveFiles(self, IsOne):
        '''剪切文件和更新数据库，分一个和所有两种情况'''
        if IsOne:
            # move file
            index = self.index - self.DBSaveLength - 1
            fetchone_sql = '''SELECT * FROM TaggingDetail WHERE id = ?'''
            result = DB.fetchone(self.conn, fetchone_sql, index)
            directory = result[0][1]
            oldFileName = result[0][2]
            newFileName = result[0][3]
            classfication = self.int_to_label[result[0][4]]
            oldName = os.path.join(directory, oldFileName)
            newName = os.path.join(self.moveTargetBaseDir,
                                   os.path.join(classfication, newFileName))
            TaggingUtils.MoveAndRename(oldName, newName)
            # update DB
            delete_sql = '''DELETE FROM TaggingDetail WHERE id = ?'''
            DB.delete(self.conn, delete_sql, [(index, )])
        else:
            # move all files
            try:
                fetchone_sql = '''SELECT * FROM TaggingDetail '''
                result = DB.fetchall(self.conn, fetchone_sql)
                for i in range(len(result)):
                    directory = result[i][1]
                    oldFileName = result[i][2]
                    newFileName = result[i][3]
                    classfication = self.int_to_label[result[i][4]]
                    oldName = os.path.join(directory, oldFileName)
                    newName = os.path.join(self.moveTargetBaseDir,
                                           os.path.join(classfication, newFileName))
                    TaggingUtils.MoveAndRename(oldName, newName)
                # drop DB 不用删除
                DB.drop_table(self.conn, DB.TaggingIndexTable)
            except:
                pass


    def ChooseAimFileDir(self, numKey):
        '''按键1、2、3触发的事件'''
        if self.flag == True:
            label = self.int_to_label[numKey]
            filePrefix = os.path.splitext(self.fileName)[0]
            filePostfix = os.path.splitext(self.fileName)[1]
            newfileName = '{}_{}{}'.format(filePrefix, label, filePostfix)
            if self.index == len(self.fileNameList) - 1:
                if numKey < self.classificationSum :
                    insert_sql = '''INSERT INTO TaggingDetail VALUES (?, ?, ?, ?, ?)'''
                    data = [(self.index, self.directory, self.fileName, newfileName, numKey)]
                    DB.insert(self.conn, insert_sql, data)

                    self.index += 1
                    if self.index < self.CountSum:
                        self.fileNameList.append(self.files[self.index])
                        self.ShowNextPic()
                        # 数据库更新及剪切文件，单条
                        if self.index > self.DBSaveLength:
                            self.DBUpdateAndMoveFiles(True)
                    else:
                        self.DBUpdateAndMoveFiles(False)
                        QtWidgets.QMessageBox.about(self, '提示', '该文件夹标注完成，请切换文件夹！')

            else:
                if numKey < self.classificationSum:
                    update_sql = '''UPDATE TaggingDetail SET newfilename = ?,classification= ? WHERE id = ?'''
                    data = [(newfileName, numKey, self.index)]
                    DB.update(self.conn, update_sql, data)
                    self.index += 1
                    self.ShowNextPic()


    def keyPressEvent(self, event):
        # region 按键事件
        if (event.key() == QtCore.Qt.Key_0):
            self.ChooseAimFileDir(0)
        if (event.key() == QtCore.Qt.Key_1):
            self.ChooseAimFileDir(1)
        if (event.key() == QtCore.Qt.Key_2):
            self.ChooseAimFileDir(2)
        if (event.key() == QtCore.Qt.Key_3):
            self.ChooseAimFileDir(3)
        if (event.key() == QtCore.Qt.Key_4):
            self.ChooseAimFileDir(4)
        if (event.key() == QtCore.Qt.Key_5):
            self.ChooseAimFileDir(5)
        if (event.key() == QtCore.Qt.Key_6):
            self.ChooseAimFileDir(6)
        if (event.key() == QtCore.Qt.Key_7):
            self.ChooseAimFileDir(7)
        if (event.key() == QtCore.Qt.Key_8):
            self.ChooseAimFileDir(8)
        if (event.key() == QtCore.Qt.Key_9):
            self.ChooseAimFileDir(9)
        #endregion
        # 左右键控制上一张和下一张
        if (event.key() == QtCore.Qt.Key_Left):
            self.pbt_back_click()
        if (event.key() == QtCore.Qt.Key_Right):
            self.pbt_next_click()


    def closeEvent(self, event):
        '''关闭工具'''
        self.DBUpdateAndMoveFiles(False)
        QtWidgets.QMessageBox.about(self, '提示', '标注辛苦了 ... ')


import sys
from PyQt5.QtWidgets import QApplication
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = taggingToolMain()
    window.setFocus()
    window.show()
    sys.exit(app.exec_())