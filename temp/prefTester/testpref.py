#!/usr/bin/env python
import sys, json
from PyQt4 import QtCore
from PyQt4.QtCore import QSettings, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox, QDialog, QColor, QColorDialog, QTableWidgetItem
from ui_mainwindow import Ui_MainWindow
from ui_testpref import Ui_Dialog

class PrefRow(object):
    def __init__(self,name=None,code=None,color=None):
        """
        name and color will be strings. code will be an int.
        """
        self.name = name
        self.code = code
        self.color = color
        
    def __repr__(self):
        return str( self.toList() )
        
    def toList(self):
        return [self.name,self.code,self.color]
        
    def fromList(self,inlist):
        self.name = inlist[0]
        self.code = inlist[1]
        self.color = inlist[2]
        
    @property
    def q_color(self):
        return QColor( self.color )
        
    def addToTableWidget(self,widget,rownum):
        itemlist = [self.code,self.name,self.color]
        for i,thing in enumerate(itemlist):
            item = QTableWidgetItem( thing )
            if i==len(itemlist)-1:
                item.setBackgroundColor( QColor(self.color) )
            widget.setItem(rownum,i,item)
        
class PrefArray(object):
    def __init__(self,rowList=None):
        if rowList:        
            self.rows = rowList
        else:
            self.rows = []
        
    def __repr__(self):
        return str( self.rows )
        
    def addrow(self, pref_row):
        self.rows.append(pref_row)
        
    def addToTableWidget(self,widget):
        for i,row in enumerate(self.rows):
            row.addToTableWidget(widget,i)
        
    def saveToSettings(self,settings,setting_tag):
        json_str = json.dumps( self.toList() )
        settings.setValue( setting_tag, json_str )
        
    def loadFromSettings(self,settings,setting_tag):
        json_str = str( settings.value(setting_tag,'[[null, null, null]]').toString() )
        self.fromJson(json_str)
        
    def fromJson(self,json_str):
        """
        Take a json string and load it into a list of rows. Then load that into
        PrefRows and load those into a PrefArray.
        """
        # turn the json into a list of lists (rows)
        print json_str
        jlist = json.loads(json_str)
        self.clear()
        for row in jlist:
            pr = PrefRow()
            pr.fromList( row )
            self.addrow( pr )
        
    def clear(self):
        """
        Clear out all data.
        """
        self.rows = []
    
    def toList(self):
        outlist = []
        for r in self.rows:
            outlist.append(r.toList())
        return outlist
        
    @property
    def rowCount(self):
        return len(self.rows)

class StartPrefs(QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.settings = QSettings("test","tpref2")
        self.habPrefArray = PrefArray()
        self.habPrefArray.loadFromSettings(self.settings,"tpref2")
        # setup habitat table
        self.habTableWidget.setColumnCount(3)
        self.habTableWidget.setRowCount(self.habPrefArray.rowCount)
        self.habPrefArray.addToTableWidget(self.habTableWidget)
        self.habTableWidget.setHorizontalHeaderLabels(["Code","Habitat","Color"])
    
    def addHabRow(self):
        if self.habLineEdit.text():
            newRow = PrefRow(name=self.habLineEdit.text())
            newRow.addToTableWidget(self.habTableWidget)
    
    def removeHabRow(self):
        pass
    
    def moveHabUp(self):
        pass
    
    def moveHabDown(self):
        pass
    
    def changeHabColor(self):
        pass
    
    def habHelp(self):
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