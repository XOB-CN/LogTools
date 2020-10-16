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
        elif re.findall('cmdb', self.filepath, re.IGNORECASE):
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
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
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
        if re.findall('cmdb\.reconciliation\.identification', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_identification'
        elif re.findall('cmdb\.reconciliation\.datain\.merged', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_datain_merged'
        elif re.findall('cmdb\.reconciliation\.datain\.ignored', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_datain_ignored'
        elif re.findall('cmdb\.api\.audit\.detailed\.unformatted', self.filepath):
            self.db_table = 'log_cmdb_api_audit_detailed_unformatted'
        elif re.findall('cmdb\.api\.audit\.detailed', self.filepath):
            self.db_table = 'log_cmdb_api_audit_detailed'
        elif re.findall('cmdb\.authentication\.audit', self.filepath):
            self.db_table = 'log_cmdb_authentication_audit'
        elif re.findall('cmdb\.browser\.resources', self.filepath):
            self.db_table = 'log_cmdb_browser_resources'
        elif re.findall('cmdb\.classmodel\.audit\.detailed', self.filepath):
            self.db_table = 'log_cmdb_classmodel_audit_detailed'
        elif re.findall('cmdb\.classmodel\.audit\.short', self.filepath):
            self.db_table = 'log_cmdb_classmodel_audit_short'
        elif re.findall('cmdb\.dal\.server', self.filepath):
            self.db_table = 'log_cmdb_dal_server'
        elif re.findall('cmdb\.dal', self.filepath):
            self.db_table = 'log_cmdb_dal'
        elif re.findall('cmdb\.dal\.slow', self.filepath):
            self.db_table = 'log_cmdb_dal_slow'
        elif re.findall('cmdb\.enrichment', self.filepath):
            self.db_table = 'log_cmdb_enrichment'
        elif re.findall('cmdb\.ha\.detailed', self.filepath):
            self.db_table = 'log_cmdb_ha_detailed'
        elif re.findall('cmdb\.ha', self.filepath):
            self.db_table = 'log_cmdb_ha'
        elif re.findall('cmdb\.model\.aging', self.filepath):
            self.db_table = 'log_cmdb_model_aging'
        elif re.findall('cmdb\.model\.audit\.short', self.filepath):
            self.db_table = 'log_cmdb_model_audit_short'
        elif re.findall('cmdb\.model\.notification', self.filepath):
            self.db_table = 'log_cmdb_model_notification'
        elif re.findall('cmdb\.model\.topology', self.filepath):
            self.db_table = 'log_cmdb_model_topology'
        elif re.findall('cmdb\.monitor', self.filepath):
            self.db_table = 'log_cmdb_monitor'
        elif re.findall('cmdb\.notification', self.filepath):
            self.db_table = 'log_cmdb_notification'
        elif re.findall('cmdb\.operation', self.filepath):
            self.db_table = 'log_cmdb_operation'
        elif re.findall('cmdb\.pattern\.statistics', self.filepath):
            self.db_table = 'log_cmdb_pattern_statistics'
        elif re.findall('cmdb\.quota', self.filepath):
            self.db_table = 'log_cmdb_quota'
        elif re.findall('cmdb\.reconciliation\.analyzer', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_analyzer'
        elif re.findall('cmdb\.reconciliation\.audit', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_audit'
        elif re.findall('cmdb\.reconciliation\.config', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_config'
        elif re.findall('cmdb\.reconciliation\.error', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_error'
        elif re.findall('cmdb\.reconciliation\.queries', self.filepath):
            self.db_table = 'log_cmdb_reconciliation_queries'
        elif re.findall('cmdb\.reconciliation', self.filepath):
            self.db_table = 'log_cmdb_reconciliation'
        elif re.findall('cmdb\.samlAuthentication', self.filepath):
            self.db_table = 'log_cmdb_samlAuthentication'
        elif re.findall('cmdb\.tql\.calculation\.audit', self.filepath):
            self.db_table = 'log_cmdb_tql_calculation_audit'
        elif re.findall('cmdb\.tql\.resultcache', self.filepath):
            self.db_table = 'log_cmdb_tql_resultcache'
        elif re.findall('cmdb\.tql\.tracker', self.filepath):
            self.db_table = 'log_cmdb_tql_tracker'
        elif re.findall('fcmdb\.adapters\.HistoryDataSource', self.filepath):
            self.db_table = 'log_fcmdb_adapters_HistoryDataSource'
        elif re.findall('fcmdb\.config\.audit', self.filepath):
            self.db_table = 'log_fcmdb_config_audit'
        elif re.findall('fcmdb\.ftql\.audit', self.filepath):
            self.db_table = 'log_fcmdb_ftql_audit'
        elif re.findall('fcmdb', self.filepath):
            self.db_table = 'log_fcmdb'

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
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
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