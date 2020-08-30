# -*- coding: utf-8 -*-

from configparser import ConfigParser
cfg = ConfigParser()
# 添加 encoding = utf-8 的目的是防止解析错误
cfg.read('Settings.cfg', encoding='utf-8')

class ConfigTools():
    """
    用于获取和设置 LogTools 的相关参数
    """
    @staticmethod
    def get_num_processes():
        """
        获取计算机上的处理器核数和内存资源来确定进程池的数量
        :return: int
        """
        value = cfg.get('Performance','Num_Processes')
        if value == "Auto":
            import psutil
            num_cpu = psutil.cpu_count(logical=False)
            num_mem = psutil.virtual_memory().free / (1024 * 1024 * 1024)
            if num_cpu * 2 <= num_mem:
                return num_cpu - 1
            else:
                num_pool = int(num_mem / 2)
                if num_pool >= 2:
                    return num_pool
                else:
                    return 1
        else:
            try:
                return int(value)
            except:
                return 1

    @staticmethod
    def get_sql_comment():
        """
        获取配置文件中 [User Settings] 部分中的 SQL_Comment 设定值
        :return: str
        """
        try:
            return cfg.get('User Settings', 'SQL_Comment')
        except Exception as e:
            return str(e)

    @staticmethod
    def get_loglevel(attribute, defaultLogLevel='WARN'):
        """
        获取配置文件中 [Logs] 部分的设定值
        :param attribute: 待获取的属性值的名字
        :param defaultLogLevel: 如果获取的值不在预期的值时, 返回的默认值
        :return: str
        """
        value = cfg.get('Logs', attribute)
        if value in ['INFO', 'Info', 'info']:
            return 'INFO'
        elif value in ['WARN', 'WARNING', 'Warn', 'Warning']:
            return 'WARN'
        elif value in ['ERROR', 'Error', 'error']:
            return 'ERROR'
        elif value in ['DEBUG', 'Debug', 'debug']:
            return 'DEBUG'
        else:
            return defaultLogLevel

    @staticmethod
    def get_debug(attribute, defaultLogLevel=False):
        """
        获取配置文件中 [Debug] 部分的设定值
        :param attribute: 待获取的属性值的名字
        :param defaultLogLevel: 如果获取的值不在预期的值时, 返回的默认值
        :return: Boolean
        """
        try:
            value = cfg.getboolean('Debug', attribute)
            return value
        except:
            return defaultLogLevel