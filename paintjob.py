import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from pylab import *
# coding:utf-8
mpl.rcParams['font.sans-serif'] = ['SimHei']

def painting(msg,datastream):#参数：图形类别，数据源
    data=datastream
    #绘制对应图形
    if msg == "价格条形图":
        # 将每平米价钱转化为数值类型
        # 经过实践，只有下面的方法才能将object类型转化为int类型
        data2 = data[['unit_price', 'loc']]
        data2['unit_price'] = data2['unit_price'].astype(str).astype(int)
        data2_group = data2.groupby(['loc'])
        mean = data2_group.aggregate({'unit_price': np.mean})
        std = data2_group.aggregate({'unit_price': np.std})
        mean.plot(kind='bar', yerr=std, color='red', title='北京各区每平米房价情况', rot=45)
        plt.show()

    elif msg=='价格箱线图':
        #同上
        data2 = data[['unit_price', 'loc']]
        data2['unit_price'] = data2['unit_price'].astype(str).astype(int)
        data2.boxplot(by='loc', figsize=(10, 30))
        plt.title("北京各区每平米房价箱线图")
        plt.show()

    elif msg=='饼图':
        data_change=data;
        for j in range(len(data_change)):
            if (data_change['unit_price'].values[j] <50000):
                data_change['unit_price'].values[j] = '5万元以内';
            elif (data_change['unit_price'].values[j] > 100000):
                data_change['unit_price'].values[j] = '10万元以上';
            else:
                data_change['unit_price'].values[j] = '5-10万元';
        #在一块画布上画出价格与年代饼图
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(2, 1, 1)
        year = data_change.groupby(['build_time']).size()
        # year.column=['20年以上','5-20年内','5年内']
        year.plot(kind='pie', figsize=(10, 10), shadow=True, startangle=30, autopct='%1.1f%%', title='建造时间（距今）', ax=ax1)
        ax1.set_ylabel('相隔年数')
        ax2 = fig.add_subplot(2, 1, 2)
        price = data_change.groupby(['unit_price']).size()
        price.plot(kind='pie', figsize=(10, 10), shadow=True, startangle=30, autopct='%1.1f%%', title='每平米价格', ax=ax2)
        ax2.set_ylabel('价格(单位：万元)')
        plt.show()

    elif msg=='年代堆积柱状图':
        data2 = data[['unit_price', 'loc']]
        for j in range(len(data2)):
            if (data2['unit_price'].values[j] <50000):
                data2['unit_price'].values[j] = '5万元以内';
            elif (data2['unit_price'].values[j] > 100000):
                data2['unit_price'].values[j] = '10万元以上';
            else:
                data2['unit_price'].values[j] = '5-10万元';
        data2_group = data2.groupby(['loc'])


