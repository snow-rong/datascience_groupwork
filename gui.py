# coding:utf-8

import re
import spider
import paintjob
from TitleBar import *
import xlrd
import pandas as pd
from PyQt5.QtWidgets import QWidget, QPushButton,QTextBrowser,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore,QtGui,QtWidgets
import sys
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent,QMediaPlaylist

class MainUi(QtWidgets.QMainWindow):#设计GUI
    up_price = 10E20;
    down_square=0;
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        # 设置背景音乐，并设置其音量为25
        self.playlist = QMediaPlaylist()  # 设置播放列表
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("holo_inochi_inst.mp3")))
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile("Sea, You & Me.mp3")))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)  # 设置播放模式为循环播放
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)  # 在播放器中载入播放列表
        self.player.setVolume(25)  # 设置音量值为25，可在此调整音量大小
        self.player.play()
        #设置窗口大小固定
        self.setFixedSize(960,700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.top_widget = QtWidgets.QWidget()  # 创建顶部插件
        self.top_widget.setObjectName('top_widget')

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格
        self.main_layout.addWidget(self.top_widget, 0,0,12,12)
        self.main_layout.addWidget(self.left_widget,1,0,12,2) # 左侧部件在第1行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,1,2,12,10) # 右侧部件在第1行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件
        #字体设置
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(11)
        font1 = QtGui.QFont()
        font1.setFamily("KaiTi")
        font1.setPointSize(9)
        # 设置数据图形描述及其下拉列表
        self.search_push_button0 = QPushButton(self.tr("图像描述"))
        self.search_push_button0.setStyleSheet(""
                                               "QPushButton{background-color:white;color: black;"
                                               "border-radius: 7px; "
                                               "border: 2px groove gray; "
                                               "border-style: outset;}"
                                               "QPushButton:hover{background-color:#A6FFFF; color: black;}"
                                               "QPushButton:pressed{background-color:red;border-style: inset; }");
        self.search_push_button0.setIcon(QIcon("paint.jpg"));
        self.left_layout.addWidget(self.search_push_button0, 1, 1, 1, 1)
        self.comboBox_Dept0 = QtWidgets.QComboBox(self.left_widget)
        self.comboBox_Dept0.setGeometry(QtCore.QRect(30, 165, 100, 25))
        self.comboBox_Dept0.setFont(font)
        self.comboBox_Dept0.setObjectName("comboBox_Dept0")
        self.comboBox_Dept0.addItem("饼图")
        self.comboBox_Dept0.addItem("柱状堆积图")
        self.comboBox_Dept0.addItem("价格条形图")
        self.comboBox_Dept0.addItem("价格箱线图")

        self.search_push_button1 = QPushButton(self.tr("启动爬虫"))#设置启动爬虫按钮
        #按钮设置
        self.search_push_button1.setStyleSheet(""
                                               "QPushButton{background-color:white;color: black;"
                                               "border-radius: 7px; "
                                               "border: 2px groove gray; "
                                               "border-style: outset;}"
                                               "QPushButton:hover{background-color:#A6FFFF; color: black;}"
                                               "QPushButton:pressed{background-color:red;border-style: inset; }");
        self.search_push_button1.setIcon(QIcon("win.png"));
        self.left_layout.addWidget(self.search_push_button1, 0, 1, 1, 1)
        #价格及其文本输入框设置
        self.left_label_1 = QtWidgets.QPushButton("房价")
        self.left_label_1.setObjectName('left_label')
        self.lineEdit_ID1 = QtWidgets.QLineEdit(self.left_widget)
        #self.left_layout.addWidget(self.lineEdit_ID1, 2, 0,1,1)#可随比例变化(难看)
        self.lineEdit_ID1.setGeometry(QtCore.QRect(25, 250, 100, 30))#不可随比例变化(不难看)
        self.lineEdit_ID1.setFont(font1)
        self.lineEdit_ID1.setObjectName("lineEdit_ID1")
        self.lineEdit_ID1.setPlaceholderText("总价上限/万元")
        # 面积及其文本输入框设置
        self.left_label_2 = QtWidgets.QPushButton("面积")
        self.left_label_2.setObjectName('left_label')
        self.lineEdit_ID2 = QtWidgets.QLineEdit(self.left_widget)
        #self.left_layout.addWidget(self.lineEdit_ID2, 4, 0,1,1)
        self.lineEdit_ID2.setGeometry(QtCore.QRect(25, 330, 100, 30))
        self.lineEdit_ID2.setFont(font1)
        self.lineEdit_ID2.setObjectName("lineEdit_ID2")
        self.lineEdit_ID2.setPlaceholderText("面积下限/m²")
        # 楼层及其下拉列表设置
        self.left_label_3 = QtWidgets.QPushButton("楼层")
        self.left_label_3.setObjectName('left_label')
        self.comboBox_Dept3 = QtWidgets.QComboBox(self.left_widget)
       #self.left_layout.addWidget(self.comboBox_Dept3, 6, 0, 1, 1)
        self.comboBox_Dept3.setGeometry(QtCore.QRect(25, 410, 100, 30))
        self.comboBox_Dept3.setFont(font)
        self.comboBox_Dept3.setObjectName("comboBox_Dept3")
        self.comboBox_Dept3.addItem("任意")
        self.comboBox_Dept3.addItem("低层")
        self.comboBox_Dept3.addItem("中层")
        self.comboBox_Dept3.addItem("高层")
        #区域及其下拉列表设置
        self.left_label_4 = QtWidgets.QPushButton("区域")
        self.left_label_4.setObjectName('left_label')
        self.comboBox_Dept1 = QtWidgets.QComboBox(self.left_widget )
        self.comboBox_Dept1.resize(100,30)
        #self.left_layout.addWidget(self.comboBox_Dept1, 8, 0, 1, 1)
        self.comboBox_Dept1.setGeometry(QtCore.QRect(25, 490, 100, 30))
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
        #户型及其下拉列表设置
        self.left_label_5 = QtWidgets.QPushButton("户型")
        self.left_label_5.setObjectName('left_label')
        self.comboBox_Dept2 = QtWidgets.QComboBox(self.left_widget)
        #self.left_layout.addWidget(self.comboBox_Dept2, 10, 0, 1, 1)
        self.comboBox_Dept2.setGeometry(QtCore.QRect(25, 575, 100, 30))
        self.comboBox_Dept2.setFont(font)
        self.comboBox_Dept2.setObjectName("comboBox_Dept2")
        self.comboBox_Dept2.addItem("任意")
        self.comboBox_Dept2.addItem("1室")
        self.comboBox_Dept2.addItem("2室")
        self.comboBox_Dept2.addItem("3室")
        self.comboBox_Dept2.addItem("4室")
        self.comboBox_Dept2.addItem("5室")
        self.comboBox_Dept2.addItem("5室以上")
        #设置各功能区位置
        self.left_layout.addWidget(self.left_label_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_4, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_5, 10, 0, 1, 3)

        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)

        self.search_push_button2= QPushButton(self.tr("查询"))
        self.search_push_button2.setStyleSheet('''
                                QPushButton{background-color:white;color: black;
                                            border-radius: 10px; 
                                            border: 2px groove gray; 
                                            border-style: outset;}
                                QPushButton:hover{background-color:black; color: white;}
                                QPushButton:pressed{background-color:rgb(85, 170, 255);border-style: inset; }''');
        self.search_push_button2.setIcon(QIcon("search.jpg"));

        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入所需二手房的地址信息")
        self.right_bar_layout.addWidget(self.search_push_button2, 1, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 1, 1, 1, 6)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 7)
        self.search_push_button0.clicked.connect(self.data_paint)
        self.search_push_button1.clicked.connect(self.spider_start_up)
        self.search_push_button2.clicked.connect(self.condition)

        #输出文本框设置
        self.right_recommend_widget = QtWidgets.QWidget()#设置输出文本框
        self.right_recommend_layout = QtWidgets.QGridLayout()
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.text_browser = QTextBrowser(self)
        self.text_browser.setStyleSheet("background:transparent;border-width:0;border-style:outset;")#设置边框透明不可见
        self.right_recommend_layout.addWidget(self.text_browser, 0, 0)
        self.right_layout.addWidget(self.right_recommend_widget, 1, 0, 2, 9)
        # 顶部部件具体设置
        self.top_widget.setStyleSheet('''
                           QWidget#top_widget{
                              color:#232C51;
                              background-image:url(time.png);
                              background-size:cover;
                              font-size:12px;
                              border:2px solid #423f48;
                              font: "KaiTi";
                              margin:0px;
                              border-top:1px solid darkGray;
                              border-bottom:1px solid darkGray;
                              border-right:1px solid darkGray;
                              border-left:1px solid darkGray;
                              border-top-right-radius:10px;
                              border-top-left-radius:10px;
                              
                           }
                           QLabel#right_lable{
                               border:none;
                               font-size:16px;
                               font-weight:700;
                               font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                           }
                       ''')

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
                       color:#232C51;
                       background-image:url(time1.jpg);
                       background-size:cover;
                       border-top:1px solid white;
                       border-bottom:1px solid white;
                       border-left:1px solid white;
                       border-bottom-left-radius:10px;
                     
                   }
                   QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
               ''')
        # 右侧部件具体设置
        self.right_widget.setStyleSheet('''
                   QWidget#right_widget{
                       color:#232C51;
                       background:url(sp .jpg);
                       background-repeat:no-repeat;
                       background-size:cover;
                       border-top:1px solid darkGray;
                       border-bottom:1px solid darkGray;
                       border-right:1px solid darkGray;
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
        self.InitializeViews()  # 设置标题栏
        self.main_layout.setSpacing(0)

    def InitializeViews(self):#标题栏初始化
        #设置顶部布局
        self.titleBar = TitleBar(self)
        self.lay = QVBoxLayout(self)
        self.top_widget.setLayout(self.lay)
        self.client = QWidget(self)
        self.lay.addWidget(self.titleBar);
        self.lay.addWidget(self.client);
        self.lay.setStretch(1, 10);
        self.lay.setSpacing(0);
        self.lay.setContentsMargins(0, 0, 0, 0)
        #将数据传输至标题栏程序，初始化标题栏
        self.titleBar.SetIcon(QPixmap("win.png"));
        self.titleBar.SetTitle("<font color='white'>"+"北京二手房爬虫@PEX");

    def spider_start_up(self):#爬虫启动程序
        spider.start()
        msg_box = QtWidgets.QMessageBox;
        msg_box.information(self.search_push_button1, "爬取成功", "爬虫数据已成功导入本地", QMessageBox.Yes | QMessageBox.No)

    def show_info(self,str):#textbrowser打印程序
        self.text_browser.append("<font color='black'>" + str);
        self.text_browser.repaint();

    def get_all_area(self):
        dl = xlrd.open_workbook(r'D:\house.xlsx')
        house_list = [];#得到区域名
        for sheet in dl.sheets():
            house_list.append(sheet.name);
        return house_list;

    def getall(self,hl):
        df = None;#遍历sheets得到总体数据表
        for name in hl:
            df1 = pd.read_excel(r"D:\house.xlsx", sheet_name=name)
            df1['loc'] = name;
            df = pd.concat([df, df1]);
        return df;

    def condition(self):#条件响应
        #读取各筛选信息
        up_prince_input=self.lineEdit_ID1.text();#价格上限
        down_square_input=self.lineEdit_ID2.text();#面积下限
        if up_prince_input:
            self.up_price=int(up_prince_input);
        if down_square_input:
            self.down_square=int(down_square_input);
        floor=self.comboBox_Dept3.currentText();#楼层情况
        type= self.comboBox_Dept2.currentText();#类型
        area= self.comboBox_Dept1.currentText();#区域
        house_info = self.right_bar_widget_search_input.text();#具体地址
        self.search(floor,type,area,house_info);

    def search(self,floor,type,area,house_info):#信息检索函数
        #对筛选信息进行查询
        self.text_browser.clear();
        house_list=self.get_all_area();
        if area!='任意':
            df = pd.read_excel(r'D:\house.xlsx', sheet_name=area)
            df['loc'] = area;
        else:
            df=self.getall(house_list);
        #依次调用函数筛选数据列
        df=self.house_type(df,type);
        df=self.house_floor(df,floor);
        df=self.house_price(df);
        df=self.house_square(df);
        df=self.house_info_search(df,house_info)
       # print(df)
        if len(df):
            for i in range(len(df)):
                #将信息拆分，避免因为信息数据过大造成textbrowser卡死
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
                for j in range(7):#逐条添加，避免卡死情况
                    self.show_info(msg[j])
                self.text_browser.append("\n");
            self.text_browser.append("共"+str(len(df))+"条");
        else:
            msg_box = QtWidgets.QMessageBox;
            msg_box.information(self.search_push_button2, "没找到对象", "未找到符合条件的房屋，请更改条件后再试", QMessageBox.Yes | QMessageBox.No)

    def house_info_search(self,a1, house_info):#住房地址信息查询
        if house_info:
            return a1.loc[a1['address'].str.contains(house_info)];
        else:
            return a1;

    def house_type(self,a2,type):#房屋类型查询
        if type=='任意':
            return a2;
        else:
            return a2.loc[a2['house_type'].str.contains(type)];

    def house_price(self,a3):#价格查询
        aa=[]
        for j in range(len(a3)):
            dd1 = re.findall(r'\d+', a3['price'].values[j])
            dd1 = int(''.join(dd1))
            if dd1 <= self.up_price:
                aa.append(a3.iloc[j])
        aa = pd.DataFrame(aa)
        return aa

    def house_square(self,a4):#住房面积查询
        aa2=[]
        for j in range(len(a4)):
            dd = re.findall(r'\d+', a4['build_area'].values[j])
            dd = int(''.join(dd))
            if dd >= self.down_square:
                aa2.append(a4.iloc[j])
        aa2 = pd.DataFrame(aa2)
        return aa2

    def house_floor(self,a5,floor):#楼层查询
        if floor=='任意':
            return a5;
        else:
            if floor=='低层':
                ddd = a5.loc[a5['bulid_floor'].str.contains('低层')]
                dddd = a5.loc[a5['bulid_floor'].str[1] != '层']
                return pd.concat([ddd,dddd]);
            else:
                return a5.loc[a5['bulid_floor'].str.contains(floor)];

    def data_paint(self):#图形绘制函数
        paintmsg=self.comboBox_Dept0.currentText()#选择绘制图形
        housename=self.get_all_area();#得到总数据源
        data=self.getall(housename);
        data = data[data['build_time'] != 'NAN']#去除建造时间为空的数据行
        for j in range(len(data)):
            #将字符类型转化为数值类型进行绘图工作
            #先将各数据转化为纯数字字符串形式
            data['unit_price'].values[j] = re.findall(r'\d+', data['unit_price'].values[j])
            data['unit_price'].values[j] = int(''.join(data['unit_price'].values[j]))#每平米价格
            data['price'].values[j] = re.findall(r'\d+', data['price'].values[j])
            data['price'].values[j] = int(''.join(data['price'].values[j]))#总价
            data['build_area'].values[j] = re.findall(r'\d+', data['build_area'].values[j])
            data['build_area'].values[j] = int(''.join(data['build_area'].values[j])) #面积
            #对于年代数据，根据建造时间按照其年数分类
            data['build_time'].values[j] = re.findall(r'\d+', data['build_time'].values[j])
            data['build_time'].values[j] = int(''.join(data['build_time'].values[j]))
            #对年代信息进行分类
            if (int(data['build_time'].values[j] )< 2000):
                data['build_time'].values[j] = '20年以上';
            elif (int(data['build_time'].values[j]) > 2015):
                data['build_time'].values[j] = '5年内';
            else:
                data['build_time'].values[j] = '5-20年内';
        #调用函数进行绘制
        paintjob.painting(paintmsg,data)

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())



