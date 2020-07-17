# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.CellContent_ui import Ui_Form

class CellContent(QWidget, Ui_Form):
    """
    当双击查询结果单元格时, 展示一个文本显示框
    """
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        # 修改标题
        self.setWindowTitle('Cell Content')

    def showContent(self, content):
        """
        显示文本框
        :param content: 单元格里的字符串数据
        """
        self.cellText.setText(content)
        self.show()

    def searchText(self):
        """
        搜索指定文本, 并且高亮
        :return:
        """
        print(self.btn_regexp.isChecked())
        content = self.cellText.toPlainText()