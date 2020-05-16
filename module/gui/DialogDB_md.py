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
    # 接收产品分类
    product_type = []
    # 自定义信号，传递需要读取的日志信息的字典数据
    singal_log_task = pyqtSignal(dict)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 显示窗口标题
        self.setWindowTitle('Select DB')

    def slot_select_db(self):
        """
        获取已存在的 DB 名，并将值填写到对应的 QlineEdit 对象中
        """
        db_dialog = QFileDialog.getOpenFileName(directory='./data', filter='*.db')
        db_name = os.path.basename(db_dialog[0][:-3])
        # QlineEdit：DB Name
        self.line_dbname.setText(db_name)

    def slot_file_path(self):
        """
        获取文件路径，并将值填写到对应的 QlineEdit 对象
        """
        logpath_dialog = QFileDialog.getOpenFileName()
        logpath = logpath_dialog[0]
        # QlineEdit：File Path
        self.line_filepath.setText(logpath)

    def slot_dir_path(self):
        """
        获取目录路径，并将值填写到对应的 QlineEdit 对象
        """
        logpath_dialog = QFileDialog.getExistingDirectory()
        logpath = logpath_dialog
        # QlineEdit：Dir Path
        self.line_dirpath.setText(logpath)

    def slot_accept(self):
        """
        生成任务清单，准备读取日志
        """
        taskdata = {'db_name':self.line_dbname.text(),
                    'dir_path':self.line_dirpath.text(),
                    'file_path': self.line_filepath.text(),
                    'product_type':self.product_type[0] + '-' + self.product_type[1] + '-' + self.product_type[2]}
        self.singal_log_task.emit(taskdata)
        self.hide()