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
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False

        # 尝试开始读取文件
        try:
            with open(self.filepath, mode='r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    try:
                        log_num += 1
                        isnoblk = True
                        for blkrule in BlackRule:
                            if len(re.findall(blkrule, line, re.IGNORECASE)) > 0:
                                isnoblk = False

                        # 判断日志的开头是否是事件的开始, 如果不是则忽略
                        if isstart == False:
                            if len(re.findall('INFO|WARN|ERROR', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            print(len(line.split('; ')), line.split('; '))
                            if len(line.split('; ')) == 4:
                                log_level = line.split(' - ')[0].split(' ')[2].strip()
                                log_time = (line.split(' - ')[0].split(' ')[0].strip() + ' ' + line.split(' - ')[0].split(' ')[1].strip()).split(',')[0]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_line = str(log_num)
                                heap_used = line.split('; ')[0].split('USED:')[-1].split(',')[0].strip()
                                heap_committed = line.split('; ')[0].split('COMMITTED:')[-1].split(',')[0].strip()
                                heap_max = line.split('; ')[0].split('MAX:')[-1].split(',')[0].strip()
                                heap_free = line.split('; ')[0].split('FREE:')[-1].split(',')[0].strip()
                                non_heap_used = line.split('; ')[1].split('USED:')[-1].split(',')[0].strip()
                                non_heap_committed = line.split('; ')[1].split('COMMITTED:')[-1].split(',')[0].strip()
                                non_heap_max = line.split('; ')[1].split('MAX:')[-1].split(',')[0].strip()
                                non_heap_free = line.split('; ')[1].split('FREE:')[-1].split(',')[0].strip()
                                othermsg = line.split('; ', 2)[-1]
                                print('logtest:', othermsg)
                            else:
                                logger.debug("Skip line {}, Because not match rule".format(str(log_num)))
                    except Exception as e:
                        logger.warn("logline can't be processed:{}".format(e))

                # for data in logdata:
                #     try:
                #         sql_insert = 'INSERT INTO tb_System (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(
                #             data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                #             data.get('logcomp'), data.get('logdetail'))
                #         sqldata.append(sql_insert)
                #     except Exception as e:
                #         logger.warn("Can't generate SQL INSERT INTO statement!")
                #
                # self.dataqueue.put({'db_name': self.db_name,
                #                     'db_type': self.db_type,
                #                     'db_table': 'tb_System',
                #                     'db_data': sqldata, })

        except Exception as reason:
            logger.warn('logfile read error:{}'.format(reason))

if __name__ == '__main__':
    filepath = 'D:\\jvm_statistics.log'
    dataqueue = 'test_queue'
    db_name = 'test_db'
    product_type = 'test_product'
    test = ITOM_OBM(filepath, dataqueue, db_name, product_type)