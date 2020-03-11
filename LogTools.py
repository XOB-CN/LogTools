# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp
from module.gui.Main_md import LogMain

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # 生成初始界面
    gui = LogApp()

    # guiMain 是 LogTools 主界面的实例
    guiMain = LogMain()
    def enable_LogMain(company_name, category_name, product_name):
        print(company_name + '\n' + category_name + '\n' + product_name)
        # 显示 LogTools 主界面
        guiMain.show()
        # 隐藏 LogTools 初始界面
        gui.hide()
    gui.singal_btn_start.connect(enable_LogMain)

    gui.show()
    sys.exit(app.exec_())