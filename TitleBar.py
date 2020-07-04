import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from default import *
#绿色的按钮是放大/还原，黄色是最小化，红色是关闭程序
class TitleBar(QWidget):
    #初始化TitleBar
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.win = parent
        self.InitializeWindow()

    def InitializeWindow(self):
        self.isPressed = False
       # self.setFixedHeight(30)
        self.InitializeViews()
        pass

    def InitializeViews(self):
        self.iconLabel = QLabel(self)
        self.titleLabel = QLabel(self)
        #设置三种按钮即其大小布局。以及图标的大小
        self.minButton = QPushButton("")
        self.restoreButton = QPushButton("")
        self.closeButton = QPushButton("")
        self.minButton.setFixedSize(15, 15);
        self.restoreButton.setFixedSize(15, 15);
        self.closeButton.setFixedSize(15, 15);

        self.iconLabel.setFixedSize(30, 30);
        self.titleLabel.setFixedHeight(20);

        self.iconLabel.setAlignment(Qt.AlignCenter);
        self.titleLabel.setAlignment(Qt.AlignCenter);

        self.closeButton.setStyleSheet(  # 设置按钮属性
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.minButton.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.restoreButton.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        #功能绑定
        self.minButton.clicked.connect(self.ShowMininizedWindow)
        self.restoreButton.clicked.connect(self.ShowRestoreWindow)
        self.closeButton.clicked.connect(self.CloseWindow)

        self.lay = QHBoxLayout(self)
        self.setLayout(self.lay)

        self.lay.setSpacing(10)

        self.lay.addWidget(self.iconLabel)
        self.lay.addWidget(self.titleLabel)
        self.lay.addWidget(self.restoreButton)
        self.lay.addWidget(self.minButton)
        self.lay.addWidget(self.closeButton)
    #设置标题栏具体功能和对事件响应机制
    def ShowMininizedWindow(self):
        self.win.showMinimized()

    def ShowMaximizedWindow(self):
        self.win.showMaximized()

    def ShowRestoreWindow(self):
        if self.win.isMaximized():
            self.win.showNormal()
        else:
            self.win.showMaximized()

    def CloseWindow(self):
        self.win.close()

    def SetTitle(self, str):
        self.titleLabel.setText(str)
        font = QFont()
        font.setFamily("KaiTi")
        font.setPointSize(12)
        self.titleLabel.setFont(font)

    def SetIcon(self, pix):
        self.iconLabel.setPixmap(pix.scaled(self.iconLabel.size() - QSize(1, 1)))

    def mouseDoubleClickEvent(self, event):
        self.ShowRestoreWindow()
        return QWidget().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        self.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.isPressed:
            if self.win.isMaximized:
                self.win.showNormal()
            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            self.win.move(self.win.pos() + movePos)
        return QWidget().mouseMoveEvent(event)