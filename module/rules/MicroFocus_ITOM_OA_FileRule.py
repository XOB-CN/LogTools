# -*- coding: utf-8 -*-

# 文件级别的匹配规则, 支持正则表达式
FileRule = [
    'system\.txt',
    '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml',
    'agent.log_\d{4}-\d{2}-\d{2}_\d{2}.\d{2}',

    # OA Trace 日志文件
    'trace_\d+\.txt',
    'ovcd_\d+\.txt',
    'oacore_\d+\.txt',
    'ovbbccb_\d+\.txt',
    'opcmsga_\d+\.txt',
    'opcmona_\d+\.txt',
]

# 文件级别的反匹规则, 支持正则表达式
FileBlkRule = [
    r'\\public\\System.txt',
    # 出现于 OpsB 的 OA 中
    r'\\PaxHeaders',
]

# 文件每一行的反匹规则, 支持正则表达式
BlackRule = [
    'rolled=0',
    '"Sev","Tic Count","Time","Machine","Application","Component","Category","Attributes","PID","TID","Source","TraceMsg"',
]