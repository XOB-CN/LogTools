# -*- coding: utf-8 -*-

################################################
# 参考代码：https://xbuba.com/questions/52765697
################################################

from PyQt5.Qt import *

class SQLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置高亮的字体格式
        sql_keyword_format = QTextCharFormat()
        sql_keyword_format.setForeground(Qt.blue)
        sql_keyword_format.setFontWeight(QFont.Bold)
        # 需要高亮的关键字
        sql_keywords = ['select ', 'from ', 'where ', 'order by ', ' and ', ' or ', ' like ', ' join ', ]
        # 根据前两个来生成高亮规则
        self.highlightRules = [(QRegExp(pattern), sql_keyword_format) for pattern in sql_keywords]

    def highlightBlock(self, text):
        for pattern, _format in self.highlightRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >=0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    editor = QTextEdit()
    editor.append("select * from <table_name>")
    highlighter = SQLHighLighter(editor.document())
    editor.show()
    sys.exit(app.exec_())