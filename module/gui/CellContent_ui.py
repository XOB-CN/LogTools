# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CellContent.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 300)
        Form.setMinimumSize(QtCore.QSize(500, 300))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_search = QtWidgets.QLineEdit(Form)
        self.line_search.setObjectName("line_search")
        self.horizontalLayout.addWidget(self.line_search)
        self.btn_regexp = QtWidgets.QRadioButton(Form)
        self.btn_regexp.setObjectName("btn_regexp")
        self.horizontalLayout.addWidget(self.btn_regexp)
        self.btn_search = QtWidgets.QPushButton(Form)
        self.btn_search.setObjectName("btn_search")
        self.horizontalLayout.addWidget(self.btn_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.cellText = QtWidgets.QTextEdit(Form)
        self.cellText.setObjectName("cellText")
        self.verticalLayout.addWidget(self.cellText)

        self.retranslateUi(Form)
        self.btn_search.clicked.connect(Form.searchText)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_regexp.setText(_translate("Form", "Enable RegExp"))
        self.btn_search.setText(_translate("Form", "Search"))
