# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5 import QtSql
from module.tools.LogRecord import logSQLInsert

class sql_write():
    """
    数据库写入类
    """
    @staticmethod
    def sqlite_to_datetime(date):
        """
        转换接收的时间字符串, 返回符合 sqlite 存储的时间字符串
        :param date: str
        :return: str(datetime)
        """
        datetime_format = [
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S,%f',
            "%a %b %d %H:%M:%S %Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%y/%m/%d %H:%M:%S",
            "%Y %b %d %H:%M:%S",
            "%d-%b-%Y %H:%M:%S",
        ]

        for time_format in datetime_format:
            try:
                datetime_str = datetime.strptime(date, time_format)
                if time_format == '%Y-%m-%d %H:%M:%S.%f':
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                elif time_format == '%Y-%m-%d %H:%M:%S,%f':
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                else:
                    return datetime_str.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
        return str('Null')

    @staticmethod
    def sqlite_to_database(logdata):
        """
        将获取的数据写入到 sqlite 数据库中
        """
        try:
            sqldata = logdata
            db_name = sqldata.get('db_name')
            db_file = '.\\data\\' + db_name + '.db'
            db_type = sqldata.get('db_type')
            db_table = sqldata.get('db_table')
            db_data = sqldata.get('db_data')

            # 使用 Qt 内嵌的 QSqlite 驱动来建立 Sqlite 数据库
            db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(db_file)
            # 使数据库处于打开状态
            db.open()
            # 开启事务
            db.transaction()

            # 判断是否需要建立相应的表
            if db_type == 'MicroFocus-ITOM-OA':
                if db_table not in db.tables():
                    if db_table == 'log_System':
                        query = QtSql.QSqlQuery()
                        # 不自动增长的语句
                        query.exec_("create table log_System (logfile TEXT, logline INT, loglevel TEXT, logtime TEXT, logcomp TEXT, logdetail TEXT);")
                        if query.lastError().isValid():
                            logSQLInsert.error('MicroFocus-ITOM-OA:\n{}'.format(query.lastError().text()))

                    if db_table == 'cfg_Policy':
                        query = QtSql.QSqlQuery()
                        # 不自动增长的语句
                        query.exec_("create table cfg_Policy (ply_name TEXT, ply_version TEXT, ply_status TEXT, ply_type TEXT, ply_data TEXT, ply_param TEXT);")
                        if query.lastError().isValid():
                            logSQLInsert.error('MicroFocus-ITOM-OA:\n{}'.format(query.lastError().text()))

            elif db_type == 'MicroFocus-ITOM-OBM/OMi':
                if db_table not in db.tables():
                    if db_table == 'log_JVMStatus':
                        query = QtSql.QSqlQuery()
                        query.exec_("create table log_JVMStatus (logfile TEXT, logline INT, loglevel TEXT, logtime TEXT, heap_free_percent INT, non_heap_free_percent INT, heap_used INT, heap_committed INT, heap_max INT, heap_free INT, non_heap_used INT, non_heap_committed INT, non_heap_max INT, non_heap_free INT, othermsg TEXT);")
                        if query.lastError().isValid():
                            logSQLInsert.error('MicroFocus-ITOM-OBM/OMi:\n{}'.format(query.lastError().text()))

                    elif db_table in ['log_bus',
                                      'log_downtime',
                                      'log_opr_backend',
                                      'log_opr_ciresolver',
                                      'log_opr_configserver',
                                      'log_opr_gateway',
                                      'log_opr_scripting_host',
                                      'log_opr_svcdiscserver',
                                      'log_opr_svcdiscserver_citrace',
                                      'log_opr_webapp',
                                      'log_pmi',
                                      'log_scripts',
                                      'log_rtsm_identification',
                                      'log_rtsm_merged',
                                      'log_rtsm_ignored',]:
                        query = QtSql.QSqlQuery()
                        query.exec_("create table {} (logfile TEXT, logline INT, loglevel TEXT, logtime TEXT, logcomp TEXT, logdetail TEXT);".format(db_table))
                        if query.lastError().isValid():
                            logSQLInsert.error('MicroFocus-ITOM-OBM/OMi:\n{}'.format(query.lastError().text()))

        except Exception as e:
            logSQLInsert.error('Step1:{}'.format(e))

        try:
            # 将获取的数据写入到指定的表中
            insert = QtSql.QSqlQuery()
            for sql in db_data:
                insert.exec_(sql)
                if insert.lastError().isValid():
                    logSQLInsert.error('Insert fail:\nSource SQL:\n{}\nResult:\n{}'.format(sql, insert.lastError().text()))
            # 结束事务
            db.commit()
            # db.close()
        except Exception as e:
            logSQLInsert.error('Step2:{}'.format(e))

# 测试代码
if __name__ == '__main__':
    pass