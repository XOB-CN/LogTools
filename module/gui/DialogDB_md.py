# -*- coding: utf-8 -*-

import os
from PyQt5.Qt import *
from module.gui.DialogDB_ui import Ui_Dialog

class DialogDB(QDialog, Ui_Dialog):
    """
    创建/导入数据库的对话框
    """
    # 软件所在的根目录
    basepath = os.path.abspath('.')

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 显示窗口标题
        self.setWindowTitle('Select DB')

    # 获取已存在的 DB 名，并将值填写到对应的 QlineEdit 对象中
    def slot_select_db(self):
        db_dialog = QFileDialog.getOpenFileName(directory='./data', filter='*.db')
        db_name = os.path.basename(db_dialog[0][:-3])
        # QlineEdit：DB Name
        self.line_dbname.setText(db_name)

    def slot_file_path(self):
        logpath = QFileDialog.getOpenFileName()
        print(logpath)