# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testpref.ui'
#
# Created: Fri Sep 27 17:45:17 2013
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
        Dialog.resize(531, 480)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.habitatTab = QtGui.QWidget()
        self.habitatTab.setObjectName(_fromUtf8("habitatTab"))
        self.gridLayout = QtGui.QGridLayout(self.habitatTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.habHelpButton = QtGui.QPushButton(self.habitatTab)
        self.habHelpButton.setObjectName(_fromUtf8("habHelpButton"))
        self.verticalLayout.addWidget(self.habHelpButton)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 142, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.habLineEdit = QtGui.QLineEdit(self.habitatTab)
        self.habLineEdit.setObjectName(_fromUtf8("habLineEdit"))
        self.gridLayout.addWidget(self.habLineEdit, 0, 0, 1, 2)
        self.habTableWidget = QtGui.QTableWidget(self.habitatTab)
        self.habTableWidget.setObjectName(_fromUtf8("habTableWidget"))
        self.habTableWidget.setColumnCount(0)
        self.habTableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.habTableWidget, 1, 0, 2, 1)
        self.tabWidget.addTab(self.habitatTab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
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
        QtCore.QObject.connect(self.habLineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Dialog.addHabRow)
        QtCore.QObject.connect(self.habColorButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.changeHabColor)
        QtCore.QObject.connect(self.habHelpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.habHelp)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.habAddButton.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.habRemoveButton.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.habUpButton.setText(QtGui.QApplication.translate("Dialog", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.habDownButton.setText(QtGui.QApplication.translate("Dialog", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.habColorButton.setText(QtGui.QApplication.translate("Dialog", "Change Color", None, QtGui.QApplication.UnicodeUTF8))
        self.habHelpButton.setText(QtGui.QApplication.translate("Dialog", "Help?", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatTab), QtGui.QApplication.translate("Dialog", "Habitats", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "Tab 2", None, QtGui.QApplication.UnicodeUTF8))

