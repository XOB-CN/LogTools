# -*- coding: utf-8 -*-

import os
from PyQt5.Qt import *
from module.rules import MicroFocus_ITOM_OA_FileRule as MF_ITOM_OA_FR

class LogRead(QThread):
    def __init__(self, parent=None, task_info=None):
        super().__init__(parent)
        self.task_info = task_info

    def run(self):
        '''
        返回待分析的文件列表
        :return: list
        '''
        filepath = self.task_info.get('file_path')
        if filepath != '':
            # 如果 file_type 的值是 file, 直接返回文件列表
            self.task_info['file_type'] = 'file'
            self.task_info['logs_list'] = [self.task_info.get('file_path'),]
        else:
            # 如果 file_type 的值是 dir, 则需要做进一步的判断
            self.task_info['file_type'] = 'dir'
            url_file_list = []
            # os.walk 方法将返回三个值, 分别为 '当前目录', '当前目录的子目录', '当前目录所包含的文件'
            for root, dirs, files in os.walk(self.task_info.get('dir_path')):
                for file in files:
                    url_file = os.path.join(root, file)
                    url_file = os.path.abspath(url_file)
                    url_file_list.append(url_file)
            print(url_file_list)

        print(self.task_info)