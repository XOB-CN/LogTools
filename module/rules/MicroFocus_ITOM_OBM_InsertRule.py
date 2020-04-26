# -*- coding: utf-8 -*-

import re
from module.rules.MicroFocus_ITOM_OBM_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logSQLCreate

class ITOM_OBM():
    '''
    读取日志文件的类, 并将分析日志的结果放到队列中
    '''

    SQLData = {}

    def __init__(self, filepath, db_name, product_type):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type

        # 如果是 system.xt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('jvm_statistics\.log|busjvm_statistics\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_jvm_statistics()
        elif len(re.findall('opr-ciresolver\.log|opr-backend\.log|opr-gateway\.log|opr-svcdiscserver\.log|opr-scripting-host\.log|bus\.log|opr-webapp\.log|opr-configserver\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_obm_logfiles_type1()
        elif len(re.findall('opr-svcdiscserver-citrace\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_obm_logfiles_type2()
        elif len(re.findall('downtime\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_obm_logfiles_type3()
        elif len (re.findall('pmi\.log', self.filepath, re.IGNORECASE)) > 0:
            self.log_obm_pmi()

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
                            if len(line.split('; ')) == 4:
                                log_level = line.split(' - ')[0].split(' ')[2].strip()
                                log_time = (line.split(' - ')[0].split(' ')[0].strip() + ' ' + line.split(' - ')[0].split(' ')[1].strip()).replace(',','.')
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_line = str(log_num)
                                heap_used = line.split('; ')[0].split('USED:')[-1].split(',')[0].strip()
                                heap_committed = line.split('; ')[0].split('COMMITTED:')[-1].split(',')[0].strip()
                                heap_max = line.split('; ')[0].split('MAX:')[-1].split(',')[0].strip()
                                heap_free = line.split('; ')[0].split('FREE:')[-1].split(',')[0].strip()[:-1]
                                non_heap_used = line.split('; ')[1].split('USED:')[-1].split(',')[0].strip()
                                non_heap_committed = line.split('; ')[1].split('COMMITTED:')[-1].split(',')[0].strip()
                                non_heap_max = line.split('; ')[1].split('MAX:')[-1].split(',')[0].strip()
                                non_heap_free = line.split('; ')[1].split('FREE:')[-1].split(',')[0].strip()[:-1]
                                othermsg = line.split('; ', 2)[-1]
                                logdata.append({'logfile':self.filepath,
                                                'loglevel':log_level,
                                                'logtime':log_time,
                                                'logline':log_line,
                                                'heap_used':heap_used,
                                                'heap_committed':heap_committed,
                                                'heap_max':heap_max,
                                                'heap_free':heap_free,
                                                'non_heap_used':non_heap_used,
                                                'non_heap_committed':non_heap_committed,
                                                'non_heap_max':non_heap_max,
                                                'non_heap_free':non_heap_free,
                                                'othermsg':othermsg,})
                            else:
                                logSQLCreate.info("logline can't match rule - {}".format(line))
                    except Exception as e:
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO tb_JVMStatus ' \
                                     '(logfile, logline, loglevel, logtime, heap_free_percent, non_heap_free_percent, heap_used, heap_committed, heap_max, heap_free, non_heap_used, non_heap_committed, non_heap_max, non_heap_free, othermsg) VALUES ' \
                                     '("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                                                                                                                  str(round((float(data.get('heap_free'))/float(data.get('heap_max')))*100, 2)),
                                                                                                                  str(round((float(data.get('non_heap_free'))/float(data.get('non_heap_max')))*100, 2)),
                                                                                                                  data.get('heap_used'), data.get('heap_committed'), data.get('heap_max'), data.get('heap_free'),
                                                                                                                  data.get('non_heap_used'), data.get('non_heap_committed'), data.get('non_heap_max'), data.get('non_heap_free'),
                                                                                                                  data.get('othermsg'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! Reason: " + str(e))

                return ({'db_name': self.db_name,
                         'db_type': self.db_type,
                         'db_table': 'tb_JVMStatus',
                         'db_data': sqldata, })

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def log_obm_pmi(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('pmi\.log', self.filepath):
            self.db_table = 'tb_pmi'

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
                            if len(re.findall('INFO |WARN |ERROR |DEBUG', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line)) > 0:
                                log_level = line.split('] ')[1].split(': ')[0].strip()
                                log_time = line.split('[',1)[0].strip()
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']',1)[0].strip()
                                if re.findall(' INFO :', line):
                                    log_detail = line.split(' INFO :', 1)[-1].strip()
                                elif re.findall(' WARN ', line):
                                    log_detail = line.split(' WARN ', 1)[-1].strip()
                                elif re.findall(' ERROR: ', line):
                                    log_detail = line.split(' ERROR: ', 1)[-1].strip()
                                elif re.findall(' DEBUG ', line):
                                    log_detail = line.split(' DEBUG ', 1)[-1].strip()
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
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! " + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def log_obm_logfiles_type1(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('bus\.log', self.filepath):
            self.db_table = 'tb_bus'
        elif re.findall('opr-ciresolver\.log', self.filepath):
            self.db_table = 'tb_opr_ciresolver'
        elif re.findall('opr-backend\.log', self.filepath):
            self.db_table = 'tb_opr_backend'
        elif re.findall('opr-gateway\.log', self.filepath):
            self.db_table = 'tb_opr_gateway'
        elif re.findall('opr-svcdiscserver\.log', self.filepath):
            self.db_table = 'tb_opr_svcdiscserver'
        elif re.findall('opr-scripting-host\.log', self.filepath):
            self.db_table = 'tb_opr_scripting_host'
        elif re.findall('opr-webapp\.log', self.filepath):
            self.db_table = 'tb_opr_webapp'
        elif re.findall('opr-configserver\.log', self.filepath):
            self.db_table = 'tb_opr_configserver'

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
                            if len(re.findall('INFO |WARN |ERROR |DEBUG', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line)) > 0:
                                log_level = line.split('] ')[1].split(' ')[0].strip()
                                log_time = line.split(' ',2)[0] + ' ' + line.split(' ',2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']',1)[0].strip()
                                if re.findall(' INFO ', line):
                                    log_detail = line.split(' INFO ', 1)[-1].strip()
                                elif re.findall(' WARN ', line):
                                    log_detail = line.split(' WARN ', 1)[-1].strip()
                                elif re.findall(' ERROR ', line):
                                    log_detail = line.split(' ERROR ', 1)[-1].strip()
                                elif re.findall(' DEBUG ', line):
                                    log_detail = line.split(' DEBUG ', 1)[-1].strip()
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
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warnning("Can't generate SQL INSERT INTO statement! Reason: " + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def log_obm_logfiles_type2(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('opr-svcdiscserver-citrace\.log', self.filepath):
            self.db_table = 'tb_opr_svcdiscserver_citrace'

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
                            if len(re.findall('INFO |WARN |ERROR |DEBUG', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*-', line)) > 0:
                                log_level = line.split(' ',3)[2].strip()
                                log_time = line.split(' ', 2)[0] + ' ' + line.split(' ', 2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('-', 3)[-1].split(':', 1)[0].strip()
                                log_detail = line.split(' - ', 1)[-1].split(': ',1)[-1].strip()
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
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(
                            self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warnning("Can't generate SQL INSERT INTO statement!" + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def log_obm_logfiles_type3(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('downtime\.log', self.filepath):
            self.db_table = 'tb_downtime'

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
                            if len(re.findall('INFO |WARN |ERROR |DEBUG', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line)) > 0:
                                log_level = line.split(') ')[1].split(' - ')[0].strip()
                                log_time = line.split(' ',2)[0] + ' ' + line.split(' ',2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']',1)[0].strip()
                                if re.findall(' INFO ', line):
                                    log_detail = line.split(' INFO ', 1)[-1].strip()
                                elif re.findall(' WARN ', line):
                                    log_detail = line.split(' WARN ', 1)[-1].strip()
                                elif re.findall(' ERROR ', line):
                                    log_detail = line.split(' ERROR ', 1)[-1].strip()
                                elif re.findall(' DEBUG ', line):
                                    log_detail = line.split(' DEBUG ', 1)[-1].strip()
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
                        logSQLCreate.warning("line:{}\nSource:{}\nException:{}".format(str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warnning("Can't generate SQL INSERT INTO statement!" + str(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': self.db_table,
                                 'db_data': sqldata, })

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

if __name__ == '__main__':
    pass
    # filepath = 'D:\\demo\pmi.log'
    # dataqueue = 'test_queue'
    # db_name = 'test_db'
    # product_type = 'test_product'
    # test = ITOM_OBM(filepath, dataqueue, db_name, product_type)