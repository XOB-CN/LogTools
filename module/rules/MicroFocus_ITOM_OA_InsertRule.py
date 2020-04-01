# -*- coding: utf-8 -*-

import re
from module.rules.MicroFocus_ITOM_OA_FileRule import BlackRule

class ITOM_OA():
    '''
    读取日志文件的类, 并将分析日志的结果放到队列中
    '''
    def __init__(self, filepath, dataqueue, infoqueue):
        self.filepath = filepath
        self.dataqueue = dataqueue
        self.infoqueue = infoqueue

        # 如果是 system.xt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('system\.txt', self.filepath, re.IGNORECASE)) > 0:
            self.log_system()

    def log_system(self):
        # 初始化数据和相关控制参数
        logdata = {}
        isnoblk = True

        # 尝试开始读取文件
        try:
            with open(self.filepath, mode='r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    isnoblk = True
                    for blkrule in BlackRule:
                        if len(re.findall(blkrule, line, re.IGNORECASE)) > 0:
                            isnoblk = False

                    if isnoblk:
                        print(line.strip())



                    pass
        except Exception as reason:
            print(reason)