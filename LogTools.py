# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp
from module.gui.Main_md import LogMain
from module.gui.DialogDB_md import DialogDB

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # 生成初始界面
    gui = LogApp()

    # guiMain 是 LogTools 主界面的实例
    guiMain = LogMain()
    def enable_LogMain(company_name, category_name, product_name):
        # 将初始界面获取的产品分类数据传递到 LogTools 主界面里
        guiMain.product_type = [company_name, category_name, product_name]
        # 显示 LogTools 主界面
        guiMain.show()
        # 隐藏 LogTools 初始界面
        gui.hide()
    gui.singal_btn_start.connect(enable_LogMain)

    # 选择 DB 的对话框
    dbgui = DialogDB()
    def enable_DialogDB(company_name, category_name, product_name):
        # 清除上一次的记录
        dbgui.line_dbname.clear()
        dbgui.line_filepath.clear()
        # 将主界面获取的产品分类数据传递到 Select DB 的界面里
        dbgui.product_type = [company_name, category_name, product_name]
        dbgui.show()
    guiMain.singal_btn_import.connect(enable_DialogDB)

    # 日志分析线程/进程
    def log_import(task_info):
        # 启动的任务参数数据
        print('传递的数据:', task_info)
        # 打开进度条
        guiMain.progressBar.show()

        ############ 暂未实现 ############
        # 预处理：检索需要读取的日志文件列表
        pass
        # 处理中：读取日志/将数据写入数据库
        pass
        # 处理后：收尾内容，做一些后续的处理

    dbgui.singal_log_task.connect(log_import)

    gui.show()
    sys.exit(app.exec_())