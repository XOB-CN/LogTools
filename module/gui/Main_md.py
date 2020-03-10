# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.Main_ui import Ui_MainWindow

class LogMain(QMainWindow, Ui_MainWindow):
    """
    LogTools Main class
    """
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 设置初始的小于时间，即当前时间
        self.leTime.setDateTime(QDateTime.currentDateTime())
        # 设置初始的大于时间，即当前时间 - 30day
        self.geTime.setDateTime(QDateTime.addDays(QDateTime.currentDateTime(), -30))