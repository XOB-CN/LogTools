# -*- coding: utf-8 -*-

from PyQt5.Qt import *

class AddMenuTools():
    """
    针对不同的产品, 在 guiMain 上的 Tools 下面增加不同的选项
    """
    def __init__(self, product_name, guiMain):
        self.procuct_name = product_name
        self.guiMain = guiMain

        # SQL comment
        self.sql_comment = "\n-- Common SQL filter parameters\n    " \
                           "-- where <column> [not] like '%keyword%' / '_keyword_' --> like no case sensitive\n    " \
                           "-- where <column> [not] glob '*keyword*' / '?keyword?' --> glob it's case sensitive\n    " \
                           "-- select aggregate_function <column> …… group by <column> --> aggregate_function like sum(), total(), count()"

        # MicroFocus ITOM OBM/OMi
        if self.procuct_name == 'OBM/OMi':
            self.set_mf_itom_obm_menu()

    # 返回当前激活的 sqledit 对象
    def _active_sqledit(self):
        sqlEdit = self.guiMain.tabQuery.currentWidget().findChild(QTextEdit)
        return sqlEdit

    # 返回当前选中的数据库中的表信息
    def _active_db_tables(self):
        tb_list = []
        try:
            # 如果选择的是表, 则按照下列代码返来返回
            db_obj = self.guiMain.treeList.currentItem().parent()
            for num in range(db_obj.childCount()):
                tb_list.append(db_obj.child(num).text(0))
            return tb_list
        except:
            try:
                # 如果选择的是数据库, 则按照下列代码来返回
                db_obj = self.guiMain.treeList.currentItem()
                for num in range(db_obj.childCount()):
                    tb_list.append(db_obj.child(num).text(0))
                return tb_list
            except Exception as e:
                QMessageBox.information(self.guiMain, 'Not select!', 'Database or Table not select!')
                return False

    def set_mf_itom_obm_menu(self):
        menu = self.guiMain.menubar.addMenu('Tools')
        menu_ci_resolver = menu.addAction('CI Resolver')
        menu_all_event = menu.addAction('All Event Processing')
        menu_epi = menu.addAction('Event Processing Interface')
        menu_pd = menu.addAction('Performance Dashboard')
        menu_ma = menu.addAction('Monitoring Automation')
        menu_rtsm = menu.addAction('RTSM')

        def select_ci_resolver():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            if tblist != False:
                # 判断 CI Resolver 具体包含哪张表
                for key in ['log_opr_ciresolver', 'log_opr_backend']:
                    if key in tblist:
                        kylist.append(key)
                if len(kylist) == 2:
                    sqltext = "select * from (\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0], kylist[1], self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'), self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0], self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'), self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No CI Resolver Information!')
        # 连接 select_ci_resolver 槽函数
        menu_ci_resolver.triggered.connect(select_ci_resolver)

        def select_all_event():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            sqltext_mid = ''
            if tblist != False:
                # 判断 All Event Processing 具体包含哪张表
                for key in ['log_opr_webapp',
                            'log_opr_gateway',
                            'log_opr_gateway_flowtrace',
                            'log_opr_event_sync_adapter',
                            'log_bus',
                            'log_opr_backend',
                            'log_opr_flowtrace_backend',
                            'log_opr_scripting_host',
                            'log_scripts',
                            'log_wde_all',]:
                    if key in tblist:
                        kylist.append(key)

                # 如果超过2个, 则按照此格式生成SQL查询语句
                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[:-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'), self.sql_comment)

                        sqledit.setText(sqltext)

                elif len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0], self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'), self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No All Event Processing Data!')
        # 连接 select_all_event 槽函数
        menu_all_event.triggered.connect(select_all_event)

        def select_epi():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            if tblist != False:
                # 判断 Event Processing Interface 具体包含哪张表
                for key in ['log_opr_gateway', 'log_opr_gateway_flowtrace', 'log_opr_event_sync_adapter', 'log_opr_backend', 'log_opr_flowtrace_backend', 'log_opr_scripting_host', 'log_scripts',]:
                    if key in tblist:
                        kylist.append(key)
                if len(kylist) == 7:
                    sqltext = "select * from (\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          kylist[3],
                                          kylist[4],
                                          kylist[5],
                                          kylist[6],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 6:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          kylist[3],
                                          kylist[4],
                                          kylist[5],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 5:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          kylist[3],
                                          kylist[4],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 4:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          kylist[3],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 3:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 2:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No Event EPI(Event Processing Interface) Information!')
        # 连接 select_epi 槽函数
        menu_epi.triggered.connect(select_epi)

        def select_pd():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            if tblist != False:
                # 判断 Performance Dashboard 具体包含哪张表
                for key in ['log_pmi', ]:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No Performance Dashboard Information!')
        # 连接 select_pd 槽函数
        menu_pd.triggered.connect(select_pd)

        def select_ma():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            if tblist != False:
                # 判断 Monitoring Automation 具体包含哪张表
                for key in ['log_opr_webapp', 'log_opr_configserver', 'log_MI_MonitorAdministration']:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) == 3:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 2:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No Monitoring Automation Information!')
        # 连接 select_ma 槽函数
        menu_ma.triggered.connect(select_ma)

        def select_rtsm():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            if tblist != False:
                # 判断 RTSM 具体包含哪张表
                for key in ['log_rtsm_identification', 'log_rtsm_merged', 'log_rtsm_ignored']:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) == 3:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          kylist[2],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 2:
                    sqltext = "select * from (\n"\
                              "select * from {} union all\n" \
                              "select * from {}\n)\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          kylist[1],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                elif len(kylist) == 1:
                    sqltext = "select * from {}\n" \
                              "where logtime > '{}' and logtime < '{}'\n" \
                              "order by logtime desc;\n" \
                              "{}".format(kylist[0],
                                          self.guiMain.geTime.text().replace('/', '-'),
                                          self.guiMain.leTime.text().replace('/', '-'),
                                          self.sql_comment)
                    sqledit.setText(sqltext)
                else:
                    QMessageBox.information(self.guiMain, 'No Data!', 'No RTSM Information!')
        # 连接 select_rtsm 槽函数
        menu_rtsm.triggered.connect(select_rtsm)