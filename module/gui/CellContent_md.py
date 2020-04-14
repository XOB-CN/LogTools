# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.CellContent_ui import Ui_Form

class CellContent(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 修改标题
        self.setWindowTitle('Cell Content')

    def showContent(self, content):
        self.cellText.setText(content)
        self.show()