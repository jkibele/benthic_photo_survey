# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testpref.ui'
#
# Created: Thu Sep 26 14:25:59 2013
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
        Dialog.resize(640, 480)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)
        self.tableWidget = QtGui.QTableWidget(self.groupBox)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 2, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addButton = QtGui.QPushButton(self.groupBox)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(self.groupBox)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout.addWidget(self.removeButton)
        self.upButton = QtGui.QPushButton(self.groupBox)
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.verticalLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(self.groupBox)
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.verticalLayout.addWidget(self.downButton)
        self.colorButton = QtGui.QPushButton(self.groupBox)
        self.colorButton.setObjectName(_fromUtf8("colorButton"))
        self.verticalLayout.addWidget(self.colorButton)
        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 190, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.addRow)
        QtCore.QObject.connect(self.removeButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.removeRow)
        QtCore.QObject.connect(self.upButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.moveUp)
        QtCore.QObject.connect(self.downButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.moveDown)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("returnPressed()")), Dialog.addRow)
        QtCore.QObject.connect(self.colorButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.changeColor)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "GroupBox", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.upButton.setText(QtGui.QApplication.translate("Dialog", "Move Up", None, QtGui.QApplication.UnicodeUTF8))
        self.downButton.setText(QtGui.QApplication.translate("Dialog", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.colorButton.setText(QtGui.QApplication.translate("Dialog", "Change Color", None, QtGui.QApplication.UnicodeUTF8))

