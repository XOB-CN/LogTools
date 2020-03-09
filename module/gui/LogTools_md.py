# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_ui import Ui_Form

class LogApp(QWidget, Ui_Form):
    """
    LogTools GUI class
    """

    # 支持的软件产品
    cbx_data = {
        'MicroFocus':{'ITOM':['OA','OBM/OMi']},
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

    def load_cbx_company(self):
        cbx_comp_list = []
        for i in self.cbx_data:
            cbx_comp_list.append(i)
        self.cbx_company.clear()
        self.cbx_company.addItems(cbx_comp_list)

    def load_cbx_category(self):
        cbx_cate_list = []
        cbx_cate_data = self.cbx_data.get(self.cbx_company.currentText())
        for i in cbx_cate_data:
            cbx_cate_list.append(i)
        self.cbx_category.clear()
        self.cbx_category.addItems(cbx_cate_list)

    def load_cbx_product(self):
        cbx_prod_list = self.cbx_data.get(self.cbx_company.currentText()).get(self.cbx_category.currentText())
        self.cbx_product.clear()
        self.cbx_product.addItems(cbx_prod_list)

    def slot_update_cate(self):
        self.load_cbx_category()
        self.load_cbx_product()

    def slot_update_prod(self):
        self.load_cbx_product()

    def slot_btn_start(self):
        print(self.cbx_company.currentText(), self.cbx_category.currentText(), self.cbx_product.currentText())