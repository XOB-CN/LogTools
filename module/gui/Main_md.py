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
    num_new_result = 1
    singal_btn_import = pyqtSignal(str, str, str)
    query_db_file = ''

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

        # 加载 QTreeWidget 中的内容
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
        tablabel = 'SQL_Query_' + str(self.num_new_query)
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

    # 执行查询语句, 并且返回结果
    def slot_run_sql_query(self):
        # 获取 sqlEdit 上一级的对象名
        sqltitle = self.tabQuery.currentWidget().objectName()
        # sqlEdit 返回的是当前激活的 QTextEdit 对象
        sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
        sql_str = sqlEdit.toPlainText()

        # 判断获取的内容
        if len(sql_str) == 0:
            print('no input anything')
        else:
            print('****** execute sql query ******')
            print('查询语句是：',sql_str)
            print('当前数据库：', self.query_db_file)
            if self.query_db_file != '':
                qrydb = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                qrydb.setDatabaseName(self.query_db_file)
                qrydb.open()

                model = QSqlQueryModel()
                model.setQuery(sql_str, db=qrydb)
                if model.lastError().isValid():
                    print(model.lastError().text())

        # 生成 QtableView 对象:self.tab_view ########################
        self.num_new_result += 1
        tablabel = sqltitle.replace('Query','Result')
        tlaylout = 'LayResult' + str(self.num_new_result)
        sql_rest = 'sqlResult' + str(self.num_new_result)
        # 生成 QWidget 以及 QtableView 中的内容
        self.tab_page_result = QWidget()
        self.tab_page_result.setObjectName(tablabel)
        self.tab_layout_result = QGridLayout(self.tab_page_result)
        self.tab_layout_result.setObjectName(tlaylout)
        self.tab_view = QTableView(self.tab_page_result)
        self.tab_view.setObjectName(sql_rest)
        self.tab_layout_result.addWidget(self.tab_view, 0, 0, 1, 1)
        # 将生成的 QWidget 中的内容追加到 QTabWidget 中
        self.tabResult.addTab(self.tab_page_result, tablabel)
        self.tabResult.setObjectName(tablabel)
        self.tabResult.setCurrentIndex(self.tabResult.count() - 1)
        ##############################################################

        self.tab_view.setModel(model)
        self.tab_view.show()

    # 选中 dblist 的表时, 设定选中的数据库文件
    def slot_dblist_sql_query(self):
        try:
            # 选中表时
            self.query_db_file = os.path.join('.\\data', self.treeList.currentItem().parent().text(0) +'.db')
            # 在 QTextEdit 中添加默认的 sql 语句 (sqlEdit 返回的是当前激活的 QTextEdit 对象)
            sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
            sqlEdit.setText('select * from {};'.format(self.treeList.currentItem().text(0)))
        except:
            # 选中数据库时
            self.query_db_file = os.path.join('.\\data', self.treeList.currentItem().text(0) +'.db')

    # SQL Query Tab 关闭函数
    def slot_tab_sql_close(self, index):
        self.tabQuery.removeTab(index)

    # SQL Result Tab 关闭函数
    def slot_tab_result_close(self, index):
        self.tabResult.removeTab(index)

    # 读取日志文件
    def slot_action_import(self):
        # 发射一个自定义信号，信号内容包括 "厂商" + "分类" + "产品"
        self.singal_btn_import.emit(self.product_type[0], self.product_type[1], self.product_type[2])