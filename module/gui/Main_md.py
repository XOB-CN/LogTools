# -*- coding: utf-8 -*-

import os, shutil
from PyQt5.Qt import *
from PyQt5 import QtSql
from module.gui.Main_ui import Ui_MainWindow
from module.tools.SQLHighLight import SQLHighLighter
from module.tools.LogRecord import logSQLQuery
from module.tools.LogRecord import loglogTools

class LogMain(QMainWindow, Ui_MainWindow):
    """
    LogTools 主界面 class
    """

    # 准备查询的数据库文件路径
    query_db_file = ''
    # 准备删除的数据库文件路径
    rmove_db_file = ''
    # Query Tab 的数字编号
    num_new_query = 1
    # Query Tab 对应结果的编号
    num_new_result = 1
    # 点击 import 时发射信号
    singal_btn_import = pyqtSignal(str, str, str)
    # 双击表的单元格时发射信号
    singal_cell_doubleClicked = pyqtSignal(str)
    # 启动日志分析任务的信号
    singal_task_start = pyqtSignal(dict)
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

        # SQL comment
        self.sql_comment = "\n-- Common WHERE filter parameters\n    " \
                           "-- <column> like '%keyword%' / '_keyword_' --> like no case sensitive\n    " \
                           "-- <column> glob '*keyword*' / '?keyword?' --> glob it's case sensitive"

        # 判断数据目录是否存在, 如果不存在, 则创建该目录
        if os.path.exists('./data') == False:
            os.mkdir('./data')

        # 重新建立临时目录
        if os.path.exists('./temp') == False:
            os.mkdir('./temp')
        else:
            shutil.rmtree('./temp', ignore_errors=True)
            os.mkdir('./temp')

        # 加载 QTreeWidget 中的内容
        self.show_db_list()

        # 设置高亮部分
        self.highlight = SQLHighLighter(self.sqlEdit1.document())

    def show_db_list(self):
        """
        展示/刷新 QTreeWidget 中的 items
        """
        # 获取数据库目录下的信息
        dbfiles = os.listdir('./data')
        if dbfiles != []:
            dbinfo = {}
            for dbfile in dbfiles:
                db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                path = os.path.join('./data', dbfile)
                db.setDatabaseName(path)
                db.open()
                dbinfo[dbfile] = (sorted(db.tables()))
                db.close()

            # 清除原先的所有内容
            self.treeList.clear()

            # 循环展示数据库列表信息
            for db,tbs in dbinfo.items():
                root = QTreeWidgetItem(self.treeList)
                # 去掉数据库文件最后的三个字符 (.db)
                root.setText(0, db[:-3])
                for tb in tbs:
                    sub_item = QTreeWidgetItem(root)
                    sub_item.setText(0, tb)
        else:
            # 此处为删除数据库时调用, 如果删除的是最后一个数据库, 则列表返回为空
            self.treeList.clear()

    def slot_new_query(self):
        """
        槽函数：创建新的 Table 标签
        """
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

    def slot_show_cell(self, cell):
        """
        槽函数：展示双击选中时, 发射单元格中的内容信号
        :param cell: 单元格对象
        """
        # cell.data() 的结果需要使用 str 转换一下, 否则如果是纯数字的话会出错
        self.singal_cell_doubleClicked.emit(str(cell.data()))

    def slot_run_sql_query(self):
        """
        槽函数：执行查询语句, 并且返回结果
        """
        # 获取 sqlEdit 上一级的对象名
        sqltitle = self.tabQuery.currentWidget().objectName()
        # sqlEdit 返回的是当前激活的 QTextEdit 对象
        sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
        sql_str = sqlEdit.toPlainText()

        # 判断获取的内容
        if len(sql_str) == 0:
            pass
        else:
            if self.query_db_file != '':
                qrydb = QtSql.QSqlDatabase.addDatabase('QSQLITE')
                qrydb.setDatabaseName(self.query_db_file)
                qrydb.open()

                model = QSqlQueryModel()
                # 这里截取第一个分号之前的内容, 因为该方法仅能执行单一的 SQL 语句, 不支持多条语句
                model.setQuery(sql_str.split(';')[0] + ';', db=qrydb)
                if model.lastError().isValid():
                    logSQLQuery.warning(model.lastError().text())
                    QMessageBox.warning(self, 'SQL Error', model.lastError().text())
                else:
                    #
                    logSQLQuery.info(sql_str)

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
                # 优化表格显示
                ## 水平方向标签拓展剩下的窗口部分
                self.tab_view.horizontalHeader().setStretchLastSection(True)
                # self.tab_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                ## 设置单元格默认的行高
                self.tab_view.verticalHeader().setDefaultSectionSize(8)
                ## 设置单元格显示的字体
                self.tab_view.setFont(QFont('Microsoft YaHei UI', 8, QFont.Normal))
                ## 自动调整每列的宽度
                self.tab_view.resizeColumnsToContents()
                ## 连接槽函数, 在双击单元格时触发
                self.tab_view.doubleClicked.connect(self.slot_show_cell)
                self.tab_view.show()
                ##############################################################
                qrydb.close()

    def slot_dblist_sql_query(self):
        """
        槽函数：选中 dblist 的表时, 设定选中的数据库文件, 并且自动生成 SQL 查询语句
        """
        try:
            # 选中表时
            self.query_db_file = os.path.join('.\\data', self.treeList.currentItem().parent().text(0) +'.db')
            # 在 QTextEdit 中添加默认的 sql 语句 (sqlEdit 返回的是当前激活的 QTextEdit 对象)
            sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
            getime = self.geTime.text().replace('/', '-')
            letime = self.leTime.text().replace('/', '-')
            sqlEdit.clear()
            # 如果表名为 cfg_OAInfo, 则生成特殊的 SQL 语句
            if self.treeList.currentItem().text(0) == 'cfg_OAInfo':
                sqlEdit.setText("select * from cfg_OAInfo;\n{}".format(self.sql_comment))
            # 如果表名为 cfg_Policy, 则生成特殊的 SQL 语句
            elif self.treeList.currentItem().text(0) == 'cfg_Policy':
                sqlEdit.setText("select * from cfg_Policy\norder by ply_name;\n{}".format(self.sql_comment))
            else:
                sqlEdit.setText("select * from {}\nwhere logtime > '{}' and logtime < '{}'\norder by logtime desc;\n{}".format(self.treeList.currentItem().text(0), getime, letime, self.sql_comment))
            self.statusBar.showMessage("Table [{}] has been selected".format(self.treeList.currentItem().text(0)))
        except:
            # 选中数据库时
            self.query_db_file = os.path.join('.\\data', self.treeList.currentItem().text(0) +'.db')
            self.statusBar.showMessage("DB [{}] has been selected".format(self.treeList.currentItem().text(0)))

    def slot_tab_sql_close(self, index):
        """
        槽函数：SQL Query Tab 关闭函数
        :param index: QtabWidget 的 index
        """
        self.tabQuery.removeTab(index)

    def slot_tab_result_close(self, index):
        """
        槽函数：SQL Result Tab 关闭函数
        :param index: QtabWidget 的 index
        """
        self.tabResult.removeTab(index)

    def slot_sql_highlight(self):
        """
        槽函数：设置 QTextEdit 的高亮
        """
        sqlEdit = self.tabQuery.currentWidget().findChild(QTextEdit)
        self.highlight = SQLHighLighter(sqlEdit.document())

    def slot_action_import(self):
        """
        槽函数：读取日志文件的按钮
        """
        # 发射一个自定义信号，信号内容包括 "厂商" + "分类" + "产品"
        self.singal_btn_import.emit(self.product_type[0], self.product_type[1], self.product_type[2])

    def slot_action_delete(self):
        """
        槽函数：删除指定的 SQLite 数据库
        """
        if self.rmove_db_file != '':
            try:
                os.remove(self.rmove_db_file)
                self.show_db_list()
            except Exception as e:
                loglogTools.warning(str(e))
                self.show_db_list()

    def slot_set_remove_db_file(self):
        """
        槽函数：设定需要删除数据库的文件
        """
        try:
            self.rmove_db_file = os.path.join('.\\data', self.treeList.currentItem().parent().text(0) +'.db')
        except:
            self.rmove_db_file = os.path.join('.\\data', self.treeList.currentItem().text(0) +'.db')

    def log_insert(self, taskdata):
        """
        将指定的日志文件进行分析并写入到数据库
        :param taskdata: dict
        """
        self.singal_task_start.emit(taskdata)