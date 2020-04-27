# -*- coding: utf-8 -*-

import re
from module.rules.MicroFocus_ITOM_OA_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logSQLCreate

class ITOM_OA():
    '''
    读取日志文件的类, 并返回分析的数据
    '''
    SQLData = {}

    def __init__(self, filepath, db_name, product_type):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type

        # 如果是 system.xt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('system\.txt', self.filepath, re.IGNORECASE)) > 0:
            self.log_system()

    def log_system(self):
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
                            if len(re.findall('INF:|WRN:|ERR:', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(line.split(': ',4)) > 4:
                                log_level = line.split(': ',4)[1].strip()
                                log_time = sql_write.sqlite_to_datetime(line.split(': ',4)[2].strip())
                                log_comp = line.split(': ',4)[3].strip()
                                log_detail = line.split(': ',4)[4].strip()
                                logdata.append({'logfile':self.filepath,
                                                'logline':log_num,
                                                'loglevel':log_level,
                                                'logtime':log_time,
                                                'logcomp':log_comp,
                                                'logdetail':log_detail})
                            else:
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'] + '\n' + line
                                # 抹掉日志中剩下的 '/n'
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'].strip()
                    except Exception as e:
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num),line,e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO tb_System (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(data.get('logfile'), str(data.get('logline')),data.get('loglevel'),data.get('logtime'),data.get('logcomp'),data.get('logdetail').replace('"',"'"))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! - {}".format(e))

                self.SQLData = ({'db_name':self.db_name,
                                 'db_type':self.db_type,
                                 'db_table':'tb_System',
                                 'db_data':sqldata,})

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))