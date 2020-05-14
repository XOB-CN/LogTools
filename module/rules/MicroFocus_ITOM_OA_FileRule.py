# -*- coding: utf-8 -*-

# 文件级别的匹配规则
FileRule = [
    'system\.txt',
    '\w{8}-\w{4}-\w{4}-\w{4}-\w{12}_header\.xml',
]

# 文件级别的反匹规则
FileBlkRule = [
    r'\\public\\System.txt',
]

BlackRule = [
    'rolled=0',
]