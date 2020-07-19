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
        代码参考链接：http://jiuaitu.com/python/407.html
        :return:
        """
        search_key = self.line_search.text()

        # 如果不启用正则表达式
        if self.btn_regexp.isChecked() == False:
            # 如果没有勾选反向查找
            if self.btn_reverse.isChecked() == False:
                self.cellText.find(search_key)
                # 重新设置焦点
                self.cellText.setFocus()
            else:
                self.cellText.find(search_key, QTextDocument.FindBackward)
                # 重新设置焦点
                self.cellText.setFocus()

        # 如果启用正则表达式
        else:
            regexp_key = QRegExp(search_key)
            # 如果没有勾选反向查找
            if self.btn_reverse.isChecked() == False:
                self.cellText.find(regexp_key)
                # 重新设置焦点
                self.cellText.setFocus()
            else:
                self.cellText.find(regexp_key, QTextDocument.FindBackward)
                # 重新设置焦点
                self.cellText.setFocus()