# -*- coding: utf-8 -*-

from PyQt5.Qt import *
from module.tools.SQLTools import sql_write

class LogInsert(QThread):
    # 发射自定义信号, 说明已经将数据写入到数据库中
    singal_had_write = pyqtSignal(int, int)

    def __init__(self, parent=None ,task_data=None):
        super().__init__(parent)
        self.task_data = task_data
        self.db_name = self.task_data.get('db_name')
        self.product_type = self.task_data.get('product_type')

    def run(self):
        # 判断导入类型
        if self.product_type == 'MicroFocus-ITOM-OA':
            from module.rules.MicroFocus_ITOM_OA_InsertRule import ITOM_OA as LogSQL
        elif self.product_type == 'MicroFocus-ITOM-OBM/OMi':
            from module.rules.MicroFocus_ITOM_OBM_InsertRule import ITOM_OBM as LogSQL

        # 如果文件列表非零, 则开启日志录入流程
        if self.task_data.get('file_path') != []:
            value = 0
            total = len(self.task_data.get('file_path'))

            # 循环执行: filepath
            for filepath in self.task_data.get('file_path'):
                value += 1
                SQL = LogSQL(filepath, self.db_name, self.product_type)
                SQLData = SQL.SQLData
                sql_write.sqlite_to_database(SQLData)
                self.singal_had_write.emit(value, total)

        # 如果文件列表为零, 直接传递为零, 代表没数据
        else:
            self.singal_had_write.emit(0, 0)