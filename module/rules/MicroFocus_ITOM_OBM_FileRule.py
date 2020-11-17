# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
FileRule = [
    # OBM Infomation file
    'opr-checker-xml\.txt',
    'opr-checker\.txt',
    # rtsm logs
    'error\.log',
    'cmdb\.reconciliation\.identification\.log',
    'cmdb\.reconciliation\.datain\.merged\.log',
    'cmdb\.reconciliation\.datain\.ignored\.log',
    # OBM logs
    'jvm_statistics\.log',
    'busjvm_statistics\.log',
    'bus\.log',
    'opr-gateway\.log',
    'opr-ciresolver\.log',
    'opr-configserver\.log',
    'opr-backend\.log',
    'opr-svcdiscserver\.log',
    'opr-svcdiscserver-citrace\.log',
    'opr-scripting-host\.log',
    'opr-webapp\.log',
    'opr-heartbeat\.log',
    'downtime\.log',
    'pmi\.log',
    'scripts\.log',
    'MI_MonitorAdministration\.log',
    'wde\.all\.log',
    'notification-service\.log',
    'nanny_all\.log',
    'server_deployer\.log',
    # boot logs
    'jboss7_boot\.log',
    'opr-backend_boot\.log',
    'opr-scripting-host_boot\.log',
    'marble_supervisor_boot\.log',
    'businessImpact_service_boot\.log',
    'wde_boot\.log',
    'schedulergw_boot\.log',
    'odb_boot\.log',
    'bus_boot\.log',
]

# 文件级别的反匹规则, 支持正则表达式
FileBlkRule = [
]

# 文件每一行的反匹规则, 支持正则表达式
BlackRule = [
]