# -*- coding: utf-8 -*-

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('Settings.cfg')

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