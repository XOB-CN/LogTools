# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_ui import Ui_Form

class LogApp(QWidget, Ui_Form):
    """
    LogTools 启动界面的 class
    """

    # 支持的软件产品
    cbx_data = {
        'MicroFocus':{'ITOM':['OA','OBM/OMi','SiteScope']},
    }
    # 自定义信号
    singal_btn_start = pyqtSignal(str, str, str)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)
        # 初始化显示数据
        self.load_cbx_company()
        self.load_cbx_category()
        self.load_cbx_product()
        # 显示窗口标题
        self.setWindowTitle('LogTools')

    def load_cbx_company(self):
        """
        加载公司的组合框 (Combo box)
        """
        cbx_comp_list = []
        for i in self.cbx_data:
            cbx_comp_list.append(i)
        self.cbx_company.clear()
        self.cbx_company.addItems(cbx_comp_list)

    def load_cbx_category(self):
        """
        加载分类的组合框 (Combo box)
        """
        cbx_cate_list = []
        cbx_cate_data = self.cbx_data.get(self.cbx_company.currentText())
        for i in cbx_cate_data:
            cbx_cate_list.append(i)
        self.cbx_category.clear()
        self.cbx_category.addItems(cbx_cate_list)

    def load_cbx_product(self):
        """
        加载产品的组合框 (Combo box)
        """
        cbx_prod_list = self.cbx_data.get(self.cbx_company.currentText()).get(self.cbx_category.currentText())
        self.cbx_product.clear()
        self.cbx_product.addItems(cbx_prod_list)

    def slot_update_cate(self):
        """
        槽函数：更新分类和软件产品列表
        """
        self.load_cbx_category()
        self.load_cbx_product()

    def slot_update_prod(self):
        """
        槽函数：更新软件产品列表
        """
        self.load_cbx_product()

    def slot_btn_start(self):
        """
        槽函数：点击 start 按钮后, 将会发射 [公司, 分类, 产品] 的信号, 该信号由 LogTools.py 文件中的 gui.singal_btn_start.connect(enable_LogMain) 负责接收
        """
        self.singal_btn_start.emit(self.cbx_company.currentText(), self.cbx_category.currentText(), self.cbx_product.currentText())