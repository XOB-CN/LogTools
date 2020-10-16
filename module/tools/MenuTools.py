# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.tools.SettingsTools import ConfigTools

class AddMenuTools():
    """
    针对不同的产品, 在 guiMain 上的 Tools 下面增加不同的选项
    """
    def __init__(self, product_name, guiMain):
        self.procuct_name = product_name
        self.guiMain = guiMain

        # SQL comment
        self.sql_comment = ConfigTools.get_sql_comment()

        # MicroFocus ITOM OBM/OMi
        if self.procuct_name == 'OBM/OMi':
            self.set_mf_itom_obm_menu()

        if self.procuct_name == 'UCMDB':
            self.set_mf_itom_ucmdb_menu()

        # Help Menu (Last one)
        self.set_help_menu()

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
        menu_obm_boot = menu.addAction('OBM Boot')
        menu_ci_resolver = menu.addAction('CI Resolver')
        menu_all_event = menu.addAction('All Event Processing')
        menu_epi = menu.addAction('Event Processing Interface')
        menu_pd = menu.addAction('Performance Dashboard')
        menu_ma = menu.addAction('Monitoring Automation')
        menu_rtsm = menu.addAction('RTSM')

        def select_obm_boot():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            sqltext_mid = ''
            if tblist != False:
                # 判断 OBM boot 具体包含哪张表
                for key in ['log_odb_boot',
                            'log_wde_boot',
                            'log_businessImpact_service_boot',
                            'log_marble_supervisor_boot',
                            'log_opr_scripting_host_boot',
                            'log_opr_backend_boot',
                            'log_bus_boot',
                            'log_jboss7_boot',
                            'log_schedulergw_boot',]:
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
                    QMessageBox.information(self.guiMain, 'No Data!', 'No OBM boot logs')
        # 链接 select_obm_boot 槽函数
        menu_obm_boot.triggered.connect(select_obm_boot)

        def select_ci_resolver():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            sqltext_mid = ''
            if tblist != False:
                # 判断 CI Resolver 具体包含哪张表
                for key in ['log_opr_ciresolver', 'log_opr_backend', 'log_error']:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[
                                                        :-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                                                                          "order by logtime desc;\n" \
                                                                          "{}".format(
                            self.guiMain.geTime.text().replace('/', '-'),
                            self.guiMain.leTime.text().replace('/', '-'), self.sql_comment)

                        sqledit.setText(sqltext)
                elif len(kylist) == 2:
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
                            'log_wde_all',
                            'log_error',]:
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
            sqltext_mid = ''
            if tblist != False:
                # 判断 Event Processing Interface 具体包含哪张表
                for key in ['log_opr_gateway',
                            'log_opr_gateway_flowtrace',
                            'log_opr_event_sync_adapter',
                            'log_opr_backend',
                            'log_opr_flowtrace_backend',
                            'log_opr_scripting_host',
                            'log_scripts',
                            'log_error',]:
                    if key in tblist:
                        kylist.append(key)
                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[
                                                        :-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                                                                          "order by logtime desc;\n" \
                                                                          "{}".format(
                            self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'),
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
            sqltext_mid = ''
            if tblist != False:
                # 判断 Monitoring Automation 具体包含哪张表
                for key in ['log_opr_webapp', 'log_opr_configserver', 'log_MI_MonitorAdministration', 'log_error',]:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[
                                                        :-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                                                                          "order by logtime desc;\n" \
                                                                          "{}".format(
                            self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'),
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
            sqltext_mid = ''
            if tblist != False:
                # 判断 RTSM 具体包含哪张表
                for key in ['log_rtsm_identification', 'log_rtsm_merged', 'log_rtsm_ignored', 'log_error',]:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[
                                                        :-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                                                                          "order by logtime desc;\n" \
                                                                          "{}".format(
                            self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'),
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

    def set_mf_itom_ucmdb_menu(self):
        menu = self.guiMain.menubar.addMenu('Tools')
        menu_ucmdb = menu.addAction('UCMDB Common1')

        def select_common1():
            kylist = []
            tblist = self._active_db_tables()
            sqledit = self._active_sqledit()
            sqltext_mid = ''
            if tblist != False:
                # 判断 UCMDB 具体包含哪张表
                for key in ['log_cmdb_reconciliation_identification',
                            'log_cmdb_reconciliation_datain_merged',
                            'log_cmdb_reconciliation_datain_ignored',
                            'log_error',]:
                    if key in tblist:
                        kylist.append(key)

                if len(kylist) >= 2:
                    for tb_name in kylist:
                        if sqltext_mid == '':
                            sqltext_mid = "select * from {} union all\n".format(tb_name)
                        else:
                            sqltext_mid = sqltext_mid + "select * from {} union all\n".format(tb_name)

                        sqltext = "select * from (\n" + sqltext_mid[
                                                        :-11] + '\n)\n' + "where logtime > '{}' and logtime < '{}'\n" \
                                                                          "order by logtime desc;\n" \
                                                                          "{}".format(
                            self.guiMain.geTime.text().replace('/', '-'), self.guiMain.leTime.text().replace('/', '-'),
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
                    QMessageBox.information(self.guiMain, 'No Data!', 'No UCMDB Information!')
        # 连接 select_common1 槽函数
        menu_ucmdb.triggered.connect(select_common1)

    def set_help_menu(self):
        menu = self.guiMain.menubar.addMenu('Help')
        menu.addAction('About Qt')

        def menu_help_about_qt():
            QMessageBox.aboutQt(self.guiMain)
        # 连接 About Qt 槽函数
        menu.triggered.connect(menu_help_about_qt)
