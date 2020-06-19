# -*- coding: utf-8 -*-

import re, os, pickle
from xml.etree import ElementTree as ET
from module.rules.MicroFocus_ITOM_OA_FileRule import BlackRule
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import logSQLCreate

class ITOM_OA():
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
        if re.findall('system\.txt', self.filepath, re.IGNORECASE):
            self.log_system()
        # 如果是 OA policy 的文件, 则调用 cfg_policy 方法来读取日志
        elif re.findall('\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml', self.filepath, re.IGNORECASE):
            self.cfg_policy()
        # 如果是 OA 的 OA 信息文件, 则调用 cfg_oainfo 方法来读取日志
        elif re.findall('agent.log_\d{4}-\d{2}-\d{2}_\d{2}.\d{2}', self.filepath, re.IGNORECASE):
            self.cfg_oainfo()
        # 其余文件则尝试匹配 OA 的 trace 日志
        elif re.findall('trace_\d+\.txt|ovcd_\d+\.txt|oacore_\d+\.txt|ovbbccb_\d+\.txt|opcmona_\d+\.txt|opcmsga_\d+\.txt', self.filepath, re.IGNORECASE):
            self.log_traces()

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
                        logSQLCreate.warning("file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath,str(log_num),line,e))

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

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

        except Exception as reason:
            logSQLCreate.error('logfile read error:{}'.format(reason))

    def log_traces(self):
        """
        针对 MicroFocus ITOM OA 中的 trace 文件 (需要先解码)
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
                            if re.findall('"Info",|"Warn",|"Error",', line):
                                isstart = True

                        # 如果改行既不在黑名单, 并且也已经确定 isstart 为 True, 则开始日志匹配流程
                        if isnoblk and isstart:
                            line = line.strip()
                            # 判断该行日志是否符合格式
                            if len(line.split(',', 11)) >= 11:
                                line_data = line.split(',',11)
                                log_level = line_data[0].strip()[1:-1]
                                log_time = sql_write.sqlite_to_datetime(line_data[2].strip())
                                log_Machine = line_data[3].strip()
                                log_comp = line_data[4].strip()
                                if re.findall(',,', line):
                                    log_pid = line.replace('"', "'").split(',', 10)[-3].strip()
                                else:
                                    log_pid = line_data[-3].strip().replace('"', "'")
                                if re.findall(',,', line):
                                    log_tid = line.replace('"', "'").split(',', 10)[-2].strip()
                                else:
                                    log_tid = line_data[-2].strip().replace('"', "'")
                                log_tic_count = line_data[1].strip().replace('"', "'")
                                if re.findall(',,', line):
                                    log_msg = line.replace('"', "'").split(',', 10)[-1].strip()
                                else:
                                    log_msg = line_data[-1].strip().replace('"', "'")
                                logdata.append({'logfile': self.filepath,
                                                'logline': log_num,
                                                'loglevel': log_level,
                                                'logtime': log_time,
                                                'machine': log_Machine,
                                                'logcomp': log_comp,
                                                'pid': log_pid,
                                                'tid': log_tid,
                                                'tic_count': log_tic_count,
                                                'logdetail': log_msg})
                            else:
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'] + '\n' + line
                                # 抹掉日志中剩下的 '/n'
                                logdata[-1]['logdetail'] = logdata[-1]['logdetail'].strip()
                    except Exception as e:
                        logSQLCreate.warning(
                            "file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath, str(log_num), line, e))

                for data in logdata:
                    try:
                        sql_insert = 'INSERT INTO log_Trace (logfile, logline, loglevel, logtime, logcomp, logdetail, machine, pid, tid, tic_count) ' \
                                     'VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}");'.format(
                            data.get('logfile'), str(data.get('logline')), data.get('loglevel'), data.get('logtime'),
                            data.get('logcomp'), data.get('logdetail'), data.get('machine'), data.get('pid'), data.get('tid'), data.get('tic_count'))
                        sqldata.append(sql_insert)
                    except Exception as e:
                        logSQLCreate.warning("Can't generate SQL INSERT INTO statement! - {}".format(e))

                self.SQLData = ({'db_name': self.db_name,
                                 'db_type': self.db_type,
                                 'db_table': 'log_Trace',
                                 'db_data': sqldata, })

                # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
                datafilepath = r'./temp/{}'.format(self.file_id)
                open('{}.lck'.format(datafilepath), 'w').close()
                with open(datafilepath, 'wb') as f:
                    pickle.dump(self.SQLData, f)
                os.remove('{}.lck'.format(datafilepath))

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

        # 生成一个对应的 .lck 文件, 在数据写入完成后, 再删除 .lck 文件
        datafilepath = r'./temp/{}'.format(self.file_id)
        open('{}.lck'.format(datafilepath), 'w').close()
        with open(datafilepath, 'wb') as f:
            pickle.dump(self.SQLData, f)
        os.remove('{}.lck'.format(datafilepath))

    def cfg_oainfo(self):
        """
        针对 MicroFocus ITOM OA 中的 agent.log_<日期> 的文件
        """
        # 初始化数据和相关控制参数
        logdata = {}
        sqldata = []
        log_num = 0
        ###########################################################################
        # 判断 ovconfget 命令的开始
        sta_ovconf = False
        # 判断 ovconfget 命令的结束
        end_ovconf_mid = False  # 第一次匹配 ****** 时做一次记录
        end_ovconf = False
        # ovconfget 命令数据
        agt_ovconf = 'Null'
        ###########################################################################
        # 判断 ovdeploy -inv -inclbdl -includeupdates 命令的开始
        sta_ovdeploy = False
        # 判断 ovdeploy -inv -inclbdl -includeupdates 命令的结束
        end_ovdeploy_mid = False  # 第一次匹配 ****** 时做一次记录
        end_ovdeploy = False
        # ovdeploy -inv -inclbdl -includeupdates 命令数据
        agt_ovdeploy = 'Null'
        ###########################################################################
        # 与软件/系统相关的参数
        os_name = 'Null'
        os_type = 'Null'
        os_version = 'Null'
        os_hostname = 'Null'
        agt_version = 'Null'
        agt_core_id = 'Null'
        os_machine = 'Null'

        # 尝试开始读取文件
        try:
            with open(self.filepath, mode='r', encoding='utf-8', errors='replace') as f:
                for line in f:
                    try:
                        log_num += 1
                        if len(re.findall('Cmd executed.*ovconfget', line, re.IGNORECASE)) > 0 and sta_ovconf == False:
                            sta_ovconf = True
                            end_ovconf = False
                            agt_ovconf = ''

                        elif len(re.findall('\*{40}', line)) > 0 and sta_ovconf == True and end_ovconf == False:
                            if end_ovconf_mid == False:
                                end_ovconf_mid = True
                            else:
                                end_ovconf = True

                        elif len(re.findall('\*{40}', line)) == 0 and sta_ovconf == True and end_ovconf == False:
                            agt_ovconf = agt_ovconf + line
                            if len(re.findall('agtversion=', line)) > 0:
                                # OA 的版本
                                agt_version = line.strip().split('=')[-1].strip()
                            elif len(re.findall('osname=', line)) > 0:
                                # 系统发行版的名字
                                os_name = line.strip().split('=')[-1].strip()
                            elif len(re.findall('ostype=', line)) > 0:
                                # 系统类型
                                os_type = line.strip().split('=')[-1].strip()
                            elif len(re.findall('osversion=', line)) > 0:
                                # 系统内核版本
                                os_version = line.strip().split('=')[-1].strip()
                            elif len(re.findall('CORE_ID=', line)) > 0:
                                # OA 的 core id
                                agt_core_id = line.strip().split('=')[-1].strip()
                            elif len(re.findall('OPC_NODENAME=', line)) > 0:
                                # 主机名
                                os_hostname = line.strip().split('=')[-1].strip()

                        elif len(re.findall('ovdeploy -inv -inclbdl -includeupdates', line)) > 0 and sta_ovdeploy == False:
                            sta_ovdeploy = True
                            end_ovdeploy = False
                            agt_ovdeploy = ''

                        elif len(re.findall('\*{40}', line)) > 0 and sta_ovdeploy == True and end_ovdeploy ==False:
                            if end_ovdeploy_mid == False:
                                end_ovdeploy_mid = True
                            else:
                                end_ovdeploy = True

                        elif len(re.findall('\*{40}', line)) == 0 and sta_ovdeploy == True and end_ovdeploy == False:
                            agt_ovdeploy = agt_ovdeploy + line

                        elif len(re.findall('Machine: ', line)) > 0:
                            os_machine = line.strip().split(':')[-1].strip()

                    except Exception as e:
                        logSQLCreate.warning(
                            "file:{}\nline:{}\nSource:{}\nException:{}".format(self.filepath, str(log_num), line, e))

            # 整理获取的值
            logdata['os_name'] = os_name.strip()
            logdata['os_type'] = os_type.strip()
            logdata['os_hostname'] = os_hostname.strip()
            logdata['os_version'] = os_version.strip()
            logdata['os_machine'] = os_machine.strip()
            logdata['agt_version'] = agt_version.strip()
            logdata['agt_core_id'] = agt_core_id.strip()
            logdata['agt_ovconf'] = agt_ovconf.strip()
            logdata['agt_ovdeploy'] = agt_ovdeploy.strip()

            for k, v in logdata.items():
                try:
                    sql_insert = 'INSERT INTO cfg_OAInfo (attribute, value) VALUES ("{}", "{}");'.format(k, v)
                    sqldata.append(sql_insert)
                except Exception as e:
                    logSQLCreate.warning("Can't generate SQL INSERT INTO statement! - {}".format(e))

            self.SQLData = ({'db_name': self.db_name,
                             'db_type': self.db_type,
                             'db_table': 'cfg_OAInfo',
                             'db_data': sqldata, })

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
    filepath = r'D:\05.Code\opcmona_00133.txt'
    test_obj = ITOM_OA(filepath, 'demodb', 'oa')