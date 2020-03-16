# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.DialogDB_ui import Ui_Dialog

class DialogDB(QWidget, Ui_Dialog):
    """
    创建/导入数据库的对话框
    """
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 显示窗口标题
        self.setWindowTitle('Select DB')