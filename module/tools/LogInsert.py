# -*- coding: utf-8 -*-

from PyQt5.Qt import *

class LogInsert(QThread):
    # 发射自定义信号, 说明已经将数据写入到数据库中
    singal_had_write = pyqtSignal(int)

    def __init__(self, parent=None ,task_data=None):
        super().__init__(parent)
        self.task_data = task_data

    def run(self):
        # 匹配产品规则
        if self.task_data.get('product_type') == 'MicroFocus-ITOM-OA':
            from module.rules import MicroFocus_ITOM_OA_FileRule as FileRule
            from module.rules.MicroFocus_ITOM_OA_InsertRule import ITOM_OA as LogRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        elif self.task_data.get('product_type') == 'MicroFocus-ITOM-OBM/OMi':
            from module.rules import MicroFocus_ITOM_OBM_FileRule as FileRule
            from module.rules.MicroFocus_ITOM_OBM_InsertRule import ITOM_OBM as LogRule
            self.file_rule = FileRule.FileRule
            self.fileblk_rule = FileRule.FileBlkRule

        if self.task_data.get('file_path') != []:
            for filepath in self.task_data.get('file_path'):
                print(self.task_data.get('product_type'), filepath, self.task_data.get('db_name'))
                self.singal_had_write.emit(1)