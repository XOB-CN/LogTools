# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
FileRule = [
    # OBM Infomation file
    'opr-checker-xml\.txt',
    'opr-checker\.txt',
    # OBM logs
    'jvm_statistics\.log',
    'busjvm_statistics\.log',
    'bus\.log',
    'opr-gateway\.log',
    'opr-ciresolver\.log',
    'opr-configserver\.log',
    'opr-backend\.log',
    'opr-backend_boot\.log',
    'opr-svcdiscserver\.log',
    'opr-svcdiscserver-citrace\.log',
    'opr-scripting-host\.log',
    'opr-webapp\.log',
    'downtime\.log',
    'pmi\.log',
    'scripts\.log',
    'cmdb\.reconciliation\.identification\.log',
    'cmdb\.reconciliation\.datain\.merged\.log',
    'cmdb\.reconciliation\.datain\.ignored\.log',
    'MI_MonitorAdministration\.log',
    'wde\.all\.log',
    'notification-service\.log',
    'nanny_all\.log',
    'server_deployer\.log',
]

# 文件级别的反匹规则, 支持正则表达式
FileBlkRule = [
]

# 文件每一行的反匹规则, 支持正则表达式
BlackRule = [
]