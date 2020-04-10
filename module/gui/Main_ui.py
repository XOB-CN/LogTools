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
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
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
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(9)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeList = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeList.sizePolicy().hasHeightForWidth())
        self.treeList.setSizePolicy(sizePolicy)
        self.treeList.setMinimumSize(QtCore.QSize(150, 0))
        self.treeList.setMaximumSize(QtCore.QSize(250, 16777215))
        self.treeList.setObjectName("treeList")
        self.tabQuery = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabQuery.sizePolicy().hasHeightForWidth())
        self.tabQuery.setSizePolicy(sizePolicy)
        self.tabQuery.setTabsClosable(True)
        self.tabQuery.setTabBarAutoHide(False)
        self.tabQuery.setObjectName("tabQuery")
        self.SQL_Query_1 = QtWidgets.QWidget()
        self.SQL_Query_1.setObjectName("SQL_Query_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.SQL_Query_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.sqlEdit1 = QtWidgets.QTextEdit(self.SQL_Query_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sqlEdit1.sizePolicy().hasHeightForWidth())
        self.sqlEdit1.setSizePolicy(sizePolicy)
        self.sqlEdit1.setObjectName("sqlEdit1")
        self.gridLayout_2.addWidget(self.sqlEdit1, 0, 0, 1, 1)
        self.tabQuery.addTab(self.SQL_Query_1, "")
        self.tabResult = QtWidgets.QTabWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabResult.sizePolicy().hasHeightForWidth())
        self.tabResult.setSizePolicy(sizePolicy)
        self.tabResult.setTabsClosable(True)
        self.tabResult.setTabBarAutoHide(False)
        self.tabResult.setObjectName("tabResult")
        self.verticalLayout.addWidget(self.splitter_2)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
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
        self.tabResult.setCurrentIndex(-1)
        self.actionImport.triggered.connect(MainWindow.slot_action_import)
        self.btnNew.clicked.connect(MainWindow.slot_new_query)
        self.treeList.itemDoubleClicked['QTreeWidgetItem*','int'].connect(MainWindow.slot_dblist_sql_query)
        self.tabQuery.tabCloseRequested['int'].connect(MainWindow.slot_tab_sql_close)
        self.btnQuery.clicked.connect(MainWindow.slot_run_sql_query)
        self.tabResult.tabCloseRequested['int'].connect(MainWindow.slot_tab_result_close)
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
        self.treeList.headerItem().setText(0, _translate("MainWindow", "Database Tree"))
        self.tabQuery.setTabText(self.tabQuery.indexOf(self.SQL_Query_1), _translate("MainWindow", "SQL_Query_1"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionImport.setText(_translate("MainWindow", "Import"))
        self.actionImport.setToolTip(_translate("MainWindow", "Import"))
