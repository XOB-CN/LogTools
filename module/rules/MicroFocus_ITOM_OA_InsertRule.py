# -*- coding: utf-8 -*-

import re, os
from xml.etree import ElementTree as ET
from module.rules.MicroFocus_ITOM_OA_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logSQLCreate

class ITOM_OA():
    """
    读取日志文件的类, 并返回分析的数据
    """
    SQLData = {}

    def __init__(self, filepath, db_name, product_type):
        self.filepath = filepath
        self.db_name = db_name
        self.db_type = product_type

        # 如果是 system.txt 文件, 则调用 log_system 方法读取日志
        if len(re.findall('system\.txt', self.filepath, re.IGNORECASE)) > 0:
            self.log_system()
        # 如果是 OA policy 的文件, 则调用 cfg_policy 方法来读取日志
        elif len(re.findall('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml', self.filepath, re.IGNORECASE)) > 0:
            self.cfg_policy()

    def log_system(self):
        """
        针对 MicroFocus ITOM OA 中的 System.txt 文件
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
                        sql_insert = 'INSERT INTO log_System (logfile, logline, loglevel, logtime, logcomp, logdetail) VALUES ("{}","{}","{}","{}","{}","{}");'.format(data.get('logfile'), str(data.get('logline')),data.get('loglevel'),data.get('logtime'),data.get('logcomp'),data.get('logdetail').replace('"',"'"))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! - {}".format(e))

                self.SQLData = ({'db_name':self.db_name,
                                 'db_type':self.db_type,
                                 'db_table':'log_System',
                                 'db_data':sqldata,})

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def cfg_policy(self):
        """
        针对 MicroFocus ITOM OA 中的 Policy 文件
        """
        # 初始变量
        sqldata = []
        ply_name = 'Null'
        ply_version = 'Null'
        ply_status = 'Null'
        ply_type = 'Null'
        ply_data = 'Null'
        ply_data_filename = 'Null'
        ply_param = 'Null'
        ply_param_filename = 'Null'

        # 读取 xml 文件
        oa_policy = ET.parse(self.filepath)
        str_prefix = './/' + oa_policy.getroot().tag.split('}')[0] + '}'
        # 获取 policy 的值
        try:
            ply_name = str(oa_policy.find(str_prefix + 'name').text)
        except:
            pass
        try:
            ply_version = str(oa_policy.find(str_prefix + 'version').text)
        except:
            pass
        try:
            ply_status = str(oa_policy.find(str_prefix + 'status').text)
        except:
            pass
        try:
            ply_type = oa_policy.find(str_prefix + 'policytype').find(str_prefix + 'name').text
        except:
            pass
        ply_files = oa_policy.findall(str_prefix + 'file_name')
        if len(ply_files) == 2:
            try:
                ply_data_filename = ply_files[0].text
                ply_data_path = os.path.join(os.path.dirname(self.filepath), ply_data_filename)
                with open(ply_data_path, mode='r', encoding='utf-8', errors='replace') as f:
                    content = f.readlines()
                    ply_data = ''
                    for line in content:
                        ply_data = ply_data + line

                    # SQLite 数据库的特殊字符转换：大致规则为单引号和双引号要变成两个, 其他特殊字符为前面加上'/'
                    ply_data = ply_data.replace("'","''").replace('"','""')

                ply_param_filename = ply_files[1].text
                ply_param_path = os.path.join(os.path.dirname(self.filepath), ply_param_filename)
                with open(ply_param_path, mode='r', encoding='utf-8', errors='replace') as f:
                    content = f.readlines()
                    ply_param = ''
                    for line in content:
                        ply_param = ply_param + line
                    ply_param = ply_param.replace("'","''").replace('"','""')
            except:
                ply_data = 'Null'
                ply_param = 'Null'
        elif len(ply_files) == 1:
            try:
                ply_data_filename = ply_files[0].text
                ply_data_path = os.path.join(os.path.dirname(self.filepath), ply_data_filename)
                with open(ply_data_path, mode='r', encoding='utf-8', errors='replace') as f:
                    content = f.readlines()
                    ply_data = ''
                    for line in content:
                        ply_data = ply_data + line
                ply_data = ply_data.replace("'", "''").replace('"', '""')
            except:
                ply_data = 'Null'

        # 生成 SQL 语句
        sql_insert = 'INSERT INTO cfg_Policy (ply_name, ply_version, ply_status, ply_type, ply_data, ply_param) VALUES ("{}","{}","{}","{}","{}","{}");'.format(ply_name, ply_version, ply_status, ply_type, ply_data, ply_param)
        sqldata.append(sql_insert)

        # 传递数据
        self.SQLData = ({'db_name':self.db_name,
                         'db_type':self.db_type,
                         'db_table':'cfg_Policy',
                         'db_data':sqldata,})

if __name__ == '__main__':
    pass
    # filepath = r'D:\05.Code\policies\monitortmpl\2a1a3226-85f3-4de4-bd66-d3f742da42a8_header.xml'
    # test_obj = ITOM_OA(filepath, 'demodb', 'oa')