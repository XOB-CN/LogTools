# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from module.gui.LogTools_ui import Ui_Form

class LogTools(QtWidgets.QWidget, Ui_Form):
    """
    LogTools GUI class
    """
    # 类变量
    cbx_data = {
        'HPE':{'BigData':['IDOL',]},
        'MicroFocus':{'ITOM':['OA','OBM/OMi']},
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def set_cbx_default(self):
        cbx_comp_list = []
        for i in self.cbx_data:
            cbx_comp_list.append(i)
        self.cbx_company.addItems(cbx_comp_list)

    def load_cbx_category(self):
        cbx_cate_list = []
        cbx_cate_data = self.cbx_data.get(self.cbx_company.currentText())
        for i in cbx_cate_data:
            cbx_cate_list.append(i)
        self.cbx_category.addItems(cbx_cate_list)

    def load_cbx_product(self):
        cbx_prod_list = self.cbx_data.get(self.cbx_category.currentText())
        print(cbx_prod_list)
        self.cbx_product.addItems(cbx_prod_list)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    From = QtWidgets.QWidget()
    ui = LogTools()
    ui.setupUi(From)
    # 设置 QComboBox（cbx_company）组件的默认内容
    ui.set_cbx_default()

    # 临时代码
    ui.load_cbx_category()
    ui.load_cbx_product()

    # 设置窗口标题
    From.setWindowTitle('LogTools')
    From.show()
    sys.exit(app.exec_())