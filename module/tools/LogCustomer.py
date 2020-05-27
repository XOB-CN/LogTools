# -*- coding: utf-8 -*-

import os, pickle
from PyQt5.Qt import *
from module.tools.SQLTools import sql_write

class LogCustomer(QThread):
    def __init__(self, parent=None, num_files=None):
        super().__init__(parent)
        # 需要保存的文件数量
        self.num_files = num_files
        # 判断阈值
        self.is_end = True

    def run(self):
        pass

if __name__ == '__main__':
    # 先获取文件列表
    files = os.listdir('../../temp')
    SQLData = ''

    if len(files) != 0:
        for file in files:
            if file[-4:] == '.lck':
                files.remove(file)
                files.remove(file[0:-4])

        if len(files) != 0:
            for file in files:
                with open('../../temp/{}'.format(file), 'rb') as f:
                    SQLData = pickle.load(f)
                    print(type(SQLData))