# -*- coding: utf-8 -*-

from datetime import datetime

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

# 测试代码
if __name__ == '__main__':
    time = sql_write.sqlite_to_datetime('Thu Aug 29 10:20:30 2019')