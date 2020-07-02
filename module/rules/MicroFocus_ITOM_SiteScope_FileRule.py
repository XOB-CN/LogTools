# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
FileRule = [
    'error\.log',
]

# 文件级别的反匹规则, 支持正则表达式
FileBlkRule = [
]

# 文件每一行的反匹规则, 支持正则表达式
BlackRule = [
    'service:.*Starting monitoring process:.*result',
    'service:.*Stopping service, requested by user',
    'service:.*cleaning up service',
    'service:.*Shutdown request process successful',
]