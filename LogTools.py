# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from module.gui.LogTools_ui import Ui_Form

class LogTools(QtWidgets.QWidget, Ui_Form):
    """
    LogTools GUI
    """
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = QtWidgets.QWidget()
    ui = LogTools()
    ui.setupUi(gui)
    gui.setWindowTitle('LogTools')
    gui.show()
    sys.exit(app.exec_())