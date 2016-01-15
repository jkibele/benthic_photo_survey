# -*- coding: utf-8 -*-
"""
Copyright (c) 2014, Jared Kibele
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of Benthic Photo Survey nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Sun Mar  8 18:17:55 2015
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

class Ui_PrefDialog(object):
    def setupUi(self, PrefDialog):
        PrefDialog.setObjectName(_fromUtf8("PrefDialog"))
        PrefDialog.resize(504, 424)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PrefDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(PrefDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.generalTab = QtGui.QWidget()
        self.generalTab.setObjectName(_fromUtf8("generalTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.generalTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.outputEPSGLineEdit = QtGui.QLineEdit(self.generalTab)
        self.outputEPSGLineEdit.setObjectName(_fromUtf8("outputEPSGLineEdit"))
        self.gridLayout_2.addWidget(self.outputEPSGLineEdit, 3, 2, 1, 1)
        self.databaseLabel = QtGui.QLabel(self.generalTab)
        self.databaseLabel.setObjectName(_fromUtf8("databaseLabel"))
        self.gridLayout_2.addWidget(self.databaseLabel, 0, 0, 1, 1)
        self.workingDirLabel = QtGui.QLabel(self.generalTab)
        self.workingDirLabel.setObjectName(_fromUtf8("workingDirLabel"))
        self.gridLayout_2.addWidget(self.workingDirLabel, 1, 0, 1, 1)
        self.toolButton = QtGui.QToolButton(self.generalTab)
        self.toolButton.setObjectName(_fromUtf8("toolButton"))
        self.gridLayout_2.addWidget(self.toolButton, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.generalTab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)
        self.databaseLineEdit = QtGui.QLineEdit(self.generalTab)
        self.databaseLineEdit.setReadOnly(True)
        self.databaseLineEdit.setObjectName(_fromUtf8("databaseLineEdit"))
        self.gridLayout_2.addWidget(self.databaseLineEdit, 0, 2, 1, 1)
        self.generalHelpButton = QtGui.QPushButton(self.generalTab)
        self.generalHelpButton.setMaximumSize(QtCore.QSize(85, 16777215))
        self.generalHelpButton.setObjectName(_fromUtf8("generalHelpButton"))
        self.gridLayout_2.addWidget(self.generalHelpButton, 6, 0, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(self.generalTab)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.gridLayout_2.addWidget(self.toolButton_2, 1, 3, 1, 1)
        self.outputEPSGLabel = QtGui.QLabel(self.generalTab)
        self.outputEPSGLabel.setObjectName(_fromUtf8("outputEPSGLabel"))
        self.gridLayout_2.addWidget(self.outputEPSGLabel, 3, 0, 1, 1)
        self.inputEPSGLineEdit = QtGui.QLineEdit(self.generalTab)
        self.inputEPSGLineEdit.setObjectName(_fromUtf8("inputEPSGLineEdit"))
        self.gridLayout_2.addWidget(self.inputEPSGLineEdit, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 154, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.inputEPSGLabel = QtGui.QLabel(self.generalTab)
        self.inputEPSGLabel.setObjectName(_fromUtf8("inputEPSGLabel"))
        self.gridLayout_2.addWidget(self.inputEPSGLabel, 2, 0, 1, 1)
        self.workingDirLineEdit = QtGui.QLineEdit(self.generalTab)
        self.workingDirLineEdit.setReadOnly(True)
        self.workingDirLineEdit.setObjectName(_fromUtf8("workingDirLineEdit"))
        self.gridLayout_2.addWidget(self.workingDirLineEdit, 1, 2, 1, 1)
        self.dodgyCheckBox = QtGui.QCheckBox(self.generalTab)
        self.dodgyCheckBox.setObjectName(_fromUtf8("dodgyCheckBox"))
        self.gridLayout_2.addWidget(self.dodgyCheckBox, 4, 2, 1, 1)
        self.tabWidget.addTab(self.generalTab, _fromUtf8(""))
        self.timezoneTab = QtGui.QWidget()
        self.timezoneTab.setObjectName(_fromUtf8("timezoneTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.timezoneTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(370, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 3, 1, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.timezoneTab)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout_3.addWidget(self.pushButton_2, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.timezoneTab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)
        self.timeZoneComboBox = QtGui.QComboBox(self.timezoneTab)
        self.timeZoneComboBox.setObjectName(_fromUtf8("timeZoneComboBox"))
        self.gridLayout_3.addWidget(self.timeZoneComboBox, 1, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 2, 0, 1, 1)
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
        spacerItem3 = QtGui.QSpacerItem(20, 142, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 1, 1, 1)
        self.habHelpButton = QtGui.QPushButton(self.habitatTab)
        self.habHelpButton.setObjectName(_fromUtf8("habHelpButton"))
        self.gridLayout.addWidget(self.habHelpButton, 2, 1, 1, 1)
        self.tabWidget.addTab(self.habitatTab, _fromUtf8(""))
        self.substratesTab = QtGui.QWidget()
        self.substratesTab.setObjectName(_fromUtf8("substratesTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.substratesTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(370, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem4, 2, 1, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.substratesTab)
        self.pushButton_3.setMaximumSize(QtCore.QSize(85, 16777215))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout_4.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.substrateListWidget = QtGui.QListWidget(self.substratesTab)
        self.substrateListWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.substrateListWidget.setObjectName(_fromUtf8("substrateListWidget"))
        self.horizontalLayout.addWidget(self.substrateListWidget)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.substAddButton = QtGui.QPushButton(self.substratesTab)
        self.substAddButton.setObjectName(_fromUtf8("substAddButton"))
        self.verticalLayout_4.addWidget(self.substAddButton)
        self.substEditButton = QtGui.QPushButton(self.substratesTab)
        self.substEditButton.setObjectName(_fromUtf8("substEditButton"))
        self.verticalLayout_4.addWidget(self.substEditButton)
        self.substRemoveButton = QtGui.QPushButton(self.substratesTab)
        self.substRemoveButton.setObjectName(_fromUtf8("substRemoveButton"))
        self.verticalLayout_4.addWidget(self.substRemoveButton)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.gridLayout_4.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.tabWidget.addTab(self.substratesTab, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(PrefDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(PrefDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PrefDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PrefDialog.reject)
        QtCore.QObject.connect(self.habAddButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.addHabRow)
        QtCore.QObject.connect(self.habRemoveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.removeHabRow)
        QtCore.QObject.connect(self.habUpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.moveHabUp)
        QtCore.QObject.connect(self.habDownButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.moveHabDown)
        QtCore.QObject.connect(self.habColorButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.changeHabColor)
        QtCore.QObject.connect(self.habHelpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.habHelp)
        QtCore.QObject.connect(self.habTableWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QTableWidgetItem*)")), PrefDialog.habItemDoubleClicked)
        QtCore.QObject.connect(self.generalHelpButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.generalHelp)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.timezoneHelp)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.substratesHelp)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.generalChooseDB)
        QtCore.QObject.connect(self.toolButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.generalChooseWorkingDir)
        QtCore.QObject.connect(self.substAddButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.substAdd)
        QtCore.QObject.connect(self.substEditButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.substEdit)
        QtCore.QObject.connect(self.substRemoveButton, QtCore.SIGNAL(_fromUtf8("clicked()")), PrefDialog.substRemove)
        QtCore.QObject.connect(self.substrateListWidget, QtCore.SIGNAL(_fromUtf8("itemDoubleClicked(QListWidgetItem*)")), PrefDialog.substEdit)
        QtCore.QMetaObject.connectSlotsByName(PrefDialog)

    def retranslateUi(self, PrefDialog):
        PrefDialog.setWindowTitle(_translate("PrefDialog", "Preferences", None))
        self.databaseLabel.setText(_translate("PrefDialog", "Database", None))
        self.workingDirLabel.setText(_translate("PrefDialog", "Working Directory", None))
        self.toolButton.setText(_translate("PrefDialog", "...", None))
        self.label_2.setText(_translate("PrefDialog", "Dodgy Features", None))
        self.generalHelpButton.setText(_translate("PrefDialog", "Help?", None))
        self.toolButton_2.setText(_translate("PrefDialog", "...", None))
        self.outputEPSGLabel.setText(_translate("PrefDialog", "Output EPSG", None))
        self.inputEPSGLabel.setText(_translate("PrefDialog", "Input EPSG", None))
        self.dodgyCheckBox.setText(_translate("PrefDialog", "Enable sketchy advanced features", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("PrefDialog", "General", None))
        self.pushButton_2.setText(_translate("PrefDialog", "Help?", None))
        self.label.setText(_translate("PrefDialog", "Choose the time zone you are working in", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.timezoneTab), _translate("PrefDialog", "Time Zone", None))
        self.habAddButton.setText(_translate("PrefDialog", "Add", None))
        self.habRemoveButton.setText(_translate("PrefDialog", "Remove", None))
        self.habUpButton.setText(_translate("PrefDialog", "Move Up", None))
        self.habDownButton.setText(_translate("PrefDialog", "Move Down", None))
        self.habColorButton.setText(_translate("PrefDialog", "Choose Color", None))
        self.habHelpButton.setText(_translate("PrefDialog", "Help?", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.habitatTab), _translate("PrefDialog", "Habitats", None))
        self.pushButton_3.setText(_translate("PrefDialog", "Help?", None))
        self.substAddButton.setText(_translate("PrefDialog", "Add", None))
        self.substEditButton.setText(_translate("PrefDialog", "Edit", None))
        self.substRemoveButton.setText(_translate("PrefDialog", "Remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.substratesTab), _translate("PrefDialog", "Substrates", None))
