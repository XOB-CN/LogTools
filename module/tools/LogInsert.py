# -*- coding: utf-8 -*-

import os, re
from PyQt5.Qt import *
from multiprocessing import Queue, Pool

class LogInsert(QThread):
    def __init__(self, parent=None, task_info=None):
        super().__init__(parent)
        self.task_info = task_info
        # 需要分析的日志文件列表
        self.file_path = []
        # 匹配产品规则
        if self.task_info.get('product_type') == 'MicroFocus-ITOM-OA':
            from module.rules import MicroFocus_ITOM_OA_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

    # 子进程：分析日志
    # 这里需要添加一个 @classmethod, 否则 multiprocessing.Pool.apply_async 方法无法执行!
    @classmethod
    def read_file(self, path):
        print('开始分析进程', str(path))

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
                    for blkrule in self.fileblk_rule:
                        if len(re.findall(blkrule, url_file, flags=re.IGNORECASE)) > 0:
                            self.file_path.pop(self.file_path.index(url_file))

        # 处理中：开启多进程，进行日志分析
        # Pool 方法里会隐含执行 os.cpu_count(), 这里会自动算出 CPU 的核数 (包括超线程)
        p = Pool()
        for path in self.file_path:
            p.apply_async(self.read_file, args=(path,))
        p.close()
