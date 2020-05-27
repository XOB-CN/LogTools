# -*- coding: utf-8 -*-

from PyQt5.Qt import *

def mult_process_task(func, filepath, db_name, product_type):
    func(filepath, db_name, product_type)

class LogProducer(QThread):
    """
    将待分析的日志文件列表分配给子进程, 这些子进程会分析日志, 并且生成数据文件
    """
    def __init__(self, parent=None ,task_data=None, pool=None):
        super().__init__(parent)
        self.task_data = task_data
        self.db_name = self.task_data.get('db_name')
        self.product_type = self.task_data.get('product_type')
        self.pool = pool

    def run(self):
        # 判断导入类型
        if self.product_type == 'MicroFocus-ITOM-OA':
            from module.rules.MicroFocus_ITOM_OA_InsertRule import ITOM_OA as LogSQL
        elif self.product_type == 'MicroFocus-ITOM-OBM/OMi':
            from module.rules.MicroFocus_ITOM_OBM_InsertRule import ITOM_OBM as LogSQL

        # 执行多进程, 开始生成分析数据
        for filepath in self.task_data.get('file_path'):
            try:
                self.pool.apply_async(mult_process_task, args=(LogSQL, filepath, self.db_name, self.product_type))
            except Exception as e:
                print(e)