# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gui = LogApp()

    # 初始化数据列表
    gui.load_cbx_company()
    gui.load_cbx_category()
    gui.load_cbx_product()

    gui.setWindowTitle('LogTools')
    gui.show()
    sys.exit(app.exec_())