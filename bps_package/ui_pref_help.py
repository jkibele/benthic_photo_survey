# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pref_help.ui'
#
# Created: Tue Dec  9 19:51:38 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PrefHelpDialog(object):
    def setupUi(self, PrefHelpDialog):
        PrefHelpDialog.setObjectName(_fromUtf8("PrefHelpDialog"))
        PrefHelpDialog.resize(447, 326)
        self.verticalLayout = QtGui.QVBoxLayout(PrefHelpDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = QtGui.QTextBrowser(PrefHelpDialog)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtGui.QDialogButtonBox(PrefHelpDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PrefHelpDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrefHelpDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrefHelpDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrefHelpDialog)

    def retranslateUi(self, PrefHelpDialog):
        PrefHelpDialog.setWindowTitle(_translate("PrefHelpDialog", "BPS Help", None))

