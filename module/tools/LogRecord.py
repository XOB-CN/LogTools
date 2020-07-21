# -*- coding: utf-8 -*-

import os, logging
from module.tools.SettingsTools import ConfigTools

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
levelSQLInsert = ConfigTools.get_loglevel('SQLInsert')
if levelSQLInsert == 'INFO':
    logSQLInsert.setLevel(level=logging.INFO)
elif levelSQLInsert == 'WARN':
    logSQLInsert.setLevel(level=logging.WARNING)
elif levelSQLInsert == 'ERROR':
    logSQLInsert.setLevel(level=logging.ERROR)
elif levelSQLInsert == 'DEBUG':
    logSQLInsert.setLevel(level=logging.DEBUG)
logSQLInsert.addHandler(handler_SQLInsert)

logSQLCreate = logging.getLogger('SQLCreate')
levelSQLCreate = ConfigTools.get_loglevel('SQLCreate')
if levelSQLCreate == 'INFO':
    logSQLCreate.setLevel(level=logging.INFO)
elif levelSQLCreate == 'WARN':
    logSQLCreate.setLevel(level=logging.WARNING)
elif levelSQLCreate == 'ERROR':
    logSQLCreate.setLevel(level=logging.ERROR)
elif levelSQLCreate == 'DEBUG':
    logSQLCreate.setLevel(level=logging.DEBUG)
logSQLCreate.addHandler(handler_SQLCreate)

logSQLQuery = logging.getLogger('SQLQuery')
levelSQLQuery = ConfigTools.get_loglevel('SQLQuery')
if levelSQLQuery == 'INFO':
    logSQLQuery.setLevel(level=logging.INFO)
elif levelSQLQuery == 'WARN':
    logSQLQuery.setLevel(level=logging.WARNING)
elif levelSQLQuery == 'ERROR':
    logSQLQuery.setLevel(level=logging.ERROR)
elif levelSQLQuery == 'DEBUG':
    logSQLQuery.setLevel(level=logging.DEBUG)
logSQLQuery.addHandler(handler_SQLQuery)

loglogTools = logging.getLogger('LogTools')
levellogTools = ConfigTools.get_loglevel('logTools')
if levellogTools == 'INFO':
    loglogTools.setLevel(level=logging.INFO)
elif levellogTools == 'WARN':
    loglogTools.setLevel(level=logging.WARNING)
elif levellogTools == 'ERROR':
    loglogTools.setLevel(level=logging.ERROR)
elif levellogTools == 'DEBUG':
    loglogTools.setLevel(level=logging.DEBUG)
loglogTools.addHandler(handler_LogTools)