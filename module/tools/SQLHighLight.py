# -*- coding: utf-8 -*-

from PyQt5.Qt import *

class SQLHighLight(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SQLHighLight, self).__init__(parent)
        # sql highlight
        sqlFormat = QTextCharFormat()
        sqlFormat.setFontWeight(QFont.Bold)
        sqlFormat.setForeground(Qt.blue)

        sqlKeywords = ["select", "where"]

        # self.highlightRules = []
        # for highlightRule in sqlKeywords:
        #     self.highlightRules.append(QRegExp(highlightRule), sqlFormat)

        self.highlightRules = [(QRegExp(pattern), sqlFormat) for pattern in sqlKeywords]
        print(self.highlightRules)


    def highlightBlock(self, text):
        try:
            for pattern, _format in self.highlightRules:
                expression = QRegExp(pattern)
                index = expression.indexIn(text)
                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, _format)
                    index = expression.indexIn(text, index + length)

        except Exception as e:
            print(e)
