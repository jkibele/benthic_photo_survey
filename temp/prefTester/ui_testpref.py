# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testpref.ui'
#
# Created: Fri Oct  4 16:41:03 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(504, 424)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName(_fromUtf8("generalTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.generalTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.workingDirLabel = QtGui.QLabel(self.generalTab)
        self.workingDirLabel.setObjectName(_fromUtf8("workingDirLabel"))
        self.gridLayout_2.addWidget(self.workingDirLabel, 1, 0, 1, 1)
        self.outputEPSGLineEdit = QtGui.QLineEdit(self.generalTab)
        self.outputEPSGLineEdit.setObjectName(_fromUtf8("outputEPSGLineEdit"))
        self.gridLayout_2.addWidget(self.outputEPSGLineEdit, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 154, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.generalTab)
        self.pushButton.setMaximumSize(QtCore.QSize(85, 16777215))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout_2.addWidget(self.pushButton, 5, 0, 1, 1)
        self.inputEPSGLabel = QtGui.QLabel(self.generalTab)
        self.inputEPSGLabel.setObjectName(_fromUtf8("inputEPSGLabel"))
        self.gridLayout_2.addWidget(self.inputEPSGLabel, 2, 0, 1, 1)
        self.toolButton = QtGui.QToolButton(self.generalTab)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_2.addWidget(self.toolButton, 0, 2, 1, 1)
        self.workingDirLineEdit = QtGui.QLineEdit(self.generalTab)
        self.workingDirLineEdit.setReadOnly(True)
        self.workingDirLineEdit.setObjectName(_fromUtf8("workingDirLineEdit"))
        self.gridLayout_2.addWidget(self.workingDirLineEdit, 1, 1, 1, 1)
        self.lineEdit_3 = QtGui.QLineEdit(self.generalTab)
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.gridLayout_2.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.generalTab)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout_2.addWidget(self.toolButton_2, 1, 2, 1, 1)
        self.databaseLabel = QtGui.QLabel(self.generalTab)
        self.databaseLabel.setObjectName(_fromUtf8("databaseLabel"))
        self.gridLayout_2.addWidget(self.databaseLabel, 0, 0, 1, 1)
        self.outputEPSGLabel = QtGui.QLabel(self.generalTab)
        self.outputEPSGLabel.setObjectName(_fromUtf8("outputEPSGLabel"))
        self.gridLayout_2.addWidget(self.outputEPSGLabel, 3, 0, 1, 1)
        self.databaseLineEdit = QtGui.QLineEdit(self.generalTab)
        self.databaseLineEdit.setReadOnly(True)
        self.databaseLineEdit.setObjectName(_fromUtf8("databaseLineEdit"))
        self.gridLayout_2.addWidget(self.databaseLineEdit, 0, 1, 1, 1)
        self.tabWidget.addTab(self.generalTab, _fromUtf8(""))
        self.timezoneTab = QtGui.QWidget()
        self.timezoneTab.setObjectName(_fromUtf8("timezoneTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.timezoneTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.timezoneTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.ktimezonewidget = KTimeZoneWidget(self.timezoneTab)
        self.ktimezonewidget.setObjectName(_fromUtf8("ktimezonewidget"))
        self.ktimezonewidget.headerItem().setText(0, _fromUtf8("1"))
        self.ktimezonewidget.headerItem().setText(1, _fromUtf8("2"))
        self.ktimezonewidget.headerItem().setText(2, _fromUtf8("3"))
        self.gridLayout_3.addWidget(self.ktimezonewidget, 1, 0, 1, 2)
        self.pushButton_2 = QtGui.QPushButton(self.timezoneTab)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_3.addWidget(self.pushButton_2, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(370, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 2, 1, 1, 1)
        self.tabWidget.addTab(self.timezoneTab, _fromUtf8(""))
        self.habitatTab = QtGui.QWidget()
        self.habitatTab.setObjectName(_fromUtf8("habitatTab"))
        self.gridLayout = QtGui.QGridLayout(self.habitatTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.habTableWidget = QtGui.QTableWidget(self.habitatTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.habTableWidget.sizePolicy().hasHeightForWidth())
        self.habTableWidget.setSizePolicy(sizePolicy)
        self.habTableWidget.setMinimumSize(QtCore.QSize(347, 0))
        self.habTableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.habTableWidget.setColumnCount(3)
        self.habTableWidget.setObjectName(_fromUtf8("habTableWidget"))
        self.habTableWidget.setRowCount(0)
        self.habTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.habTableWidget.horizontalHeader().setDefaultSectionSize(110)
        self.habTableWidget.horizontalHeader().setStretchLastSection(True)
        self.habTableWidget.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.habTableWidget, 0, 0, 3, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.habAddButton = QtGui.QPushButton(self.habitatTab)
        self.habAddButton.setObjectName(_fromUtf8("habAddButton"))
        self.verticalLayout.addWidget(self.habAddButton)
        self.habRemoveButton = QtGui.QPushButton(self.habitatTab)
        self.habRemoveButton.setObjectName(_fromUtf8("habRemoveButton"))
        self.verticalLayout.addWidget(self.habRemoveButton)
        self.habUpButton = QtGui.QPushButton(self.habitatTab)
        self.habUpButton.setObjectName(_fromUtf8("habUpButton"))
        self.verticalLayout.addWidget(self.habUpButton)
        self.habDownButton = QtGui.QPushButton(self.habitatTab)
        self.habDownButton.setObjectName(_fromUtf8("habDownButton"))
        self.verticalLayout.addWidget(self.habDownButton)
        self.habColorButton = QtGui.QPushButton(self.habitatTab)
        self.habColorButton.setObjectName(_fromUtf8("habColorButton"))
        self.verticalLayout.addWidget(self.habColorButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 142, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.habHelpButton = QtGui.QPushButton(self.habitatTab)
        self.habHelpButton.setObjectName(_fromUtf8("habHelpButton"))
        self.gridLayout.addWidget(self.habHelpButton, 2, 1, 1, 1)
        self.tabWidget.addTab(self.habitatTab, _fromUtf8(""))
        self.substratesTab = QtGui.QWidget()
        self.substratesTab.setObjectName(_fromUtf8("substratesTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.substratesTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.keditlistwidget = KEditListWidget(self.substratesTab)
        self.keditlistwidget.setObjectName(_fromUtf8("keditlistwidget"))
        self.gridLayout_4.addWidget(self.keditlistwidget, 0, 0, 1, 2)
        self.pushButton_3 = QtGui.QPushButton(self.substratesTab)
        self.pushButton_3.setMaximumSize(QtCore.QSize(85, 16777215))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_4.addWidget(self.pushButton_3, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(370, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 1, 1, 1, 1)
        self.tabWidget.addTab(self.substratesTab, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.habAddButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.addHabRow)
        QtCore.QObject.connect(self.habRemoveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.removeHabRow)
        QtCore.QObject.connect(self.habUpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.moveHabUp)
        QtCore.QObject.connect(self.habDownButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.moveHabDown)
        QtCore.QObject.connect(self.habColorButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.changeHabColor)
        QtCore.QObject.connect(self.habHelpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.habHelp)
        QtCore.QObject.connect(self.habTableWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QTableWidgetItem*)")), Dialog.habItemDoubleClicked)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.generalHelp)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.timezoneHelp)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.substratesHelp)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.generalChooseDB)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.generalChooseWorkingDir)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.workingDirLabel.setText(QtGui.QApplication.translate("Dialog", "Working Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Help?", None, QtGui.QApplication.UnicodeUTF8))
        self.inputEPSGLabel.setText(QtGui.QApplication.translate("Dialog", "Input EPSG", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.databaseLabel.setText(QtGui.QApplication.translate("Dialog", "Database", None, QtGui.QApplication.UnicodeUTF8))
        self.outputEPSGLabel.setText(QtGui.QApplication.translate("Dialog", "Output EPSG", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), QtGui.QApplication.translate("Dialog", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Choose the time zone you are working in", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Help?", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timezoneTab), QtGui.QApplication.translate("Dialog", "Time Zone", None, QtGui.QApplication.UnicodeUTF8))
        self.habAddButton.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.habRemoveButton.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.habUpButton.setText(QtGui.QApplication.translate("Dialog", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.habDownButton.setText(QtGui.QApplication.translate("Dialog", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.habColorButton.setText(QtGui.QApplication.translate("Dialog", "Choose Color", None, QtGui.QApplication.UnicodeUTF8))
        self.habHelpButton.setText(QtGui.QApplication.translate("Dialog", "Help?", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatTab), QtGui.QApplication.translate("Dialog", "Habitats", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Dialog", "Help?", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.substratesTab), QtGui.QApplication.translate("Dialog", "Substrates", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KTimeZoneWidget, KEditListWidget
