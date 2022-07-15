# -*- coding: utf-8 -*-

import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Window(QMainWindow):
    # 상수 위주
    FILTER = ['IKJnt', 'FKJnt', 'RSJnt', '']

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle('Search joint UI')
        # ui만
        self.ui()
        # connection 정보들
        self.connections()

        # ui 만든 후 최초 실행할 함수들
        self.init()

    def connections(self):
        pass

    def init(self):
        self.init_combobox()

    def init_combobox(self):
        self.filter_combobox.addItems(self.FILTER)

    def ui(self):
        # central widget
        self.centralwidget = QWidget(self)

        # main layout
        self.main_layout = QVBoxLayout()

        #
        self.data_layout = QHBoxLayout()

        # central widget -> setlayout
        self.sub_layout = QHBoxLayout()


        # listwidget
        self.data = QListWidget()
        self.data.setMinimumWidth(300)
        self.data.setMinimumHeight(300)
        self.data_layout.addWidget(self.data)

        # tablewidget
        self.table = QTableWidget()
        self.table.setMinimumWidth(300)
        self.table.setMinimumHeight(300)
        self.data_layout.addWidget(self.table)



        # combobox filter
        self.filter_combobox = QComboBox()
        self.filter_combobox.setFixedSize(100, 30)
        self.sub_layout.addWidget(self.filter_combobox)

        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addLayout(self.sub_layout)



        # search button
        self.button_search = QPushButton("search")
        self.button_search.setMinimumHeight(30)
        self.sub_layout.addWidget(self.button_search)

        self.centralwidget.setLayout(self.main_layout)
        self.setCentralWidget(self.centralwidget)


def show():
    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    win = Window()
    win.show()


show()