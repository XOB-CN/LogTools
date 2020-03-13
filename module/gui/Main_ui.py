# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(982, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.geText = QtWidgets.QLabel(self.centralwidget)
        self.geText.setObjectName("geText")
        self.horizontalLayout.addWidget(self.geText)
        self.geTime = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.geTime.setObjectName("geTime")
        self.horizontalLayout.addWidget(self.geTime)
        self.leText = QtWidgets.QLabel(self.centralwidget)
        self.leText.setObjectName("leText")
        self.horizontalLayout.addWidget(self.leText)
        self.leTime = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.leTime.setObjectName("leTime")
        self.horizontalLayout.addWidget(self.leTime)
        self.btnNew = QtWidgets.QPushButton(self.centralwidget)
        self.btnNew.setObjectName("btnNew")
        self.horizontalLayout.addWidget(self.btnNew)
        self.btnQuery = QtWidgets.QPushButton(self.centralwidget)
        self.btnQuery.setObjectName("btnQuery")
        self.horizontalLayout.addWidget(self.btnQuery)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabQuery = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabQuery.sizePolicy().hasHeightForWidth())
        self.tabQuery.setSizePolicy(sizePolicy)
        self.tabQuery.setTabsClosable(True)
        self.tabQuery.setTabBarAutoHide(False)
        self.tabQuery.setObjectName("tabQuery")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sqlEdit1 = QtWidgets.QTextEdit(self.tab_1)
        self.sqlEdit1.setObjectName("sqlEdit1")
        self.gridLayout_2.addWidget(self.sqlEdit1, 0, 0, 1, 1)
        self.tabQuery.addTab(self.tab_1, "")
        self.gridLayout.addWidget(self.tabQuery, 0, 1, 1, 1)
        self.treeList = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeList.sizePolicy().hasHeightForWidth())
        self.treeList.setSizePolicy(sizePolicy)
        self.treeList.setMinimumSize(QtCore.QSize(150, 0))
        self.treeList.setMaximumSize(QtCore.QSize(250, 16777215))
        self.treeList.setObjectName("treeList")
        self.gridLayout.addWidget(self.treeList, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tabResult = QtWidgets.QTabWidget(self.centralwidget)
        self.tabResult.setTabsClosable(True)
        self.tabResult.setTabBarAutoHide(True)
        self.tabResult.setObjectName("tabResult")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabResult.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabResult.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.tabResult)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 982, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setCheckable(False)
        self.actionImport.setObjectName("actionImport")
        self.menuFile.addAction(self.actionImport)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar.addAction(self.actionImport)

        self.retranslateUi(MainWindow)
        self.tabQuery.setCurrentIndex(0)
        self.btnNew.clicked.connect(MainWindow.slot_new_query)
        self.btnQuery.clicked.connect(MainWindow.slot_run_sql_query)
        self.tabQuery.tabCloseRequested['int'].connect(MainWindow.slot_tab_sql_close)
        self.actionImport.triggered.connect(MainWindow.slot_action_import)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.geText.setText(_translate("MainWindow", "Greater than or equal to"))
        self.geTime.setDisplayFormat(_translate("MainWindow", "yyyy/M/d HH:mm:ss"))
        self.leText.setText(_translate("MainWindow", "Less than or equal to"))
        self.leTime.setDisplayFormat(_translate("MainWindow", "yyyy/M/d HH:mm:ss"))
        self.btnNew.setText(_translate("MainWindow", "New"))
        self.btnQuery.setText(_translate("MainWindow", "Query"))
        self.tabQuery.setTabText(self.tabQuery.indexOf(self.tab_1), _translate("MainWindow", "Tab 1"))
        self.treeList.headerItem().setText(0, _translate("MainWindow", "Database Tree"))
        self.tabResult.setTabText(self.tabResult.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        self.tabResult.setTabText(self.tabResult.indexOf(self.tab_4), _translate("MainWindow", "Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setToolTip(_translate("MainWindow", "Import"))
