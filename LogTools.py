# -*- coding: utf-8 -*-

import os
from PyQt5.Qt import *
from module.gui.LogTools_md import LogApp
from module.gui.Main_md import LogMain
from module.gui.DialogDB_md import DialogDB
from module.gui.CellContent_md import CellContent
from module.tools.LogInsert import LogInsert
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logger
from multiprocessing import Manager, Pool, Process

# 将 queue 中的数据写入到数据库中
def sql_insert(dataqueue, infoqueue):
    try:
        while True:
            sql_write.sqlite_to_database(dataqueue, infoqueue)
    except:
        logger.info('software has be logout!')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    # 多进程部分
    p = Pool()
    dataqueue = Manager().Queue()
    infoqueue = Manager().Queue()
    # 先启动录入数据的子进程, 并且将此进程设置为守护进程
    sub_proc = Process(target=sql_insert, args=(dataqueue, infoqueue,))
    sub_proc.daemon = True
    sub_proc.start()

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
        # 将初始界面获取的产品分类数据传递到 LogTools 主界面里
        guiMain.product_type = [company_name, category_name, product_name]
        # 设置软件标题
        guiMain.setWindowTitle(category_name + ' ' + product_name + ' LogTools ' + 'v0.8.0 Beta')
        # 显示 LogTools 主界面
        guiMain.show()
        # 隐藏 LogTools 初始界面
        gui.hide()
    gui.singal_btn_start.connect(enable_LogMain)

    def enable_DialogDB(company_name, category_name, product_name):
        # 清除上一次的记录
        dbgui.line_dbname.clear()
        dbgui.line_filepath.clear()
        # 将主界面获取的产品分类数据传递到 Select DB 的界面里
        dbgui.product_type = [company_name, category_name, product_name]
        dbgui.show()
    guiMain.singal_btn_import.connect(enable_DialogDB)

    # 日志分析进程: task_info 为字典类型的任务数据
    def log_producer(task_info):
        product_type = task_info.get('product_type')
        file_path = task_info.get('file_path')
        db_name = task_info.get('db_name')
        # 判断产品分类
        try:
            if product_type == 'MicroFocus-ITOM-OA':
                from module.rules.MicroFocus_ITOM_OA_InsertRule import ITOM_OA
                for path in file_path:
                    p.apply_async(ITOM_OA, args=(path, dataqueue, db_name, product_type))

            elif product_type == 'MicroFocus-ITOM-OBM/OMi':
                from module.rules.MicroFocus_ITOM_OBM_InsertRule import ITOM_OBM
                for path in file_path:
                    p.apply_async(ITOM_OBM, args=(path, dataqueue, db_name, product_type))
                # 此处不能写 p.close() 这个代码
                # p.close() 表示关闭 Pool 池, 即不在接收新的任务
                # 如果添加了 p.close(), 那么在接收后续的分析任务时, 就会提示 Pool not running 的异常
        except Exception as e:
            logger.error(e)

    # 更新 GUI 的相关状态
    def guiMain_update(value, now, total):
        proc_bar = int((now/total)*100)
        if proc_bar == 100:
            guiMain.statusBar.showMessage('log has been written to the database.')
            guiMain.progressBar.hide()
            guiMain.show_db_list()
        else:
            guiMain.statusBar.showMessage("Writing to the database, please waiting...")
            guiMain.progressBar.setValue(proc_bar)

    # 双击单元格时, 显示单元格中的内容
    def showCellContent(content):
        cellgui.showContent(content)
        cellgui.show()
    guiMain.singal_cell_doubleClicked.connect(showCellContent)

    # 日志分析线程: 用于完善 task_info 信息的
    def log_import(task_info):
        # 打开进度条
        try:
            guiMain.progressBar.show()
            sub_thread = LogInsert(guiMain, task_info, infoqueue)
            sub_thread.singal_log_task_end.connect(log_producer)
            sub_thread.singal_sql_write.connect(guiMain_update)
            sub_thread.start()
        except Exception as e:
            logger.error(e)
    dbgui.singal_log_task.connect(log_import)
    #####################################################################################
    gui.show()
    sys.exit(app.exec_())