# coding:utf-8

import tkinter
from  tkinter  import ttk
from PyQt5.QtWidgets import QApplication, QWidget,QToolTip,QPushButton,QTextBrowser
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtCore,QtGui,QtWidgets

import sys
import qtawesome

class MainUi(QtWidgets.QMainWindow):#设计GUI
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

        self.left_label_1 = QtWidgets.QPushButton("房价")
        self.left_label_1.setObjectName('left_label')
        self.lineEdit_ID3 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID3.setGeometry(QtCore.QRect(30, 200, 80, 25))
        self.lineEdit_ID3.setObjectName("lineEdit_ID3")
        self.lineEdit_ID4 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID4.setGeometry(QtCore.QRect(30, 230, 80, 25))
        self.lineEdit_ID4.setObjectName("lineEdit_ID4")

        self.left_label_2 = QtWidgets.QPushButton("面积")
        self.left_label_2.setObjectName('left_label')
        self.lineEdit_ID1 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID1.setGeometry(QtCore.QRect(30, 300, 80, 25))
        self.lineEdit_ID1.setObjectName("lineEdit_ID1")
        self.lineEdit_ID2 = QtWidgets.QLineEdit(self.left_widget)
        self.lineEdit_ID2.setGeometry(QtCore.QRect(30, 330, 80, 25))
        self.lineEdit_ID2.setObjectName("lineEdit_ID2")

        self.left_label_3 = QtWidgets.QPushButton("楼层")
        self.left_label_3.setObjectName('left_label')
        self.comboBox_Dept3 = QtWidgets.QComboBox(self.left_widget)
        self.comboBox_Dept3.setGeometry(QtCore.QRect(30, 400, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        self.comboBox_Dept3.setFont(font)
        self.comboBox_Dept3.setObjectName("comboBox_Dept3")
        self.comboBox_Dept3.addItem("低层")
        self.comboBox_Dept3.addItem("中层")
        self.comboBox_Dept3.addItem("高层")

        self.left_label_4 = QtWidgets.QPushButton("区域")
        self.left_label_4.setObjectName('left_label')
        self.comboBox_Dept1 = QtWidgets.QComboBox(self.left_widget )
        self.comboBox_Dept1.setGeometry(QtCore.QRect(30, 500, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        self.comboBox_Dept1.setFont(font)
        self.comboBox_Dept1.setObjectName("comboBox_Dept1")
        self.comboBox_Dept1.addItem("密云区")
        self.comboBox_Dept1.addItem("延庆区")
        self.comboBox_Dept1.addItem("朝阳区")
        self.comboBox_Dept1.addItem("丰台区")
        self.comboBox_Dept1.addItem("石景山区")
        self.comboBox_Dept1.addItem("海淀区")
        self.comboBox_Dept1.addItem("门头沟区")
        self.comboBox_Dept1.addItem("房山区")
        self.comboBox_Dept1.addItem("通州区")
        self.comboBox_Dept1.addItem("顺义区")
        self.comboBox_Dept1.addItem("昌平区")
        self.comboBox_Dept1.addItem("大兴区")
        self.comboBox_Dept1.addItem("怀柔区")
        self.comboBox_Dept1.addItem("平谷区")
        self.comboBox_Dept1.addItem("东城区")
        self.comboBox_Dept1.addItem("西城区")
        self.comboBox_Dept1.addItem("北京周边")

        self.left_label_5 = QtWidgets.QPushButton("户型")
        self.left_label_5.setObjectName('left_label')
        self.comboBox_Dept2 = QtWidgets.QComboBox(self.left_widget)
        self.comboBox_Dept2.setGeometry(QtCore.QRect(30, 600, 100, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        self.comboBox_Dept2.setFont(font)
        self.comboBox_Dept2.setObjectName("comboBox_Dept2")
        self.comboBox_Dept2.addItem("一室")
        self.comboBox_Dept2.addItem("两室")
        self.comboBox_Dept2.addItem("三室")
        self.comboBox_Dept2.addItem("四室")
        self.comboBox_Dept2.addItem("五室")
        self.comboBox_Dept2.addItem("五室以上")


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
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 16))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入所需二手房的详细信息")
        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)



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
                       background-image:url(sp.jpg);
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

def info():
    return self.right_bar_widget_search_input.text();

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


