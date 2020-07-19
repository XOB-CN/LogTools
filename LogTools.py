# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp
from module.gui.Main_md import LogMain
from module.gui.DialogDB_md import DialogDB
from module.gui.CellContent_md import CellContent
from module.tools.LogCheck import LogCheck
from module.tools.LogProducer import LogProducer
from module.tools.LogCustomer import LogCustomer
from module.tools.MenuTools import AddMenuTools
from module.tools.SettingsTools import ConfigTools
from multiprocessing import freeze_support, Pool

if __name__ == '__main__':
    # 在 Windows 环境下可以正常运行多进程
    freeze_support()
    # 可以让异常抛出但是程序继续执行 (https://blog.csdn.net/hidxl/article/details/49800353)
    # 考虑将来这部分代码可以做出 debug 模式
    # import cgitb
    # cgitb.enable(format='text')
    # Pool 对象
    p = Pool(ConfigTools.get_num_processes())

    # 主程序开始
    import sys
    app = QApplication(sys.argv)

    # 生成初始界面
    gui = LogApp()
    # 选择 DB 的对话框
    dbgui = DialogDB()
    # guiMain 是 LogTools 主界面的实例
    guiMain = LogMain()
    # 显示单元格内容的实例
    cellgui = CellContent()
    
    ######################## 跨界面的槽函数 ##############################################
    def enable_LogMain(company_name, category_name, product_name):
        """
        跳转到软件主界面
        :param company_name: str
        :param category_name: str
        :param product_name: str
        """
        # 将初始界面获取的产品分类数据传递到 LogTools 主界面里
        guiMain.product_type = [company_name, category_name, product_name]
        # 设置软件标题
        guiMain.setWindowTitle(category_name + ' ' + product_name + ' LogTools ' + 'Beta v0.5.0')
        # 判断产品分类, 加载不同的菜单
        AddMenuTools(product_name, guiMain)
        # 显示 LogTools 主界面
        guiMain.show()
        # 隐藏 LogTools 初始界面
        gui.hide()
    gui.singal_btn_start.connect(enable_LogMain)

    def enable_DialogDB(company_name, category_name, product_name):
        """
        显示日志录入界面
        :param company_name: str
        :param category_name: str
        :param product_name: str
        """
        # 清除上一次的记录
        dbgui.line_dbname.clear()
        dbgui.line_filepath.clear()
        # 将主界面获取的产品分类数据传递到 Select DB 的界面里
        dbgui.product_type = [company_name, category_name, product_name]
        dbgui.show()
    guiMain.singal_btn_import.connect(enable_DialogDB)

    def task_per_process(task_info):
        """
        日志预处理, 获取待分析的文件信息
        :param task_info:{'db_name': str, 'dir_path': str, 'file_path': '', 'product_type': str}
        """
        obj_task = LogCheck(task_info)
        # task_data:{'db_name': str, 'dir_path': str, 'file_path': list, 'product_type': str}
        task_data = obj_task.check()
        # 判断文件列表是否为空
        if task_data.get('file_path') == []:
            QMessageBox.warning(guiMain, 'No Files!', 'No files need to be analyzed!')
        else:
            # log_insert 方法将会发射一个 singal_task_start 的信号, task_running 方法会连接这个信号
            guiMain.log_insert(task_data)

    dbgui.singal_log_task.connect(task_per_process)

    def task_running(task_data):
        """
        真正的日志分析线程
        :param task_data:{'db_name': str, 'dir_path': str, 'file_path': list, 'product_type': str}
        """
        # 日志的分析线程, 该线程会启动日志的分析进程
        sub_thread1 = LogProducer(parent=guiMain, task_data=task_data, pool=p)
        sub_thread1.start()
        # 日志的保存线程, 该线程会将生成的分析数据保存到数据库
        sub_thread2 = LogCustomer(parent=guiMain, num_files=len(task_data.get('file_path')))
        sub_thread2.singal_had_write.connect(gui_update_process)
        sub_thread2.start()
        # 必须要显示才行, 在执行 show 之前, 进度条处于 hide 状态
        guiMain.progressBar.show()

    guiMain.singal_task_start.connect(task_running)

    def gui_update_process(value, total):
        """
        界面状态更新
        :param value: int
        :param total: int
        """
        process_status = (value/total)*100
        process_status = int(round(process_status, 2))
        guiMain.progressBar.setValue(process_status)
        guiMain.statusBar.showMessage("Writing to the database, please waiting...")
        if process_status == 100:
            guiMain.progressBar.hide()
            guiMain.statusBar.showMessage('log has been written to the database.')
            guiMain.show_db_list()

    def showCellContent(content):
        """
        双击单元格时, 显示单元格中的内容
        :param content: str
        """
        cellgui.showContent(content)
        cellgui.show()
    guiMain.singal_cell_doubleClicked.connect(showCellContent)
    #####################################################################################
    gui.show()
    sys.exit(app.exec_())