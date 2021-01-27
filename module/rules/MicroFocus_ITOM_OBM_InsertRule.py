# -*- coding: utf-8 -*-

import re, pickle, os
from module.rules.MicroFocus_ITOM_OBM_FileRule import BlackRule
from module.tools.SQLTools import sql_write, sql_string
from module.tools.LogRecord import logSQLCreate

class ITOM_OBM():
    """
    读取日志文件的类, 并将分析日志的结果放到队列中
    """
    SQLData = {}

    def __init__(self, filepath, db_name, product_type, fileid = None):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type
        self.file_id = str(fileid)

        # 如果是 jvm 的统计信息类型的日志, 则调用 log_jvm_statistivs 方法
        if re.findall('jvm_statistics\.log|busjvm_statistics\.log', self.filepath, re.IGNORECASE):
            self.log_jvm_statistics()
        elif re.findall('opr-ciresolver\.log|opr-backend\.log|opr-gateway\.log|opr-svcdiscserver\.log|opr-scripting-host\.log|scripts\.log|bus\.log|opr-webapp\.log|opr-configserver\.log|opr-heartbeat\.log', self.filepath, re.IGNORECASE):
            self.log_obm_logfiles_type1()
        elif re.findall('opr-svcdiscserver-citrace\.log', self.filepath, re.IGNORECASE):
            self.log_obm_logfiles_type2()
        elif re.findall('downtime\.log|wde\.all\.log|notification-service\.log|nanny_all\.log|server_deployer\.log', self.filepath, re.IGNORECASE):
            self.log_obm_logfiles_type3()
        elif re.findall('cmdb\.reconciliation\.identification\.log|cmdb\.reconciliation\.datain\.merged\.log|cmdb\.reconciliation\.datain\.ignored\.log', self.filepath, re.IGNORECASE):
            self.log_obm_logfiles_type4()
        elif re.findall('jboss7_boot\.log|opr-backend_boot\.log|opr-scripting-host_boot\.log|marble_supervisor_boot\.log|businessImpact_service_boot\.log|wde_boot\.log|schedulergw_boot\.log|odb_boot\.log|bus_boot\.log', self.filepath, re.IGNORECASE):
            self.log_obm_logfiles_type5()
        elif re.findall('pmi\.log', self.filepath, re.IGNORECASE):
            self.log_obm_pmi()
        elif re.findall('MI_MonitorAdministration\.log', self.filepath):
            self.log_obm_MI_MonitorAdministration()
        elif re.findall('opr-checker-xml\.txt', self.filepath, re.IGNORECASE):
            self.cfg_obminfo_xml()
        elif re.findall('opr-checker\.txt', self.filepath, re.IGNORECASE):
            self.cfg_obminfo_txt()
        elif re.findall('error\.log', self.filepath, re.IGNORECASE):
            self.log_rtsm_logfiles_type1()

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
                            if re.findall(blkrule, line, re.IGNORECASE):
                                isnoblk = False

                        # 判断日志的开头是否是事件的开始, 如果不是则忽略
                        if isstart == False:
                            if re.findall('INFO|WARN|ERROR', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('INFO.*HEAP.*\[USAGE.*FREE.*TOTAL.*MAX.*\].*PERM.*\[USAGE.*FREE.*MAX.*\]|INFO.*HEAP.*\[USAGE.*FREE.*TOTAL.*MAX.*\].*NON-HEAP.*\[USAGE.*FREE.*MAX.*\]', line):
                                log_level = line.split(' - ')[0].split(' ')[2].strip()
                                if log_level == '':
                                    log_level = line.split(' - ')[0].split('[')[0].strip().split(' ')[-1]
                                log_time = (line.split(' - ')[0].split(' ')[0].strip() + ' ' + line.split(' - ')[0].split(' ')[1].strip()).replace(',', '.')
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_line = str(log_num)
                                heap_usage = line.split('; ')[0].split('USAGE:')[-1].split(',')[0].strip()
                                heap_free = line.split('; ')[0].split('FREE:')[-1].split(',')[0].strip()
                                heap_total = line.split('; ')[0].split('TOTAL:')[-1].split(',')[0].strip()
                                heap_max = line.split('; ')[0].split('MAX:')[-1].split(',')[0].strip()[:-1]
                                perm_usage = line.split('; ')[1].split('USAGE:')[-1].split(',')[0].strip()
                                perm_free = line.split('; ')[1].split('FREE:')[-1].split(',')[0].strip()
                                perm_max = line.split('; ')[1].split('MAX:')[-1].split(',')[0].strip()[:-1]
                                othermsg = line.split('; ', 2)[-1]
                                logdata.append({'logfile':self.filepath,
                                                'loglevel':log_level,
                                                'logtime':log_time,
                                                'logline':log_line,
                                                'heap_used':heap_usage,
                                                'heap_committed':heap_total,
                                                'heap_max':heap_max,
                                                'heap_free':heap_free,
                                                'non_heap_used':perm_usage,
                                                'non_heap_committed':'Null',
                                                'non_heap_max':perm_max,
                                                'non_heap_free':perm_free,
                                                'othermsg':othermsg,})

                            elif re.findall('INFO.*HEAP.*\[USAGE.*FREE.*MAX.*\].*NON-HEAP.*\[USAGE.*FREE.*MAX.*\]', line):
                                log_level = line.split(' - ')[0].split(' ')[2].strip()
                                log_time = (line.split(' - ')[0].split(' ')[0].strip() + ' ' + line.split(' - ')[0].split(' ')[1].strip()).replace(',', '.')
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_line = str(log_num)
                                heap_usage = line.split('; ')[0].split('USAGE:')[-1].split(',')[0].strip()
                                heap_free = line.split('; ')[0].split('FREE:')[-1].split(',')[0].strip()
                                heap_max = line.split('; ')[0].split('MAX:')[-1].split(',')[0].strip()[:-1]
                                non_heap_usage = line.split('; ')[1].split('USAGE:')[-1].split(',')[0].strip()
                                non_heap_free = line.split('; ')[1].split('FREE:')[-1].split(',')[0].strip()
                                non_heap_max = line.split('; ')[1].split('MAX:')[-1].split(',')[0].strip()[:-1]
                                othermsg = line.split('; ', 2)[-1]
                                logdata.append({'logfile':self.filepath,
                                                'loglevel':log_level,
                                                'logtime':log_time,
                                                'logline':log_line,
                                                'heap_used':heap_usage,
                                                'heap_committed':'Null',
                                                'heap_max':heap_max,
                                                'heap_free':heap_free,
                                                'non_heap_used':non_heap_usage,
                                                'non_heap_committed':'Null',
                                                'non_heap_max':non_heap_max,
                                                'non_heap_free':non_heap_free,
                                                'othermsg':othermsg,})

                            elif len(line.split('; ')) == 4:
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
                                logSQLCreate.info("file:{}\nlogline can't match rule - {}".format(self.filepath, line))
                    except Exception as e:
                        logSQLCreate.warning("[log_jvm_statistics] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO log_JVMStatus ' \
                                     '(logfile, logline, loglevel, logtime, heap_free_percent, non_heap_free_percent, heap_used, heap_committed, heap_max, heap_free, non_heap_used, non_heap_committed, non_heap_max, non_heap_free, othermsg) VALUES ' \
                                     '("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                                                                                                                  str(round((float(data.get('heap_free'))/float(data.get('heap_max')))*100, 2)),
                                                                                                                  str(round((1.0 - float(data.get('non_heap_used'))/float(data.get('non_heap_max')))*100, 2)),
                                                                                                                  data.get('heap_used'), data.get('heap_committed'), data.get('heap_max'), data.get('heap_free'),
                                                                                                                  data.get('non_heap_used'), data.get('non_heap_committed'), data.get('non_heap_max'), data.get('non_heap_free'),
                                                                                                                  data.get('othermsg'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_jvm_statistics] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': 'log_JVMStatus',
                                 'db_data': sqldata, })

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('[log_jvm_statistics] logfile read error:{}'.format(reason))

    def log_obm_pmi(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('pmi\.log', self.filepath):
            self.db_table = 'log_pmi'

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
                            if re.findall('INFO |WARN |ERROR |DEBUG', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line):
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
                        logSQLCreate.warning("[log_obm_pmi] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_obm_pmi] Can't generate SQL INSERT INTO statement! " + str(e))

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
            logSQLCreate.error('[log_obm_pmi] logfile read error:{}'.format(reason))

    def log_obm_MI_MonitorAdministration(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('MI_MonitorAdministration\.log', self.filepath):
            self.db_table = 'log_MI_MonitorAdministration'

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
                            if re.findall('INFO |WARN |ERROR |DEBUG', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line):
                                log_level = line.split(' ', 5)[4].strip()
                                log_time = line.split('[',1)[0].strip()
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split(' ', 4)[2].strip() + line.split(' ', 4)[3].strip()
                                if re.findall(' INFO -', line):
                                    log_detail = line.split(' INFO -', 1)[-1].strip()
                                elif re.findall(' WARN -', line):
                                    log_detail = line.split(' WARN -', 1)[-1].strip()
                                elif re.findall(' ERROR -', line):
                                    log_detail = line.split(' ERROR -', 1)[-1].strip()
                                elif re.findall(' DEBUG -', line):
                                    log_detail = line.split(' DEBUG -', 1)[-1].strip()
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
                        logSQLCreate.warning("[log_obm_MI_MonitorAdministration] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_obm_MI_MonitorAdministration] Can't generate SQL INSERT INTO statement! " + str(e))

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
            logSQLCreate.error('[log_obm_MI_MonitorAdministration] logfile read error:{}'.format(reason))

    def log_obm_logfiles_type1(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('bus\.log', self.filepath):
            self.db_table = 'log_bus'
        elif re.findall('opr-ciresolver\.log', self.filepath):
            self.db_table = 'log_opr_ciresolver'
        elif re.findall('opr-backend\.log', self.filepath):
            self.db_table = 'log_opr_backend'
        elif re.findall('opr-gateway\.log', self.filepath):
            self.db_table = 'log_opr_gateway'
        elif re.findall('opr-svcdiscserver\.log', self.filepath):
            self.db_table = 'log_opr_svcdiscserver'
        elif re.findall('opr-scripting-host\.log', self.filepath):
            self.db_table = 'log_opr_scripting_host'
        elif re.findall('scripts\.log', self.filepath):
            self.db_table = 'log_scripts'
        elif re.findall('opr-webapp\.log', self.filepath):
            self.db_table = 'log_opr_webapp'
        elif re.findall('opr-configserver\.log', self.filepath):
            self.db_table = 'log_opr_configserver'
        elif re.findall('opr-heartbeat\.log', self.filepath):
            self.db_table = 'log_opr_heartbeat'

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
                            if re.findall('INFO |WARN |ERROR |DEBUG', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line):
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
                        logSQLCreate.warning("[log_obm_logfiles_type1] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_obm_logfiles_type1] Can't generate SQL INSERT INTO statement! Reason: " + str(e))

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
            logSQLCreate.error('[log_obm_logfiles_type1] logfile read error:{}'.format(reason))

    def log_obm_logfiles_type2(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('opr-svcdiscserver-citrace\.log', self.filepath):
            self.db_table = 'log_opr_svcdiscserver_citrace'

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
                            if re.findall('INFO |WARN |ERROR |DEBUG', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*-', line):
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
                        logSQLCreate.warning("[log_obm_logfiles_type2] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

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
                        logSQLCreate.warning("[log_obm_logfiles_type2] Can't generate SQL INSERT INTO statement!" + str(e))

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
            logSQLCreate.error('[log_obm_logfiles_type2] logfile read error:{}'.format(reason))

    def log_obm_logfiles_type3(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('downtime\.log', self.filepath):
            self.db_table = 'log_downtime'
        elif re.findall('wde\.all\.log', self.filepath):
            self.db_table = 'log_wde_all'
        elif re.findall('notification-service\.log', self.filepath):
            self.db_table = 'log_notification_service'
        elif re.findall('nanny_all\.log', self.filepath):
            self.db_table = 'log_nanny_all'
        elif re.findall('server_deployer\.log', self.filepath):
            self.db_table = 'log_server_deployer'

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
                            if re.findall('INFO |WARN |ERROR |DEBUG', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*\[.*\]', line):
                                log_level = line.split(') ')[1].split(' - ')[0].strip()
                                log_time = line.split(' ',2)[0] + ' ' + line.split(' ',2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = '[' + line.split('[', 1)[1].split(')',1)[0].strip() + ')'
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
                        logSQLCreate.warning("[log_obm_logfiles_type3] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_obm_logfiles_type3] Can't generate SQL INSERT INTO statement!" + str(e))

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
            logSQLCreate.error('[log_obm_logfiles_type3] logfile read error:{}'.format(reason))

    def log_obm_logfiles_type4(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = False
        # db_table 名字
        if re.findall('cmdb\.reconciliation\.identification\.log', self.filepath):
            self.db_table = 'log_rtsm_identification'
        elif re.findall('cmdb\.reconciliation\.datain\.merged\.log', self.filepath):
            self.db_table = 'log_rtsm_merged'
        elif re.findall('cmdb\.reconciliation\.datain\.ignored\.log', self.filepath):
            self.db_table = 'log_rtsm_ignored'

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
                                log_time = line.split(' ',2)[0] + ' ' + line.split(' ',2)[1]
                                log_time = sql_write.sqlite_to_datetime(log_time)
                                log_comp = line.split('[', 1)[1].split(']',1)[0].strip()
                                log_detail = '[' + line.split('[',2)[-1]
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
                        logSQLCreate.warning("[log_obm_logfiles_type4] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num), line, e))

                for data in logdata:
                    try:
                        data['logcomp'] = sql_string.sqlite_to_string(data.get('logcomp'))
                        data['logdetail'] = sql_string.sqlite_to_string(data.get('logdetail'))
                        sql_insert = 'INSERT INTO {} (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(self.db_table,
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("[log_obm_logfiles_type4] Can't generate SQL INSERT INTO statement!" + str(e))

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
            logSQLCreate.error('[log_obm_logfiles_type4] logfile read error:{}'.format(reason))
            # print(reason)

    def log_obm_logfiles_type5(self):
        # 初始化数据和相关控制参数
        logdata = []
        sqldata = []
        isnoblk = True
        log_num = 0
        isstart = True
        str_muline = False
        # end_muline = False
        # db_table 名字
        if re.findall('jboss7_boot\.log', self.filepath):
            self.db_table = 'log_jboss7_boot'
        elif re.findall('opr-backend_boot\.log', self.filepath):
            self.db_table = 'log_opr_backend_boot'
        elif re.findall('opr-scripting-host_boot\.log', self.filepath):
            self.db_table = 'log_opr_scripting_host_boot'
        elif re.findall('marble_supervisor_boot\.log', self.filepath):
            self.db_table = 'log_marble_supervisor_boot'
        elif re.findall('businessImpact_service_boot\.log', self.filepath):
            self.db_table = 'log_businessImpact_service_boot'
        elif re.findall('wde_boot\.log', self.filepath):
            self.db_table = 'log_wde_boot'
        elif re.findall('schedulergw_boot\.log', self.filepath):
            self.db_table = 'log_schedulergw_boot'
        elif re.findall('odb_boot\.log', self.filepath):
            self.db_table = 'log_odb_boot'
        elif re.findall('bus_boot\.log', self.filepath):
            self.db_table = 'log_bus_boot'

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
                        # 特殊判断, 如果该行内容仅为 "2019-04-16 14:55:32,973 - " 这样的, 也不匹配
                        if len(line.strip()) == 25:
                            isnoblk = False

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 提前设置此项, 如果后续没有修改, 则此值是默认值
                            log_comp = "Logs"
                            # 如果不是多行匹配, 则进入单行匹配
                            # if str_muline == False:
                            #     if re.findall("-\s+===================================| at ", line):
                            #         str_muline = True

                            # 如果是"- at " 开头的
                            if re.findall("-\s+at ", line, re.IGNORECASE):
                                str_muline = True
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'] + '\n' + line
                                # 抹掉日志中剩下的 '/n'
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'].strip()

                            # 如果不是 "- at " 这部分内容, 则按照单行模式处理
                            elif re.findall("-XX:\+|Bootstrap Environment|Date:|ServerType:|Physical Memory:|Java:|Jvm Opts:|FIPS_Mode:|ClassPath:|MainClass:|Args:|HPBSM\\\\supervisor\\\\wrapper>.*\s+.*|HPBSM\\\\bin>.*|-\s+.*msec|Creating DB object:", line, re.IGNORECASE):
                                log_level = "INFO"
                                log_comp = "Config"
                                str_muline = False
                            elif re.findall("error|fail|can't|Exception|notfound|Caused by|Dumping", line, re.IGNORECASE):
                                log_level = "ERROR"
                                str_muline = False
                            elif re.findall("warn", line, re.IGNORECASE):
                                log_level = "WARN"
                                str_muline = False
                            else:
                                log_level = "INFO"
                                str_muline = False
                            log_time = line[:23]
                            log_time = sql_write.sqlite_to_datetime(log_time)
                            log_detail = line

                            if str_muline == False:
                                logdata.append({'logfile': self.filepath,
                                                'logline': log_num,
                                                'loglevel': log_level,
                                                'logtime': log_time,
                                                'logcomp': log_comp,
                                                'logdetail': log_detail})

                    except Exception as e:
                        logSQLCreate.warning(
                            "[log_obm_logfiles_type5] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,
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
                            "[log_obm_logfiles_type5] Can't generate SQL INSERT INTO statement!" + str(e))

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
            logSQLCreate.error('[log_obm_logfiles_type4] logfile read error:{}'.format(reason))
            # print(reason)

    def log_rtsm_logfiles_type1(self):
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
                            "[log_rtsm_logfiles_type1] file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,
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
                            "[log_rtsm_logfiles_type1] Can't generate SQL INSERT INTO statement!" + str(e))

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
            logSQLCreate.error('[log_rtsm_logfiles_type1] logfile read error:{}'.format(reason))
            # print(reason)

    def cfg_obminfo_xml(self):
        """
        针对 MicroFocus ITOM OBM 中的 opr-checker-xml.txt 的文件
        """
        # 初始化数据和相关控制参数
        logdata = {}
        sqldata = []
        # 预设变量
        os_hostname = 'Null'
        os_memory = 'Null'
        obm_version = 'Null'
        # 读取指定文本, 并筛选出指定的内容
        with open(self.filepath, 'r', encoding='utf-8', errors='replace') as f:
            opr_checker = f.readlines()
        # 循环匹配相关内容
        try:
            for line in opr_checker:
                # 针对 os_hostname 的处理
                if re.findall('<hostname>.*?</hostname>', line):
                    if os_hostname == 'Null':
                        os_hostname = line.strip()[len('<hostname>'):-(len('</hostname>'))]
                    elif len(line.strip()[len('<hostname>'):-(len('</hostname>'))]) > len(os_hostname):
                        os_hostname = line.strip()[len('<hostname>'):-(len('</hostname>'))]
                # 针对 os_memory 的处理
                elif re.findall('<memsize>.*?</memsize>|<physical_memory>.*</physical_memory>', line):
                    if os_memory == 'Null':
                        if re.findall('<memsize>.*?</memsize>', line):
                            os_memory = line.strip()[len('<memsize>'):-(len('</memsize>'))]
                        elif re.findall('<physical_memory>.*</physical_memory>', line):
                            os_memory = line.strip()[len('<physical_memory>'):-(len('</physical_memory>'))]
                    elif len(line.strip()[len('<memsize>'):-(len('</memsize>'))]) > len(os_memory):
                        if re.findall('<memsize>.*?</memsize>', line):
                            os_memory = line.strip()[len('<memsize>'):-(len('</memsize>'))]
                        elif re.findall('<physical_memory>.*</physical_memory>', line):
                            os_memory = line.strip()[len('<physical_memory>'):-(len('</physical_memory>'))]
                # 针对 obm_version 的处理
                elif re.findall('<opr_baseversion>.*?</opr_baseversion>', line):
                    obm_version = line.strip()[len('<opr_baseversion>'):-(len('</opr_baseversion>'))]

            # 整理数据
            logdata['os_hostname'] = os_hostname
            logdata['os_memory'] = os_memory
            logdata['obm_version'] = obm_version

            for k, v in logdata.items():
                try:
                    sql_insert = 'INSERT INTO cfg_OBMInfo (attribute, value) VALUES ("{}", "{}");'.format(k, v)
                    sqldata.append(sql_insert)
                except Exception as e:
                    logSQLCreate.warning("[cfg_obminfo_xml] Can't generate SQL INSERT INTO statement! - {}".format(e))

            self.SQLData = ({'db_name': self.db_name,
                             'db_type': self.db_type,
                             'db_table': 'cfg_OBMInfo',
                             'db_data': sqldata, })

            # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
            datafilepath = r'./temp/{}'.format(self.file_id)
            open('{}.lck'.format(datafilepath), 'w').close()
            with open(datafilepath, 'wb') as f:
                pickle.dump(self.SQLData, f)
            os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('[cfg_obminfo_xml] logfile read error:{}'.format(reason))

    def cfg_obminfo_txt(self):
        """
        针对 MicroFocus ITOM OBM 中的 opr-checker.txt 的文件
        """
        # 初始化数据和相关控制参数
        logdata = {}
        sqldata = []
        # 判断获取数据的开始和结束以及数据本身
        vm_params = 'Null'
        str_vm_params = False
        end_vm_params = False
        jms_bus = 'Null'
        str_jms_bus = False
        end_jms_bus = False
        # 读取指定文本, 并筛选出指定的内容
        with open(self.filepath, 'r', encoding='utf-8', errors='replace') as f:
            opr_checker = f.readlines()
        # 循环匹配相关内容
        try:
            for line in opr_checker:
                # 开始匹配 vm_params
                #### [vm_params] ##################################################
                if 'vm_params' in line and str_vm_params == False:
                    str_vm_params = True
                    vm_params = line
                # 已经匹配 vm_params
                elif str_vm_params == True and end_vm_params == False:
                    # 结束匹配 vm_params
                    if '_________________________________________________' in line:
                        str_vm_params = False
                        end_vm_params = True
                        # 将完整的数据保持到 logdata 中
                        logdata['vm_params'] = vm_params
                    else:
                        vm_params = vm_params + line
                #### [jms_bus] #####################################################
                if 'JMS_Bus' in line and str_jms_bus == False:
                    str_jms_bus = True
                    jms_bus = line
                # 已经匹配 jms_bus
                elif str_jms_bus == True and end_jms_bus == False:
                    # 结束匹配 jms_bus
                    if '_________________________________________________' in line:
                        str_jms_bus = False
                        end_jms_bus = True
                        # 将完整的数据保持到 logdata 中
                        logdata['jms_bus'] = jms_bus
                    else:
                        jms_bus = jms_bus + line
                ###################################################################

            for k, v in logdata.items():
                try:
                    sql_insert = 'INSERT INTO cfg_OBMInfo (attribute, value) VALUES ("{}", "{}");'.format(k, sql_string.sqlite_to_string(v))
                    sqldata.append(sql_insert)
                except Exception as e:
                    logSQLCreate.warning("[cfg_obminfo_txt] Can't generate SQL INSERT INTO statement! - {}".format(e))

            self.SQLData = ({'db_name': self.db_name,
                             'db_type': self.db_type,
                             'db_table': 'cfg_OBMInfo',
                             'db_data': sqldata, })

            # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
            datafilepath = r'./temp/{}'.format(self.file_id)
            open('{}.lck'.format(datafilepath), 'w').close()
            with open(datafilepath, 'wb') as f:
                pickle.dump(self.SQLData, f)
            os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('[cfg_obminfo_txt] logfile read error:{}'.format(reason))

if __name__ == '__main__':
    pass
    # filepath = 'D:\\MI_MonitorAdministration.log'
    # db_name = 'test_db'
    # product_type = 'test_product'
    # test = ITOM_OBM(filepath, db_name, product_type)