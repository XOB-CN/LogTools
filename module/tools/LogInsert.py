# -*- coding: utf-8 -*-

import os
from PyQt5.Qt import *
from module.rules import MicroFocus_ITOM_OA_FileRule as MF_ITOM_OA_FR

class LogRead(QThread):
    def __init__(self, parent=None, task_info=None):
        super().__init__(parent)
        self.task_info = task_info

    def run(self):
        filepath = self.task_info.get('file_path')
        if filepath != '':
            self.task_info['file_type'] = 'file'
            # 待分析的文件 URL 列表
            self.task_info['logs_list'] = [self.task_info.get('file_path'),]
        else:
            self.task_info['file_type'] = 'dir'
            # 待分析的文件 URL 列表
            for root, dirs, files in os.walk(self.task_info.get('dir_path')):
                print(root)
                print(dirs)
                print(files)

        print(self.task_info)