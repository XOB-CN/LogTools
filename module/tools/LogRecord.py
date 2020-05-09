# -*- coding: utf-8 -*-

import os, logging

if os.path.exists('./logs') == False:
    os.mkdir('./logs')

# logging.basicConfig(level=logging.DEBUG,
#                     filename='.\\logs\\output.log',
#                     datefmt='%Y/%m/%d %H:%M:%S',
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s',)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 设定 logging handler 的输出位置和格式
handler_SQLInsert = logging.FileHandler('.\\logs\\SQLInsert.log')
handler_SQLInsert.setFormatter(formatter)
handler_SQLCreate = logging.FileHandler('.\\logs\\SQLCreate.log')
handler_SQLCreate.setFormatter(formatter)
handler_SQLQuery = logging.FileHandler('.\\logs\\SQLQuery.log')
handler_SQLQuery.setFormatter(formatter)
handler_LogTools = logging.FileHandler('.\\logs\\LogTools.log')
handler_LogTools.setFormatter(formatter)

# 增加 logging 的 logger 实例
logSQLInsert = logging.getLogger('SQLInsert')
logSQLInsert.setLevel(level=logging.INFO)
logSQLInsert.addHandler(handler_SQLInsert)

logSQLCreate = logging.getLogger('SQLCreate')
logSQLCreate.setLevel(level=logging.INFO)
logSQLCreate.addHandler(handler_SQLCreate)

logSQLQuery = logging.getLogger('SQLQuery')
logSQLQuery.setLevel(level=logging.INFO)
logSQLQuery.addHandler(handler_SQLQuery)

loglogTools = logging.getLogger('LogTools')
loglogTools.setLevel(level=logging.INFO)
loglogTools.addHandler(handler_LogTools)