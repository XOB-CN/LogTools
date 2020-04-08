# -*- coding: utf-8 -*-

import os
from PyQt5.Qt import *
from PyQt5 import QtSql
from module.gui.Main_ui import Ui_MainWindow

class LogMain(QMainWindow, Ui_MainWindow):
    """
    LogTools Main class
    """
    num_new_query = 1
    singal_btn_import = pyqtSignal(str, str, str)

    # 接收产品分类
    product_type = []

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setupUi(self)

        # 设置初始的小于时间，即当前时间
        self.leTime.setDateTime(QDateTime.currentDateTime())
        # 设置初始的大于时间，即当前时间 - 30day
        self.geTime.setDateTime(QDateTime.addDays(QDateTime.currentDateTime(), -30))

        # 隐藏/初始化进度条
        self.progressBar.setValue(0)
        self.progressBar.hide()

        # 判断数据目录是否存在, 如果不存在, 则创建该目录
        if os.path.exists('./data') == False:
            os.mkdir('./data')

        # 加载 QTreeWidget 中的内容，仅仅是测试用途
        self.show_db_list()

    # 针对 QTreeWidget 的操作
    def show_db_list(self):
        # 获取数据库目录下的信息
        dbfiles = os.listdir('./data')
        if dbfiles != []:
            dbinfo = {}
            for dbfile in dbfiles:
                db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                path = os.path.join('./data', dbfile)
                db.setDatabaseName(path)
                db.open()
                dbinfo[dbfile] = db.tables()
                db.close()

            # 循环展示数据库列表信息
            for db,tbs in dbinfo.items():
                root = QTreeWidgetItem(self.treeList)
                # 去掉数据库文件最后的三个字符 (.db)
                root.setText(0, db[:-3])
                for tb in tbs:
                    sub_item = QTreeWidgetItem(root)
                    sub_item.setText(0, tb)

    # 创建新的 Table 标签
    def slot_new_query(self):
        # 新建的 Tab 名字
        self.num_new_query += 1
        tablabel = 'Tab' + str(self.num_new_query)
        tlaylout = 'Layout' + str(self.num_new_query)
        textedit = 'sqlEdit' + str(self.num_new_query)

        # 生成 QWidget 以及 QTextEdit 中的内容
        self.tab_page = QWidget()
        self.tab_page.setObjectName(tablabel)
        self.tab_layout = QGridLayout(self.tab_page)
        self.tab_layout.setObjectName(tlaylout)
        self.tab_text = QTextEdit(self.tab_page)
        self.tab_text.setObjectName(textedit)
        self.tab_layout.addWidget(self.tab_text, 0, 0, 1, 1)

        # 将生成的 QWidget 中的内容追加到 QTabWidget 中
        self.tabQuery.addTab(self.tab_page, tablabel)
        self.tabQuery.setObjectName(tablabel)
        self.tabQuery.setCurrentIndex(self.tabQuery.count() - 1)

    def slot_run_sql_query(self):
        # sqlEdit 返回的是当前激活的 QTextEdit 对象
        sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
        sql_str = sqlEdit.toPlainText()
        # 判断获取的内容
        if len(sql_str) == 0:
            print('no input anything')
        else:
            print('****** execute sql query ******')
            print(sql_str)

    # SQL Query Tab 关闭函数
    def slot_tab_sql_close(self, index):
        self.tabQuery.removeTab(index)

    # 读取日志文件
    def slot_action_import(self):
        # 发射一个自定义信号，信号内容包括 "厂商" + "分类" + "产品"
        self.singal_btn_import.emit(self.product_type[0], self.product_type[1], self.product_type[2])