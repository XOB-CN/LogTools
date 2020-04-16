# -*- coding: utf-8 -*-

import re
from module.rules.MicroFocus_ITOM_OBM_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logger

class ITOM_OBM():
    '''
    读取日志文件的类, 并将分析日志的结果放到队列中
    '''
    def __init__(self, filepath, dataqueue, db_name, product_type):
        self.filepath = filepath
        self.dataqueue = dataqueue
        self.db_name = db_name
        self.db_type = product_type

        # 如果是 system.xt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('jvm_statistics\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_jvm_statistics()

    def log_jvm_statistics(self):
        pass