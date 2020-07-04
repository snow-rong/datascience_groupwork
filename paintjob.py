import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import collections
from pylab import *
# coding:utf-8
mpl.rcParams['font.sans-serif'] = ['SimHei']
#使plot绘图时能显示中文字符
#绘制的图像中，饼图与柱状堆积图能实现价格与建造时间的分区域内部对比
#条形图与箱线图仅提供总体比较

def painting(msg,datastream):#参数：图形类别，数据源
    data=datastream
    #绘制对应图形
    if msg == "价格条形图":
        # 将每平米价钱转化为数值类型
        # 经过实践，只有下面的方法才能将object类型转化为int类型(int32类型)
        data2 = data[['unit_price', 'loc']]
        data2['unit_price'] = data2['unit_price'].astype(str).astype(int)
        data2_group = data2.groupby(['loc'])
        #均值与标准差
        mean = data2_group.aggregate({'unit_price': np.mean})
        std = data2_group.aggregate({'unit_price': np.std})
        mean.plot(kind='bar', yerr=std, color='red', title='北京各区每平米房价情况', rot=45)
        plt.show()

    elif msg=='价格箱线图':
        #同上
        data2 = data[['unit_price', 'loc']]
        data2['unit_price'] = data2['unit_price'].astype(str).astype(int)
        #绘制箱线图
        data2.boxplot(by='loc', figsize=(10, 30))
        plt.title("北京各区每平米房价箱线图")
        plt.show()

    elif msg=='饼图':
        data_change=data;
        #设置每平米价钱对应类别
        for j in range(len(data_change)):
            if (int(data_change['unit_price'].values[j]) <30000):
                data_change['unit_price'].values[j] = '3万元以内';
            elif (int(data_change['unit_price'].values[j]) > 100000):
                data_change['unit_price'].values[j] = '10万元以上';
            else:
                data_change['unit_price'].values[j] = '3-10万元';
        #在一块画布上画出价格与年代饼图
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(1, 2, 1)
        year = data_change.groupby(['build_time']).size()
        # year.column=['20年以上','5-20年内','5年内']
        year.plot(kind='pie', figsize=(10, 10), shadow=True, startangle=30, autopct='%1.1f%%', title='建造时间（距今）', ax=ax1)
        ax1.set_ylabel('相隔年数')
        ax2 = fig.add_subplot(1, 2, 2)
        price = data_change.groupby(['unit_price']).size()
        price.plot(kind='pie', figsize=(10, 10), shadow=True, startangle=120, autopct='%1.1f%%', title='每平米价格', ax=ax2)
        ax2.set_ylabel('价格(单位：万元)')
        plt.show()

    elif msg=='柱状堆积图':
        # 在一块画布上画出价格与年代柱状堆积图
        #绘制年代柱状堆积图
        data_omega = data[['loc', 'build_time']]
        data1=data_omega.loc[data_omega['build_time'] == '5年内']
        data2=data_omega.loc[data_omega['build_time'] == '5-20年内']
        data3=data_omega.loc[data_omega['build_time'] == '20年以上']

        data_count1 = collections.Counter(data1['loc'])
        data_count2 = collections.Counter(data2['loc'])
        data_count3 = collections.Counter(data3['loc'])
        # data_count1 = pd.DataFrame(data_count1)
        # data_count2 = pd.DataFrame(data_count2)
        # data_count3 = pd.DataFrame(data_count3,index=[0])
        #将字典类型转化为dataframe类
        data_count1 = pd.DataFrame(pd.Series(data_count1), columns=['build_time'])
        data_count1 = data_count1.reset_index().rename(columns={'index': 'loc'})
        data_count2 = pd.DataFrame(pd.Series(data_count2), columns=['build_time'])
        data_count2 = data_count2.reset_index().rename(columns={'index': 'loc'})
        data_count3 = pd.DataFrame(pd.Series(data_count3), columns=['build_time'])
        data_count3 = data_count3.reset_index().rename(columns={'index': 'loc'})
        #绘图
        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.bar(data_count1['loc'], data_count1['build_time'], width=0.4, label='20年以上')
        ax1.bar(data_count2['loc'], data_count2['build_time'], width=0.4, bottom=data_count1['build_time'],
                label='5-20年内')
        ax1.bar(data_count3['loc'], data_count3['build_time'], width=0.4,
                bottom=data_count2['build_time'] + data_count1['build_time'], label='5年内')
        ax1.set_ylim(0, 1500)
        ax1.set_xticklabels(data_count1['loc'], rotation=90)
        ax1.legend(loc='upper left', shadow=True)
        plt.savefig('9.tiff', dpi=300)

        # 绘制价格柱状堆积图
        data_p = data[['unit_price', 'loc']]
        for j in range(len(data_p)):
            if (int(data_p['unit_price'].values[j]) < 30000):
                data_p['unit_price'].values[j] = '3万元以内';
            elif (int(data_p['unit_price'].values[j]) > 100000):
                data_p['unit_price'].values[j] = '10万元以上';
            else:
                data_p['unit_price'].values[j] = '3-10万元';
        #data_p.iloc[1:10]
        data_p_1 = data_p.loc[data_p['unit_price'] == '3万元以内']
        data_p_2 = data_p.loc[data_p['unit_price'] == '3-10万元']
        data_p_3 = data_p.loc[data_p['unit_price'] == '10万元以上']
        dic1 = collections.Counter(data_p_1['loc'])
        dic2 = collections.Counter(data_p_2['loc'])
        dic3 = collections.Counter(data_p_3['loc'])
        sl = set(data['loc'])
        # 将字典类型转化为dataframe类
        #因为各字典中都有缺少loc信息的情况，因此手动制作三个字典
        data_p_count1 = {'朝阳': 0, '海淀': 0, '朝阳': 0, '丰台': 0, '东城': 0, '西城': 0, '怀柔': 0, '大兴': 0, '密云': 0, '平谷': 0,
                         '延庆': 0, '昌平': 0, '房山': 0, '石景山': 0, '通州': 0, '门头沟': 0, '顺义': 0, '北京周边': 0}
        data_p_count2 = {'朝阳': 0, '海淀': 0, '朝阳': 0, '丰台': 0, '东城': 0, '西城': 0, '怀柔': 0, '大兴': 0, '密云': 0, '平谷': 0,
                         '延庆': 0, '昌平': 0, '房山': 0, '石景山': 0, '通州': 0, '门头沟': 0, '顺义': 0, '北京周边': 0}
        data_p_count3 = {'朝阳': 0, '海淀': 0, '朝阳': 0, '丰台': 0, '东城': 0, '西城': 0, '怀柔': 0, '大兴': 0, '密云': 0, '平谷': 0,
                         '延庆': 0, '昌平': 0, '房山': 0, '石景山': 0, '通州': 0, '门头沟': 0, '顺义': 0, '北京周边': 0}
        for i in sl:
            #填充非空数据
            if dic1[i]:
                data_p_count1[i] = dic1[i]
            if dic2[i]:
                data_p_count2[i] = dic2[i]
            if dic3[i]:
                data_p_count3[i] = dic3[i]
        #data_p_count3
        #此步操作同bulid_time
        data_p_count1 = pd.DataFrame(pd.Series(data_p_count1), columns=['unit_price'])
        data_p_count1 = data_p_count1.reset_index().rename(columns={'index': 'loc'})
        data_p_count2 = pd.DataFrame(pd.Series(data_p_count2), columns=['unit_price'])
        data_p_count2 = data_p_count2.reset_index().rename(columns={'index': 'loc'})
        data_p_count3 = pd.DataFrame(pd.Series(data_p_count3), columns=['unit_price'])
        data_p_count3 = data_p_count3.reset_index().rename(columns={'index': 'loc'})
        # fig = plt.figure(figsize=(10, 10))
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.bar(data_p_count1['loc'], data_p_count1['unit_price'], width=0.4, label='3万元以内')
        ax2.bar(data_p_count2['loc'], data_p_count2['unit_price'], width=0.4, bottom=data_p_count1['unit_price'],
                label='3-10万元')
        ax2.bar(data_p_count3['loc'], data_p_count3['unit_price'], width=0.4,
                bottom=data_p_count2['unit_price'] + data_p_count1['unit_price'], label='10万元以上')
        ax2.set_ylim(0, 1500)
        ax2.set_xticklabels(data_p_count1['loc'], rotation=90)
        ax2.legend(loc='upper left', shadow=True)
        plt.show()



