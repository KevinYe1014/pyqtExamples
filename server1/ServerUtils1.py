import numpy as np
import cv2, os, shutil
from PyQt5.QtGui import *
import pandas as pd
import matplotlib.pyplot as plt



minCycleCount = 4
isMeltingStage = True

# region 读写图像文件及画图

def cv_imread(file_path = './{}.jpg'.format('source')):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), 1)
    size=(801,461)
    cv_img=cv2.resize(cv_img,size,interpolation=cv2.INTER_AREA)
    return cv_img


def cv_imwrite(filename, src):
    cv2.imencode('.jpg', src)[1].tofile(filename)

def QIM_From_Numpy(base_img):
    image_height, image_width, image_depth = base_img.shape  # 获取图像的高，宽以及深度。
    QIm = cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)  # opencv读图片是BGR，qt显示要RGB，所以需要转换一下
    QIm = QImage(QIm.data, image_width, image_height,  # 创建QImage格式的图像，并读入图像信息
                 image_width * image_depth,
                 QImage.Format_RGB888)
    return QIm


def PlotAndSave(datalist, statelist):
    '''画图和保存图'''
    plotCount = len(statelist)
    p = []
    for i in range(plotCount):
        pi, = plt.plot(datalist[i])  #'-o'
        p.append(pi)
    plt.legend(p, statelist, loc = 2 ,fontsize = 8)
    plt.title('Data Analysis Picture')
    plt.xlabel('Temperature')
    plt.ylabel('Rn')
    fileFullName = './{}.jpg'.format('source')
    if os.path.exists(fileFullName) and os.path.isfile(fileFullName):
        os.remove(fileFullName)
    plt.savefig(fileFullName)
    plt.close()

# endregion


# region 具体处理函数

def program(inten, count, isAoTu, isSlope, isSecondCurve):
    '''C#中program中的函数'''
    items = []
    for i in range(count):
        items.append(inten[i])
        if len(items) >= minCycleCount:
            for j in range(1 if isMeltingStage else 2):
                items_temp = items[len(items) - minCycleCount: ]
                smooth(items_temp, isAoTu, isSlope, isSecondCurve)

                for t in range(len(items_temp)):
                    items[len(items) - minCycleCount + t] = items_temp[t]

                if len(items) >= minCycleCount + 1:
                    items_temp1 = items[len(items) - minCycleCount - 1: ]
                    smooth(items_temp1, isAoTu, isSlope, isSecondCurve)

                    for t in range(len(items_temp1)):
                        items[len(items) - minCycleCount - 1 + t] = items_temp1[t]
    return  items

def smooth(flrs, isAoTu, isSlope, isSecondCurve):
    '''以前委托的地方'''
    intensities = []
    for i in range(len(flrs)):
        intensities.append(flrs[i])
    Fitting(intensities, isAoTu, isSlope, isSecondCurve)
    for i in range(len(flrs)):
        flrs[i] = intensities[i]

def Fitting(yValues, isAoTu, isSlope, isSecondCurve):
    '''下面函数集合拟合'''
    SmoothCurve(yValues)
    for i in range(2):
        if isAoTu:
            SmoothPeak(yValues)
        if isSlope:
            SmoothSlope(yValues)
        if isSecondCurve:
            SmoothCurve(yValues)
    # SmoothCurve(yValues)



def SecondCurveFitting(ptx, pty, beginIndex = 0, count = 4):
    '''二次曲线拟合'''
    if len(ptx) != len(pty):
        raise Exception('ptx.Length != pty.Length')
    fX = 0
    fXX = 0
    fXXX = 0
    fY = 0
    fXY = 0
    fXXY = 0
    fXXXX = 0
    if count < 4:
        count = len(ptx) - beginIndex

    for i in range(count):
        x = ptx[beginIndex + i];
        y = pty[beginIndex + i];
        fX += x
        fY += y
        fXX += x * x
        fXY += x * y
        fXXX += x * x * x
        fXXY += x * x * y
        fXXXX += x * x * x * x
    matrix = np.zeros(9)
    matrix[0] = count
    matrix[1] = fX
    matrix[2] = fXX
    matrix[3] = fX
    matrix[4] = fXX
    matrix[5] = fXXX
    matrix[6] = fXX
    matrix[7] = fXXX
    matrix[8] = fXXXX

    fD = HangLieShi(matrix)

    if (fD < 0.01):
        return None

    matrix[0] = fY
    matrix[1] = fX
    matrix[2] = fXX
    matrix[3] = fXY
    matrix[4] = fXX
    matrix[5] = fXXX
    matrix[6] = fXXY
    matrix[7] = fXXX
    matrix[8] = fXXXX
    fDX = HangLieShi(matrix)

    matrix[0] = count
    matrix[1] = fY
    matrix[2] = fXX
    matrix[3] = fX
    matrix[4] = fXY
    matrix[5] = fXXX
    matrix[6] = fXX
    matrix[7] = fXXY
    matrix[8] = fXXXX
    fDY = HangLieShi(matrix)

    matrix[0] = count
    matrix[1] = fX
    matrix[2] = fY
    matrix[3] = fX
    matrix[4] = fXX
    matrix[5] = fXY
    matrix[6] = fXX
    matrix[7] = fXXX
    matrix[8] = fXXY
    fDZ = HangLieShi(matrix)

    for i in range(count):
        x = ptx[beginIndex + i]
        pty[beginIndex + i] = (fDX + fDY * x + fDZ * x * x) / fD
    # 返回待定

def HangLieShi(matrix):
    '''行列式'''
    fResult = matrix[0] * matrix[4] * matrix[8] +  \
              matrix[1] * matrix[5] * matrix[6] + \
              matrix[2] * matrix[3] * matrix[7] - \
              matrix[2] * matrix[4] * matrix[6] - \
              matrix[5] * matrix[7] * matrix[0] - \
              matrix[1] * matrix[3] * matrix[8]
    return fResult








def SmoothPeak(yValues):
    '''突变点拟合'''
    if len(yValues) < 3:
        return
    y1 = 0
    y2 = yValues[0]
    y3 = yValues[1]
    for x in range(2,len(yValues)):
        y1 = y2
        y2 = y3
        y3 = yValues[x]
        if ((y2 >= y1 and y2 >= y3) or (y2 <= y1 and y2 <= y3)):
            y2 = (y1 + y3) / 2
            yValues[x - 1] = y2

def SmoothSlope(yValues):
    '''斜率平滑'''
    pointCount = len(yValues)
    if pointCount < 4:
        return
    y = np.array([0, yValues[0], yValues[1], yValues[2]])
    dy = np.zeros(3)
    for i in range(3, pointCount):
        y[0] = y[1]
        y[1] = y[2]
        y[2] = y[3]
        y[3] = yValues[i]

        dy[0] = y[1] - y[0]
        dy[1] = y[2] - y[1]
        dy[2] = y[3] - y[2]
        if (dy[1] > dy[2] and dy[1] > dy[0]) or (dy[1] < dy[2] and dy[1] < dy[0]):
            y[2] = (y[1] + y[3]) / 2
            yValues[i - 1] = y[2]
        elif dy[1] > dy[0] * 3 / 2:
            y[1] = y[0] + (int)(dy[0] * 2.0 / 3.0 + dy[1] / 3.0)
            yValues[i - 2] = y[1]
        elif dy[2] > dy[1] * 3 / 2:
            y[2] = y[1] + (int)(dy[1] * 2.0 / 3.0 + dy[2] / 3.0)
            yValues[i - 1] = y[2]

def SmoothCurve(yValues):
    '''二次曲线拟合'''
    x = 0
    yValues2 = np.zeros(len(yValues) + 6)
    yValues2[0] = yValues2[1] = yValues2[2] = yValues[0]
    yValues2[len(yValues) + 3] = yValues2[len(yValues) + 4] = yValues2[len(yValues) + 5] = yValues[len(yValues) - 1]
    ArrayCopy(yValues, 0, yValues2, 3, len(yValues))
    ptx = [i + 1 for i in range(len(yValues2))]
    for i in range(len(yValues2) - 3):
        ptx[i] = 1
        ptx[i + 1] = 2
        ptx[i + 2] = 3
        ptx[i + 3] = 4
        SecondCurveFitting(ptx, yValues2, i)
    ArrayCopy(yValues2, 3, yValues, 0, len(yValues))

def ArrayCopy(yValues, sourceIndex, yValues2, destinationIndex, Length):
    '''深度复制'''
    for i in range(Length):
        yValues2[destinationIndex + i ] = yValues[sourceIndex + i]

# endregion