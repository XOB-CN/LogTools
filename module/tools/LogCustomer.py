# -*- coding: utf-8 -*-

import os, time, pickle
from PyQt5.Qt import *
from module.tools.SQLTools import sql_write
from module.tools.LogRecord import loglogTools

class LogCustomer(QThread):
    """
    获取分析完成的文件数据, 然后将这些数据保存到 SQLite 数据库中
    """
    # 发射自定义信号, 说明已经将数据写入到数据库中
    singal_had_write = pyqtSignal(int, int)

    def __init__(self, parent=None, num_files=None):
        super().__init__(parent)
        # 需要保存的文件数量
        self.num_files = num_files
        # 判断阈值
        self.is_end = True

    def run(self):
        num = 0
        SQLData = ''
        while self.is_end:
            time.sleep(1)
            files = os.listdir('./temp')
            # 将包含有 .lck 的文件从待读取的文件列表中去掉
            if len(files) != 0:
                for file in files:
                    if file[-4:] == '.lck':
                        files.remove(file)
                        files.remove(file[0:-4])
                # 如果将包含有 .lck 相关的文件去掉后还不为空, 那么这些文件就是 LogProducer 处理完成的数据
                if len(files) != 0:
                    for file in files:
                        with open('./temp/{}'.format(file), 'rb') as f:
                            num += 1
                            try:
                                if num == self.num_files:
                                    self.is_end = False
                                SQLData = pickle.load(f)
                                sql_write.sqlite_to_database(SQLData)
                            except Exception as e:
                                loglogTools.warning(e)
                        os.remove('./temp/{}'.format(file))
                        self.singal_had_write.emit(num, self.num_files)