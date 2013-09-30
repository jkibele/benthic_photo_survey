#!/usr/bin/env python
import sys, json
from PyQt4 import QtCore
from PyQt4.QtCore import QSettings, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox, QDialog, QColor, QColorDialog, QTableWidgetItem
from ui_mainwindow import Ui_MainWindow
from ui_testpref import Ui_Dialog

class PrefRow(object):
    def __init__(self,name=None,code=None,color=None,parent=None):
        """
        name and color will be strings. code will be an int.
        """
        self.name = name
        self.code = code
        if color:
            self.color = color
        else:
            self.color = u'#000000'
        self.parent = parent
        
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
        try:
            return QColor( self.color )
        except:
            return False
    
    @property
    def validName(self):
        try:
            str(self.name)
            return True
        except:
            return False
            
    @property
    def validCode(self):
        if type(self.code)==int:
            return True
        else:
            return False
        
    @property
    def validColor(self):
        if self.color:
            return True
        else:
            return False
        
    @property
    def isValid(self):
        """
        Can these values be added?
        """
        if self.validName and self.validCode and self.validColor:
            return True
        else:
            return False
        
    def addToTableWidget(self,widget,rownum):
        self.setCode()
        self.setColor()
        itemlist = [self.code,self.name,self.color]
        print itemlist
        for i,thing in enumerate(itemlist):
            item = QTableWidgetItem( thing )
            if i==len(itemlist)-1:
                item.setBackgroundColor( self.q_color )
            print "Adding %s to row %i" % (item.text(),rownum)
            widget.setItem(rownum,i,item)
            
    def setCode(self):
        if not self.code:
            self.code = 1
            
    def setColor(self):
        if not self.validColor:
            self.color = "#247612"
            
        
class PrefArray(object):
    """
    An object that ties my preferences dialog to settings.
    """
    def __init__(self,rowList=None,settings=None,settings_tag=None,widget=None):
        if rowList:        
            self.rows = rowList
        else:
            self.rows = []
        self.settings = settings
        self.settings_tag = settings_tag
        self.widget = widget
        self.__set_row_parent()
        
    def __repr__(self):
        return str( self.rows )
        
    def __set_row_parent(self):
        for r in self.rows:
            r.parent = self
        
    @property
    def rowsValid(self):
        if False in [r.isValid for r in self.rows]:
            return False
        else:
            return True
        
    def addrow(self, pref_row):
        pref_row.parent = self
        self.rows.append(pref_row)
        
    def addToTableWidget(self):
        for i,row in enumerate(self.rows):
            row.addToTableWidget(self.widget,i)
        
    def saveToSettings(self):
        json_str = json.dumps( self.toList() )
        self.settings.setValue( self.settings_tag, json_str )
        
    def loadFromSettings(self):
        json_str = str( self.settings.value(self.settings_tag,'[[null, null, null]]').toString() )
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
        
class HabPrefArray(PrefArray):
    """
    A PrefArray that's pre-populated with habitat preference specific values.
    """
    def __init__(self,rowList=None, widget=None):
        qset = QSettings("test","tpref2")
        stag = "tpref2"
        super(HabPrefArray, self).__init__(rowList=rowList,settings=qset,settings_tag=stag,widget=widget)

class StartPrefs(QDialog, Ui_Dialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.settings = QSettings("test","tpref2")
        self.habPrefArray = HabPrefArray(widget=self.habTableWidget)
        self.habPrefArray.loadFromSettings()
        # setup habitat table
        self.habTableWidget.setColumnCount(3)
        self.habTableWidget.setRowCount(self.habPrefArray.rowCount)
        if self.habPrefArray.rowsValid:
            self.habPrefArray.addToTableWidget()
        self.habTableWidget.setHorizontalHeaderLabels(["Code","Habitat","Color"])
    
    def addHabRow(self):
        if self.habLineEdit.text():
            newRow = PrefRow(name=unicode(self.habLineEdit.text()) )
            self.habTableWidget.setRowCount( self.habTableWidget.rowCount() + 1 )
            newRow.addToTableWidget(self.habTableWidget,self.habTableWidget.rowCount())
    
    def removeHabRow(self):
        pass
    
    def moveHabUp(self):
        pass
    
    def moveHabDown(self):
        pass
    
    def changeHabColor(self):
        pass
    
    def habHelp(self):
        widg = self.habTableWidget
        currRow = widg.currentRow()
        pr = PrefRow()
        pr.code = widg.item(currRow,0).text()
        pr.name = widg.item(currRow,1).text()
        pr.color = widg.item(currRow,2).text()
        print pr

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