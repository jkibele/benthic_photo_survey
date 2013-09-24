# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Tue Sep 24 14:21:54 2013
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
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.habitatTab)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.habkeditlistbox = KEditListWidget(self.habitatTab)
        self.habkeditlistbox.setObjectName(_fromUtf8("habkeditlistbox"))
        self.horizontalLayout_3.addWidget(self.habkeditlistbox)
        self.tabWidget.addTab(self.habitatTab, _fromUtf8(""))
        self.substrateTab = QtGui.QWidget()
        self.substrateTab.setObjectName(_fromUtf8("substrateTab"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.substrateTab)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.substkeditlistwidget = KEditListWidget(self.substrateTab)
        self.substkeditlistwidget.setObjectName(_fromUtf8("substkeditlistwidget"))
        self.horizontalLayout_4.addWidget(self.substkeditlistwidget)
        self.tabWidget.addTab(self.substrateTab, _fromUtf8(""))
        self.itemColorTab = QtGui.QWidget()
        self.itemColorTab.setObjectName(_fromUtf8("itemColorTab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.itemColorTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.habColorGroupBox = QtGui.QGroupBox(self.itemColorTab)
        self.habColorGroupBox.setObjectName(_fromUtf8("habColorGroupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.habColorGroupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.habColorListWidget = QtGui.QListWidget(self.habColorGroupBox)
        self.habColorListWidget.setObjectName(_fromUtf8("habColorListWidget"))
        self.verticalLayout_2.addWidget(self.habColorListWidget)
        self.horizontalLayout_2.addWidget(self.habColorGroupBox)
        self.substColorGroupBox = QtGui.QGroupBox(self.itemColorTab)
        self.substColorGroupBox.setObjectName(_fromUtf8("substColorGroupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.substColorGroupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.substColorListWidget = QtGui.QListWidget(self.substColorGroupBox)
        self.substColorListWidget.setObjectName(_fromUtf8("substColorListWidget"))
        self.verticalLayout_3.addWidget(self.substColorListWidget)
        self.horizontalLayout_2.addWidget(self.substColorGroupBox)
        self.tabWidget.addTab(self.itemColorTab, _fromUtf8(""))
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
        QtCore.QObject.connect(self.habColorListWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), PrefDialog.editItemColor)
        QtCore.QObject.connect(self.tabWidget, QtCore.SIGNAL(_fromUtf8("currentChanged(int)")), PrefDialog.updateColorList)
        QtCore.QMetaObject.connectSlotsByName(PrefDialog)

    def retranslateUi(self, PrefDialog):
        PrefDialog.setWindowTitle(QtGui.QApplication.translate("PrefDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.habitatTab.setToolTip(QtGui.QApplication.translate("PrefDialog", "<html><head/><body><p>Habitat</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.habitatTab.setAccessibleName(QtGui.QApplication.translate("PrefDialog", "Habitat", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatTab), QtGui.QApplication.translate("PrefDialog", "Habitats", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.substrateTab), QtGui.QApplication.translate("PrefDialog", "Substrates", None, QtGui.QApplication.UnicodeUTF8))
        self.habColorGroupBox.setTitle(QtGui.QApplication.translate("PrefDialog", "Habitat Colors", None, QtGui.QApplication.UnicodeUTF8))
        self.substColorGroupBox.setTitle(QtGui.QApplication.translate("PrefDialog", "Substrate Colors", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.itemColorTab), QtGui.QApplication.translate("PrefDialog", "Colors", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KEditListWidget
