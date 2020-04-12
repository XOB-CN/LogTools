# -*- coding: utf-8 -*-

from datetime import datetime
from PyQt5 import QtSql

class sql_write():
    '''
    数据库写入类
    '''
    @staticmethod
    def sqlite_to_datetime(date):
        '''
        转换接收的时间字符串, 返回符合 sqlite 存储的时间字符串
        :param date: str
        :return: str(datetime)
        '''
        datetime_format = [
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
                return datetime_str.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass

        return str('Null')

    @staticmethod
    def sqlite_to_database(dataqueue, infoqueue):
        '''
        将获取的数据写入到 sqlite 数据库中
        :param dataqueue:
        :param infoqueue:
        :return:
        '''
        sqldata = dataqueue.get()
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
                if db_table == 'tb_System':
                    query = QtSql.QSqlQuery()
                    # 带自动增长的语句
                    # query.exec_("create table tb_System (id INTEGER PRIMARY KEY, logfile TEXT, logline INT, loglevel TEXT, logtime TEXT, logcomp TEXT, logdetail TEXT);")
                    # 不自动增长的语句
                    query.exec_("create table tb_System (logfile TEXT, logline INT, loglevel TEXT, logtime TEXT, logcomp TEXT, logdetail TEXT);")

        try:
            # 将获取的数据写入到指定的表中
            insert = QtSql.QSqlQuery()
            for sql in db_data:
                insert.exec_(sql)
            # 结束事务
            db.commit()

            infoqueue.put(0)
        except:
            infoqueue.put(1)

# 测试代码
if __name__ == '__main__':
    pass