#!/usr/bin/env python
import sys
from PyQt4 import QtCore
from PyQt4.QtCore import QSettings, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox, QDialog, QColor, QColorDialog
from ui_mainwindow import Ui_MainWindow
from ui_testpref import Ui_Dialog

class prefRow(object):
    def __init__(self,name=None,code=None,color=None):
        """
        name and color will be strings. code will be an int.
        """
        self.name = name
        self.code = code
        self.color = color
        
    def toList(self):
        return [self.name,self.code,self.color]
        
    @property
    def q_color(self):
        return QColor( self.color )
        
class prefArray(object):
    def __init__(self,rowList=None):
        self.rows = rowList
        
    def __repr__(self):
        return self.rows

class StartPrefs(QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.settings = QSettings("jkibele","TestPref")
    
    def addRow(self):
        pass
    
    def removeRow(self):
        pass
    
    def moveUp(self):
        pass
    
    def moveDown(self):
        pass
    
    def changeColor(self):
        pass

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        #self.settings = QSettings("jkibele","TestPref")                                    
        self.setupUi(self)

    def prefTest(self):
        #write this dialog launching code
        dlg = StartPrefs(parent=self)
        dlg.exec_()
        if dlg.Accepted==1:
            self.applySettings()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()