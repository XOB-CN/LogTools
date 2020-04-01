# -*- coding: utf-8 -*-

import re, time

class ITOM_OA():
    '''
    读取日志文件的类, 并将分析日志的结果放到队列中
    '''
    def __init__(self, filepath, dataqueue=None, infoqueue=None):
        print('1-:')
        self.filepath = filepath
        self.dataqueue = dataqueue
        self.infoqueue = infoqueue
        print('2-:', self.filepath, self.dataqueue, self.infoqueue)

        # 如果是 system.xt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('system\.txt', self.filepath, re.IGNORECASE)) > 0:
            self.log_system()

    def log_system(self):
        print('3-:' ,self.filepath, self.dataqueue, self.infoqueue)
        time.sleep(10)
        print('end!')