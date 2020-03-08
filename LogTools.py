# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    gui = LogApp()
    gui.load_cbx_company()
    gui.load_cbx_category()
    gui.load_cbx_product()
    gui.show()
    sys.exit(app.exec_())