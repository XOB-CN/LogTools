# -*- coding: utf-8 -*-

import re, os, pickle
from xml.etree import ElementTree as ET
from module.rules.MicroFocus_ITOM_OA_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logSQLCreate

class ITOM_MP_SQLServer():
    """
    读取日志文件的类, 并返回分析的数据
    """
    SQLData = {}

    def __init__(self, filepath, db_name, product_type, fileid = None):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type
        self.file_id = str(fileid)

        # 如果是 system.txt 文件, 则调用 log_system 方法读取日志
        if re.findall('[^_]trace$', self.filepath, re.IGNORECASE):
            self.log_trace()

    def log_trace(self):
        """
        针对 MicroFocus ITOM MP for Microsoft SQL Server 中的 trace 文件
        """
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
                            if len(re.findall('\d{4}-\d+-\d+ \d+:\d+:\d+.\d{3}|\d{4}-\d+-\d+T\d+:\d+:\d+.\d{3}', line)) > 0:
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(re.findall('\d{4}-\d+-\d+ \d+:\d+:\d+.\d{3}', line)) > 0:
                                if re.findall('fail|error|deny|refused|exception', line, re.IGNORECASE):
                                    log_level = 'ERROR'
                                else:
                                    log_level = 'INFO'
                                log_time = sql_write.sqlite_to_datetime(line.split(' ', 2)[0] + ' ' + line.split(' ', 2)[1])
                                log_comp = line.split(' ', 2)[-1].split(': ', 1)[0].strip()
                                log_detail = line.split(' ', 2)[-1].split(':', 1)[1].strip()

                                logdata.append({'logfile':self.filepath,
                                                'logline':log_num,
                                                'loglevel':log_level,
                                                'logtime':log_time,
                                                'logcomp':log_comp,
                                                'logdetail':log_detail})

                            elif len(re.findall('\d{4}-\d+-\d+T\d+:\d+:\d+.\d{3}', line)) > 0:
                                if re.findall('fail|error|deny|refused|exception', line, re.IGNORECASE):
                                    log_level = 'ERROR'
                                else:
                                    log_level = 'INFO'
                                log_time = sql_write.sqlite_to_datetime(line.split(' ', 2)[0])
                                log_comp = line.split(' ', 1)[-1].split(': ', 1)[0].strip()
                                log_detail = line.split(' ', 1)[-1].split(':', 1)[1].strip()

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
                        logSQLCreate.warning("file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num),line,e))

                for data in logdata:
                    if data.get('logdetail') == '':
                        data['logdetail'] = 'Null'
                    try:
                        sql_insert = 'INSERT INTO log_trace (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(data.get('logfile'), str(data.get('logline')),data.get('loglevel'),data.get('logtime'),data.get('logcomp'),data.get('logdetail').replace('"',"'"))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! - {}".format(e))

                self.SQLData = ({'db_name':self.db_name,
                                 'db_type':self.db_type,
                                 'db_table':'log_trace',
                                 'db_data':sqldata,})

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

if __name__ == '__main__':
    pass
    # filepath = r'D:\05.Code\1trace'
    # test_obj = ITOM_MP_SQLServer(filepath, 'demodb', 'oa')