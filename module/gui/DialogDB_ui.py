# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogDB.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 200)
        Dialog.setMinimumSize(QtCore.QSize(350, 200))
        Dialog.setMaximumSize(QtCore.QSize(350, 200))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.lab_filepath = QtWidgets.QLabel(Dialog)
        self.lab_filepath.setObjectName("lab_filepath")
        self.gridLayout.addWidget(self.lab_filepath, 5, 0, 1, 1)
        self.btn_dialog = QtWidgets.QDialogButtonBox(Dialog)
        self.btn_dialog.setOrientation(QtCore.Qt.Horizontal)
        self.btn_dialog.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_dialog.setObjectName("btn_dialog")
        self.gridLayout.addWidget(self.btn_dialog, 7, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.lab_explain = QtWidgets.QLabel(Dialog)
        self.lab_explain.setObjectName("lab_explain")
        self.gridLayout.addWidget(self.lab_explain, 0, 0, 1, 3)
        self.line_dbname = QtWidgets.QLineEdit(Dialog)
        self.line_dbname.setClearButtonEnabled(True)
        self.line_dbname.setObjectName("line_dbname")
        self.gridLayout.addWidget(self.line_dbname, 3, 1, 1, 1)
        self.line_filepath = QtWidgets.QLineEdit(Dialog)
        self.line_filepath.setDragEnabled(False)
        self.line_filepath.setClearButtonEnabled(True)
        self.line_filepath.setObjectName("line_filepath")
        self.gridLayout.addWidget(self.line_filepath, 5, 1, 1, 1)
        self.lab_dbname = QtWidgets.QLabel(Dialog)
        self.lab_dbname.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lab_dbname.setObjectName("lab_dbname")
        self.gridLayout.addWidget(self.lab_dbname, 3, 0, 1, 1)
        self.btn_dbname = QtWidgets.QPushButton(Dialog)
        self.btn_dbname.setObjectName("btn_dbname")
        self.gridLayout.addWidget(self.btn_dbname, 3, 2, 1, 1)
        self.btn_filepath = QtWidgets.QPushButton(Dialog)
        self.btn_filepath.setObjectName("btn_filepath")
        self.gridLayout.addWidget(self.btn_filepath, 5, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.btn_dialog.accepted.connect(Dialog.slot_accept)
        self.btn_dialog.rejected.connect(Dialog.reject)
        self.btn_dbname.clicked.connect(Dialog.slot_select_db)
        self.btn_filepath.clicked.connect(Dialog.slot_file_path)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lab_filepath.setText(_translate("Dialog", "LogFile"))
        self.lab_explain.setText(_translate("Dialog", "Please select the database you want to create or import"))
        self.lab_dbname.setText(_translate("Dialog", "DB Name"))
        self.btn_dbname.setText(_translate("Dialog", "Select DB"))
        self.btn_filepath.setText(_translate("Dialog", "File Path"))
