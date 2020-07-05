# -*- coding: utf-8 -*-

import os, re
from module.tools.LogRecord import loglogTools

class LogCheck():
    """
    检查文件列表中有哪些文件需要被分析
    """
    def __init__(self, task_info):
        self.task_info = task_info
        # 需要分析的日志文件列表
        self.file_path = []
        # 调试功能, 仅用于内部调试
        self.debug = False

        # 匹配产品规则
        if self.task_info.get('product_type') == 'MicroFocus-ITOM-OA':
            from module.rules import MicroFocus_ITOM_OA_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        elif self.task_info.get('product_type') == 'MicroFocus-ITOM-OBM/OMi':
            from module.rules import MicroFocus_ITOM_OBM_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        elif self.task_info.get('product_type') == 'MicroFocus-ITOM-MP for Microsoft SQL Server':
            from module.rules import MicroFocus_ITOM_MP_MSSQLServer_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        elif self.task_info.get('product_type') == 'MicroFocus-ITOM-MP for Oracle Database':
            from module.rules import MicroFocus_ITOM_MP_OracleDatabase_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        elif self.task_info.get('product_type') == 'MicroFocus-ITOM-SiteScope':
            from module.rules import MicroFocus_ITOM_SiteScope_FileRule as FileRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

    def check(self):
        """
        获取需要分析的文件列表, 以及日志类型
        :return: dict
        """
        try:
            # self.file_path 为获取需要进一步分析的文件列表
            filepath = self.task_info.get('file_path')
            log_type = self.task_info.get('product_type')
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
                        if self.debug:
                            print('识别的文件:', url_file)
                        # 对这个文件进行匹配, 如果该文件符合匹配规则, 则加入待到文件列表中
                        for rule in self.file_rule:
                            if len(re.findall(rule, url_file, flags=re.IGNORECASE)) > 0:
                                self.file_path.append(url_file)
                                if self.debug:
                                    print('匹配的文件:', url_file)
                                # 如果该文件路径符合黑名单规则, 则在文件列表中去掉这个文件
                                for blkrule in self.fileblk_rule:
                                    if len(re.findall(blkrule, url_file, flags=re.IGNORECASE)) > 0:
                                        self.file_path.pop(self.file_path.index(url_file))
                                        if self.debug:
                                            print('去除的文件:', url_file)
        except Exception as e:
            loglogTools.warning('FileRule: ' + str(e))

        self.task_info['file_path'] = list(set(self.file_path))

        return self.task_info