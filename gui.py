# coding:utf-8

import requests
import re
import os,xlrd
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import tkinter
from  tkinter  import ttk
from PyQt5.QtWidgets import QApplication, QWidget,QToolTip,QPushButton,QTextBrowser,QMessageBox
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
import qtawesome

class MainUi(QtWidgets.QMainWindow):#设计GUI
    up_price = 10E20;
    down_square=0;
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(QCoreApplication.instance().quit)#设置关闭按钮响应
        self.left_normal = QtWidgets.QPushButton("")  # 还原按钮
        self.left_normal.clicked.connect(self.showNormal);
        self.left_max = QtWidgets.QPushButton("")  # 最大化按钮
        self.left_max.clicked.connect(self.showMaximized);
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_normal.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_max.setFixedSize(15, 15)  # 设置最大化按钮大小
        self.left_close.setStyleSheet(#设置按钮属性
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_normal.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_max.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font1 = QtGui.QFont()
        font1.setFamily("KaiTi")
        font1.setPointSize(8)
        self.left_label_1 = QtWidgets.QPushButton("房价")
        self.left_label_1.setObjectName('left_label')
        self.lineEdit_ID1 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID1.setGeometry(QtCore.QRect(30, 200, 100, 30))
        self.lineEdit_ID1.setFont(font1)
        self.lineEdit_ID1.setObjectName("lineEdit_ID1")
        self.lineEdit_ID1.setPlaceholderText("总价上限/万元")

        self.left_label_2 = QtWidgets.QPushButton("面积")
        self.left_label_2.setObjectName('left_label')
        self.lineEdit_ID2 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID2.setGeometry(QtCore.QRect(30, 300, 100, 30))
        self.lineEdit_ID2.setFont(font1)
        self.lineEdit_ID2.setObjectName("lineEdit_ID2")
        self.lineEdit_ID2.setPlaceholderText("面积下限/m²")

        self.left_label_3 = QtWidgets.QPushButton("楼层")
        self.left_label_3.setObjectName('left_label')
        self.comboBox_Dept3 = QtWidgets.QComboBox(self.left_widget)
        self.comboBox_Dept3.setGeometry(QtCore.QRect(30, 400, 100, 30))
        self.comboBox_Dept3.setFont(font)
        self.comboBox_Dept3.setObjectName("comboBox_Dept3")
        self.comboBox_Dept3.addItem("任意")
        self.comboBox_Dept3.addItem("低层")
        self.comboBox_Dept3.addItem("中层")
        self.comboBox_Dept3.addItem("高层")

        self.left_label_4 = QtWidgets.QPushButton("区域")
        self.left_label_4.setObjectName('left_label')
        self.comboBox_Dept1 = QtWidgets.QComboBox(self.left_widget )
        self.comboBox_Dept1.setGeometry(QtCore.QRect(25, 500, 102, 30))
        self.comboBox_Dept1.setFont(font)
        self.comboBox_Dept1.setObjectName("comboBox_Dept1")
        self.comboBox_Dept1.addItem("任意")
        self.comboBox_Dept1.addItem("密云")
        self.comboBox_Dept1.addItem("延庆")
        self.comboBox_Dept1.addItem("朝阳")
        self.comboBox_Dept1.addItem("丰台")
        self.comboBox_Dept1.addItem("石景山")
        self.comboBox_Dept1.addItem("海淀")
        self.comboBox_Dept1.addItem("门头沟")
        self.comboBox_Dept1.addItem("房山")
        self.comboBox_Dept1.addItem("通州")
        self.comboBox_Dept1.addItem("顺义")
        self.comboBox_Dept1.addItem("昌平")
        self.comboBox_Dept1.addItem("大兴")
        self.comboBox_Dept1.addItem("怀柔")
        self.comboBox_Dept1.addItem("平谷")
        self.comboBox_Dept1.addItem("东城")
        self.comboBox_Dept1.addItem("西城")
        self.comboBox_Dept1.addItem("北京周边")

        self.left_label_5 = QtWidgets.QPushButton("户型")
        self.left_label_5.setObjectName('left_label')
        self.comboBox_Dept2 = QtWidgets.QComboBox(self.left_widget)
        self.comboBox_Dept2.setGeometry(QtCore.QRect(25, 600, 102, 30))
        self.comboBox_Dept2.setFont(font)
        self.comboBox_Dept2.setObjectName("comboBox_Dept2")
        self.comboBox_Dept2.addItem("任意")
        self.comboBox_Dept2.addItem("1室")
        self.comboBox_Dept2.addItem("2室")
        self.comboBox_Dept2.addItem("3室")
        self.comboBox_Dept2.addItem("4室")
        self.comboBox_Dept2.addItem("5室")
        self.comboBox_Dept2.addItem("5室以上")



        self.left_layout.addWidget(self.left_max, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_normal, 0, 1, 1, 1)

        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_4, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_5, 9, 0, 1, 3)

        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_push_button= QPushButton(self.tr("查询"))
        self.search_push_button.setStyleSheet(""
                                "QPushButton{background-color:white;color: black;"
                                            "border-radius: 10px; "
                                            "border: 2px groove gray; "
                                            "border-style: outset;}"
                                "QPushButton:hover{background-color:black; color: white;}"
                                "QPushButton:pressed{background-color:rgb(85, 170, 255);border-style: inset; }");
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入所需二手房的信息")
        self.right_bar_layout.addWidget(self.search_push_button, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)
        self.search_push_button.clicked.connect(self.condition)

        self.right_recommend_widget = QtWidgets.QWidget()#设置输出文本框
        self.right_recommend_layout = QtWidgets.QGridLayout()
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.text_browser = QTextBrowser(self)
        self.text_browser.setStyleSheet("background:transparent;border-width:0;border-style:outset;")
        self.right_recommend_layout.addWidget(self.text_browser, 0, 0)
        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)

        # 左侧部件具体设置
        self.left_widget.setStyleSheet('''
                   QPushButton{border:none;color:white;}
                   QPushButton#left_label{
                       border:none;
                       border-bottom:1px solid white;
                       font-size:18px;
                       font-weight:700;
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                   }
                   QWidget#left_widget{
                       background:black;
                       border-top:1px solid white;
                       border-bottom:1px solid white;
                       border-left:1px solid white;
                       border-top-left-radius:10px;
                       border-bottom-left-radius:10px;
                   }
                   QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
               ''')
        # 右侧部件具体设置

        self.right_widget.setStyleSheet('''
                   QWidget#right_widget{
                       color:#232C51;
                       background:url(sp.jpg);
                       background-repeat:no-repeat;
                       background-size:cover;
                       border-top:1px solid darkGray;
                       border-bottom:1px solid darkGray;
                       border-right:1px solid darkGray;
                       border-top-right-radius:10px;
                       border-bottom-right-radius:10px;
                   }
                   QLabel#right_lable{
                       border:none;
                       font-size:16px;
                       font-weight:700;
                       font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                   }
               ''')

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    def condition(self):#条件响应
        up_prince_input=self.lineEdit_ID1.text();
        down_square_input=self.lineEdit_ID2.text();
        if up_prince_input:
            self.up_price=int(up_prince_input);
        if down_square_input:
            self.down_square=int(down_square_input);

        floor=self.comboBox_Dept3.currentText();
        type= self.comboBox_Dept2.currentText();
        area= self.comboBox_Dept1.currentText();
        house_info = self.right_bar_widget_search_input.text();
        self.search(floor,type,area,house_info);

    def search(self,floor,type,area,house_info):
        dl = xlrd.open_workbook(r'D:\house.xlsx')
        house_list=[];
        df=None;
        for sheet in dl.sheets():
            house_list.append(sheet.name);
        if area!='任意':
            df = pd.read_excel(r'D:\house.xlsx', sheet_name=area)
            df['loc'] = area;
        else:
            for name in house_list:
                df1 = pd.read_excel(r"D:\house.xlsx", sheet_name=name)
                df1['loc'] = name;
                df=pd.concat([df,df1]);
        df=self.house_type(df,type);
        df=self.house_floor(df,floor);
        df=self.house_price(df);
        df=self.house_square(df);
        df=self.house_info_search(df,house_info)
       # print(df)
        if len(df):
            for i in range(len(df)):
                msg=['1','2','3','4','5','6','7'];
                loc=df['loc'].iloc[i]
                house_type=df['house_type'].iloc[i];
                build_area=df['build_area'].iloc[i];
                bulid_floor = df['bulid_floor'].iloc[i];
                address = df['address'].iloc[i];
                price = df['price'].iloc[i];
                unit_price = df['unit_price'].iloc[i];
                build_time = df['build_time'].iloc[i];
                house_tags = df['house_tags'].iloc[i];
                msg[0] ='编号:' + str(i+1);
                msg[1]='所在区域:'+loc+" 面积:"+build_area;
                msg[2]="地址:"+address;
                msg[3]="售价:"+price+" 每平米售价:"+unit_price;
                msg[4]="楼层:"+bulid_floor+" 样式:"+house_type;
                msg[5] = "修建时间:"+build_time;
                msg[6]="特点:"+house_tags+'\n';
                for j in range(7):
                    self.text_browser.append("<font color='black'>" +msg[j]);
                    self.text_browser.repaint();
                self.text_browser.append("\n");
        else:
            msg_box = QtWidgets.QMessageBox;
            msg_box.information(self.search_push_button, "没找到对象", "未找到符合条件的房屋，请更改条件后再试", QMessageBox.Yes | QMessageBox.No)





    def house_info_search(self,a1, house_info):
        if house_info:
            return a1.loc[a1['address'].str.contains(house_info)];
        else:
            return a1;

    def house_type(self,a2,type):
        if type=='任意':
            return a2;
        else:
            return a2.loc[a2['house_type'].str.contains(type)];

    def house_price(self,a3):
        aa=[]
        for j in range(len(a3)):
            dd1 = re.findall(r'\d+', a3['price'].values[j])
            dd1 = int(''.join(dd1))
            if dd1 <= self.up_price:
                aa.append(a3.iloc[j])
        aa = pd.DataFrame(aa)
        return aa

    def house_square(self,a4):
        aa2=[]
        for j in range(len(a4)):
            dd = re.findall(r'\d+', a4['build_area'].values[j])
            dd = int(''.join(dd))
            if dd >= self.down_square:
                aa2.append(a4.iloc[j])
        aa2 = pd.DataFrame(aa2)
        return aa2

    def house_floor(self,a5,floor):
        if floor=='任意':
            return a5;
        else:
            if floor=='低层':
                ddd = a5.loc[a5['bulid_floor'].str.contains('低层')]
                dddd = a5.loc[a5['bulid_floor'].str[1] != '层']
                return pd.concat([ddd,dddd]);
            else:
                return a5.loc[a5['bulid_floor'].str.contains(floor)];

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())



