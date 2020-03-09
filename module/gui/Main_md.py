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