# -*- coding: utf-8 -*-

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