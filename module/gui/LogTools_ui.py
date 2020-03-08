# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogTools.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 300)
        Form.setMinimumSize(QtCore.QSize(300, 300))
        Form.setMaximumSize(QtCore.QSize(300, 300))
        self.lab_company = QtWidgets.QLabel(Form)
        self.lab_company.setGeometry(QtCore.QRect(12, 74, 42, 16))
        self.lab_company.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_company.setObjectName("lab_company")
        self.lab_product = QtWidgets.QLabel(Form)
        self.lab_product.setGeometry(QtCore.QRect(12, 150, 42, 16))
        self.lab_product.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_product.setObjectName("lab_product")
        self.lab_category = QtWidgets.QLabel(Form)
        self.lab_category.setGeometry(QtCore.QRect(12, 112, 48, 16))
        self.lab_category.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_category.setObjectName("lab_category")
        self.cbx_company = QtWidgets.QComboBox(Form)
        self.cbx_company.setGeometry(QtCore.QRect(66, 74, 220, 20))
        self.cbx_company.setMinimumSize(QtCore.QSize(220, 20))
        self.cbx_company.setMaximumSize(QtCore.QSize(220, 20))
        self.cbx_company.setObjectName("cbx_company")
        self.cbx_category = QtWidgets.QComboBox(Form)
        self.cbx_category.setGeometry(QtCore.QRect(66, 112, 220, 20))
        self.cbx_category.setMinimumSize(QtCore.QSize(220, 20))
        self.cbx_category.setMaximumSize(QtCore.QSize(220, 20))
        self.cbx_category.setObjectName("cbx_category")
        self.cbx_product = QtWidgets.QComboBox(Form)
        self.cbx_product.setGeometry(QtCore.QRect(66, 150, 220, 20))
        self.cbx_product.setMinimumSize(QtCore.QSize(220, 20))
        self.cbx_product.setMaximumSize(QtCore.QSize(220, 20))
        self.cbx_product.setObjectName("cbx_product")
        self.btn_start = QtWidgets.QPushButton(Form)
        self.btn_start.setEnabled(True)
        self.btn_start.setGeometry(QtCore.QRect(110, 200, 80, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start.sizePolicy().hasHeightForWidth())
        self.btn_start.setSizePolicy(sizePolicy)
        self.btn_start.setMinimumSize(QtCore.QSize(80, 20))
        self.btn_start.setMaximumSize(QtCore.QSize(80, 20))
        self.btn_start.setObjectName("btn_start")

        self.retranslateUi(Form)
        self.cbx_company.activated['QString'].connect(Form.slot_update_cate)
        self.cbx_category.activated['QString'].connect(Form.slot_update_prod)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lab_company.setText(_translate("Form", "Company"))
        self.lab_product.setText(_translate("Form", "Product"))
        self.lab_category.setText(_translate("Form", "Category"))
        self.btn_start.setText(_translate("Form", "Start"))
