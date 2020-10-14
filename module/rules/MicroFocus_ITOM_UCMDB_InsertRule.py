# -*- coding: utf-8 -*-

import re, pickle, os
from module.rules.MicroFocus_ITOM_UCMDB_FileRule import BlackRule
from module.tools.SQLTools import sql_write, sql_string
from module.tools.LogRecord import logSQLCreate

class ITOM_UCMDB():
    """
        读取日志文件的类, 并将分析日志的结果放到队列中
        """
    SQLData = {}

    def __init__(self, filepath, db_name, product_type, fileid=None):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type
        self.file_id = str(fileid)

        # 如果是 error.log 文件, 则调用此方法
        if re.findall('error\.log', self.filepath, re.IGNORECASE):
            self.log_error()
        elif re.findall('cmdb\.reconciliation\.identification\.log|cmdb\.reconciliation\.datain\.merged\.log|cmdb\.reconciliation\.datain\.ignored\.log', self.filepath, re.IGNORECASE):
            self.log_ucmdb_logfiles_type1()

    def log_error(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('error\.log', self.filepath):
            self.db_table = 'log_error'

        # 尝试开始读取文件
        try:
            with open(self.filepath, mode='r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    try:
                        log_num += 1
                        isnoblk = True
                        for blkrule in BlackRule:
                            if re.findall(blkrule, line, re.IGNORECASE):
                                isnoblk = False

                        # 判断日志的开头是否是事件的开始, 如果不是则忽略
                        if isstart == False:
                            if re.findall('\d{4}-\d{2}-\d{2}.*INFO |\d{4}-\d{2}-\d{2}.*WARN |\d{4}-\d{2}-\d{2}.*ERROR |\d{4}-\d{2}-\d{2}.*DEBUG ', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*', line):
                                log_level = line.split(' ')[3].strip()
                                log_time = line.split(' ', 2)[0] + ' ' + line.split(' ', 2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']', 1)[0].strip()
                                log_detail = line.split('(:) -')[-1].strip()
                                logdata.append({'logfile': self.filepath,
                                                'logline': log_num,
                                                'loglevel': log_level,
                                                'logtime': log_time,
                                                'logcomp': log_comp,
                                                'logdetail': log_detail})
                            else:
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'] + '\n' + line
                                # 抹掉日志中剩下的 '/n'
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'].strip()

                    except Exception as e:
                        logSQLCreate.warning(
                            "[log_ucmdb_logfiles_type1] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,
                                                                                                        str(log_num),
                                                                                                        line, e))

                for data in logdata:
                    try:
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(
                            self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning(
                            "[log_ucmdb_logfiles_type1] Can't generate SQL INSERT INTO statement!" + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('[log_ucmdb_logfiles_type1] logfile read error:{}'.format(reason))
            # print(reason)

    def log_ucmdb_logfiles_type1(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('cmdb\.reconciliation\.identification\.log', self.filepath):
            self.db_table = 'log_ucmdb_identification'
        elif re.findall('cmdb\.reconciliation\.datain\.merged\.log', self.filepath):
            self.db_table = 'log_ucmdb_merged'
        elif re.findall('cmdb\.reconciliation\.datain\.ignored\.log', self.filepath):
            self.db_table = 'log_ucmdb_ignored'

        # 尝试开始读取文件
        try:
            with open(self.filepath, mode='r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    try:
                        log_num += 1
                        isnoblk = True
                        for blkrule in BlackRule:
                            if re.findall(blkrule, line, re.IGNORECASE):
                                isnoblk = False

                        # 判断日志的开头是否是事件的开始, 如果不是则忽略
                        if isstart == False:
                            if re.findall(' INFO | WARN | ERROR | DEBUG ', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line):
                                log_level = line.split(' ')[3].strip()
                                log_time = line.split(' ', 2)[0] + ' ' + line.split(' ', 2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']', 1)[0].strip()
                                log_detail = '[' + line.split('[', 2)[-1]
                                logdata.append({'logfile': self.filepath,
                                                'logline': log_num,
                                                'loglevel': log_level,
                                                'logtime': log_time,
                                                'logcomp': log_comp,
                                                'logdetail': log_detail})
                            else:
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'] + '\n' + line
                                # 抹掉日志中剩下的 '/n'
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'].strip()

                    except Exception as e:
                        logSQLCreate.warning(
                            "[log_ucmdb_logfiles_type1] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,
                                                                                                        str(log_num),
                                                                                                        line, e))

                for data in logdata:
                    try:
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(
                            self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning(
                            "[log_ucmdb_logfiles_type1] Can't generate SQL INSERT INTO statement!" + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('[log_ucmdb_logfiles_type1] logfile read error:{}'.format(reason))
            # print(reason)