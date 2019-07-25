import pandas as pd
import matplotlib.pyplot as plt
import random




# directory = r'H:\code\age-gender-estimation-master\server\d.csv'
# directory1 = r'C:\Users\yelei\Desktop\d.csv'
# sourceData = pd.read_csv(directory1)
# sourceData.columns.values[0] = 'dudu'
# sourceData.plot()
# plt.title('Origin Data Picture')
# plt.xlabel('Temperature')
# plt.ylabel('Rn')
# plt.savefig('./source.jpg')
# plt.show()

def PlotAndSave(data, columsName, titleName, fileName):
    '''画图和保存图'''
    data.columns.values[0] = columsName
    plt.title(titleName)
    plt.xlabel('Temperature')
    plt.ylabel('Rn')
    plt.savefig('./{}.jpg'.format(fileName))


a = [random.randint(0, 100) for i in range(20)]
s = pd.Series(a)
s.plot()

plt.title('Origin Data Picture')
plt.xlabel('Temperature')
plt.ylabel('Rn')
plt.show()
