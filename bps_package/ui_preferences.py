# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Mon Sep 23 18:54:04 2013
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PrefDialog(object):
    def setupUi(self, PrefDialog):
        PrefDialog.setObjectName(_fromUtf8("PrefDialog"))
        PrefDialog.resize(640, 480)
        self.verticalLayout = QtGui.QVBoxLayout(PrefDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(PrefDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.habitatTab = QtGui.QWidget()
        self.habitatTab.setObjectName(_fromUtf8("habitatTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.habitatTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.habkeditlistbox = KEditListBox(self.habitatTab)
        self.habkeditlistbox.setObjectName(_fromUtf8("habkeditlistbox"))
        self.gridLayout_2.addWidget(self.habkeditlistbox, 0, 0, 1, 1)
        self.tabWidget.addTab(self.habitatTab, _fromUtf8(""))
        self.habitatColorTab = QtGui.QWidget()
        self.habitatColorTab.setObjectName(_fromUtf8("habitatColorTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.habitatColorTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.habitatColorTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.kcolorbutton = KColorButton(self.habitatColorTab)
        self.kcolorbutton.setObjectName(_fromUtf8("kcolorbutton"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.kcolorbutton)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.habitatColorTab, _fromUtf8(""))
        self.substrateTab = QtGui.QWidget()
        self.substrateTab.setObjectName(_fromUtf8("substrateTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.substrateTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.substkeditlistwidget = KEditListWidget(self.substrateTab)
        self.substkeditlistwidget.setObjectName(_fromUtf8("substkeditlistwidget"))
        self.gridLayout_4.addWidget(self.substkeditlistwidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.substrateTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(PrefDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PrefDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrefDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrefDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrefDialog)

    def retranslateUi(self, PrefDialog):
        PrefDialog.setWindowTitle(QtGui.QApplication.translate("PrefDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.habitatTab.setToolTip(QtGui.QApplication.translate("PrefDialog", "<html><head/><body><p>Habitat</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.habitatTab.setAccessibleName(QtGui.QApplication.translate("PrefDialog", "Habitat", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatTab), QtGui.QApplication.translate("PrefDialog", "Habitats", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PrefDialog", "Placeholder", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatColorTab), QtGui.QApplication.translate("PrefDialog", "Habitat Colors", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.substrateTab), QtGui.QApplication.translate("PrefDialog", "Substrates", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KEditListWidget, KColorButton, KEditListBox
