import configparser, cv2, os
import numpy as np
from PyQt5.QtGui import *
import shutil, os

# region 读写图像文件
def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), 1)
    size=(600,450)
    cv_img=cv2.resize(cv_img,size,interpolation=cv2.INTER_AREA)
    return cv_img


def cv_imwrite(filename, src):
    cv2.imencode('.jpg', src)[1].tofile(filename)


def read_all_files(file_dir):
    files = os.listdir(file_dir)
    files = [file for file in files if str(file).lower().endswith(('.jpg', '.png'))]
    return files


def QIM_From_Numpy(base_img):
    image_height, image_width, image_depth = base_img.shape  # 获取图像的高，宽以及深度。
    QIm = cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
    QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                 image_width * image_depth,
                 QImage.Format_RGB888)
    return QIm


# endregion


# 读取配置参数
config_dir = 'config.ini'
cf = configparser.ConfigParser()
cf.read(config_dir, encoding='utf-8')
re_ori = cf.get("Re-IDCARD", "_re")
classificationLabel = cf.get('ClassificationLabel', 'CL')


def AnalysisConfig(fileName, re_ori=re_ori, classificationLabel=classificationLabel):
    '''解析配置参数'''
    aimFileName = str(eval(re_ori.replace('str', repr(fileName))))
    fileNameList = []
    fileNameList.append(fileName[0: fileName.index(aimFileName)])
    fileNameList.append(aimFileName)
    fileNameList.append(fileName[fileName.index(aimFileName) + len(aimFileName):])
    classificationLabels = str(classificationLabel).split(',')
    return fileNameList, classificationLabels


def MoveAndRename(src, dst):
    '''文件剪切和重命名'''
    dstDir = os.path.abspath(os.path.join(dst, '..'))
    srcDir = os.path.abspath(os.path.join(src, '..'))
    if dstDir != srcDir:
        srcfileName = os.path.basename(src)
        shutil.move(src, dstDir)
        dstOldName = os.path.join(dstDir, srcfileName)
        os.rename(dstOldName, dst)
    else:
        os.rename(src, dst)

