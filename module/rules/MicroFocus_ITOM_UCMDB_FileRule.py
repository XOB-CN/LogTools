# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
FileRule = [
    # also in obm logs
    'error\.log',
    'cmdb\.reconciliation\.identification.*log',
    'cmdb\.reconciliation\.datain\.merged.*log',
    'cmdb\.reconciliation\.datain\.ignored.*log',
    # ucmdb logs
    'cmdb\.api\.audit\.detailed.*log',
    'cmdb\.api\.audit\.detailed\.unformatted.*log',
    'cmdb\.authentication\.audit.*log',
    'cmdb\.browser\.resources.*log',
    'cmdb\.classmodel\.audit\.detailed.*log',
    'cmdb\.classmodel\.audit\.short.*log',
    'cmdb\.dal\.server.*log',
    'cmdb\.dal.*log',
    'cmdb\.dal\.slow.*log',
    'cmdb\.enrichment.*log',
    'cmdb\.ha\.detailed.*log',
    'cmdb\.ha.*log',
    'cmdb\.model\.aging.*log',
    'cmdb\.model\.audit\.short.*log',
    'cmdb\.model\.notification.*log',
    'cmdb\.model\.topology.*log',
    'cmdb\.monitor.*log',
    'cmdb\.notification.*log',
    'cmdb\.operation.*log',
    'cmdb\.pattern\.statistics.*log',
    'cmdb\.quota.*log',
    'cmdb\.reconciliation\.analyzer.*log',
    'cmdb\.reconciliation\.audit.*log',
    'cmdb\.reconciliation\.config.*log',
    'cmdb\.reconciliation\.error.*log',
    'cmdb\.reconciliation\.queries.*log',
    'cmdb\.reconciliation.*log',
    'cmdb\.samlAuthentication.*log',
    'cmdb\.tql\.calculation\.audit.*log',
    'cmdb\.tql\.resultcache.*log',
    'cmdb\.tql\.tracker.*log',
    'fcmdb\.adapters\.HistoryDataSource.*log',
    'fcmdb\.config\.audit.*log',
    'fcmdb\.ftql\.audit.*log',
    'fcmdb.*log',
]

# 文件级别的反匹规则, 支持正则表达式
FileBlkRule = [
]

# 文件每一行的反匹规则, 支持正则表达式
BlackRule = [
]