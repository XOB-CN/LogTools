# -*- coding: utf-8 -*-

################################################
# 参考代码：https://xbuba.com/questions/52765697
################################################

from PyQt5.Qt import *

class SQLHighLighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置 keyword 高亮的字体格式
        sql_keyword_format = QTextCharFormat()
        sql_keyword_format.setForeground(Qt.blue)
        sql_keyword_format.setFontWeight(QFont.Bold)
        # 设置 comment 高亮的字体格式
        sql_comment_format = QTextCharFormat()
        sql_comment_format.setForeground(Qt.darkGreen)
        sql_comment_format.setFontWeight(QFont.Bold)
        # 需要高亮的关键字
        sql_keywords = [
            # 基本 SQL 语句
            'select ', 'from ',
            # SQL 子句
            'where ', 'order by ', 'group by ',
            # SQL 操作符/运算符
            ' and ', ' or ', ' like ', ' not like ', ' glob ', ' not glob ', ' join ', ' union', ' union all', 'distinct ',
            # SQL 常用函数
            # 参考链接：https://www.runoob.com/sqlite/sqlite-functions.html
            'sum', 'total', 'count', 'max', 'min', 'avg', 'abs', 'random', 'upper', 'lower', 'length',
        ]
        # 根据前两个来生成高亮规则
        self.highlightRules = [(QRegExp(pattern), sql_keyword_format) for pattern in sql_keywords]
        # 追加 comment 规则
        self.highlightRules.append((QRegExp('--.*'), sql_comment_format))

    def highlightBlock(self, text):
        # keyword 高亮
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