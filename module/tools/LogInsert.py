# -*- coding: utf-8 -*-

import os, re
from PyQt5.Qt import *

class LogInsert(QThread):
    def __init__(self, parent=None, task_info=None):
        super().__init__(parent)
        self.task_info = task_info
        self.file_path = []
        # 匹配产品规则
        if self.task_info.get('product_type') == 'MicroFocus-ITOM-OA':
            from module.rules import MicroFocus_ITOM_OA_FileRule as FileRule
            self.file_rule = FileRule.FileRule

    def run(self):
        '''
        将符合规则的日志文件导入到数据库中
        '''
        # 预处理：获取需要进一步分析的文件列表以及相关信息，例如总共需要分析的文件个数
        filepath = self.task_info.get('file_path')
        if filepath != '':
            # 如果 file_type 的值是 file, 直接返回文件列表
            self.task_info['file_type'] = 'file'
            self.file_path.append(os.path.abspath(self.task_info.get('file_path')))
        else:
            # 如果 file_type 的值是 dir, 则需要做进一步的判断
            self.task_info['file_type'] = 'dir'
            # os.walk 方法将返回三个值, 分别为 '当前目录', '当前目录的子目录', '当前目录所包含的文件'
            for root, dirs, files in os.walk(self.task_info.get('dir_path')):
                for file in files:
                    url_file = os.path.join(root, file)
                    url_file = os.path.abspath(url_file)
                    # 对这个文件进行匹配, 如果该文件符合匹配规则, 则加入待到文件列表中
                    for rule in self.file_rule:
                        if len(re.findall(rule, url_file, flags=re.IGNORECASE)) > 0:
                            self.file_path.append(url_file)

        print(self.file_path)
        # 处理中：读取日志/将数据写入数据库
        pass
        # 处理后：收尾内容，做一些后续的处理