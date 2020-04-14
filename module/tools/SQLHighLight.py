# -*- coding: utf-8 -*-

from PyQt5.Qt import *

class SQLHighLight(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(SQLHighLight, self).__init__(parent)
        pass


    def highlightBlock(self, text):
        try:
            sqlFormat = QTextCharFormat()
            sqlFormat.setFontWeight(QFont.Bold)
            sqlFormat.setForeground(Qt.blue)

            pattern = '\\bselect\\b'

            expression = QRegExp(pattern)
            index = text.indexOf(expression)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, sqlFormat)
                index = text.indexOf(expression, index + length)

        except Exception as e:
            print(e)
