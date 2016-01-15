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

import json
from types import StringType, UnicodeType
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QColor, QTableWidgetItem, QMessageBox
from configuration import CONF_QSETTINGS_DEVELOPER, CONF_QSETTINGS_APPLICATION

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
        if type(self.name)==StringType or type(self.name)==UnicodeType:
            return True
        else:
            return False

    @property
    def validCode(self):
        if type(self.code)==int and self.code > 0:
            return True
        else:
            return False

    @property
    def validColor(self):
        if type(self.color)==StringType or type(self.color)==UnicodeType:
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
        #print itemlist
        for i,thing in enumerate(itemlist):
            item = QTableWidgetItem( str(thing) )
            if i==len(itemlist)-1:
                item.setBackgroundColor( self.q_color )
            #print "Adding %s to row %i" % (item.text(),rownum)
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
    def hab_color_dict(self):
        d = {}
        for pr in self.rows:
            d[pr.name] = str(pr.color)
        return d

    @property
    def hab_number_dict(self):
        d = {}
        for pr in self.rows:
            d[pr.name] = int(pr.code)
        return d

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
        if self.rowsValid:
            json_str = json.dumps( self.toList() )
            self.settings.setValue( self.settings_tag, json_str )
            return True
        else:
            #print "row not valid"
            for row in self.rows:
                if not row.isValid:
                    if not row.validCode:
                        msg = QMessageBox()
                        msg.setText("Habitat codes must be non-zero integers (whole numbers).")
                        msg.setWindowTitle("Invalid Habitat Code")
                        msg.exec_()
                    if not row.validName:
                        msg = QMessageBox()
                        msg.setText("You entered an invalide habitat name. I'm not sure how you even did that.")
                        msg.setWindowTitle("Invalid Habitat Name")
                        msg.exec_()
                    if not row.validColor:
                        msg = QMessageBox()
                        msg.setText("You apparently entered an invalid color. Try selecting the row and clicking the 'Choose Color' button.")
                        msg.setWindowTitle("Invalid Habitat Color")
                        msg.exec_()
            return False

    def loadFromSettings(self):
        try:
            json_str = str( self.settings.value(self.settings_tag,'[["kelp", 1, "#009900"]]').toString() )
        except AttributeError:
            json_str = str( self.settings.value(self.settings_tag,'[["kelp", 1, "#009900"]]') )
        self.fromJson(json_str)
        return self

    def loadFromWidget(self):
        """
        Load values from the QTableWidget. This will overwrite the rows.
        """
        self.rows = []
        row_cnt = self.widget.rowCount()
        #print "row_cnt in loadFromWidget=%i" % row_cnt
        for r in range(row_cnt):
            newpr = PrefRow()
            try:
                newpr.code = int( self.widget.item(r,0).text() )
            except ValueError:
                try:
                    newpr.code = float( self.widget.item(r,0).text() )
                except:
                    newpr.code = None
            newpr.name = unicode( self.widget.item(r,1).text() )
            newpr.color = unicode( self.widget.item(r,2).text() )
            self.rows.append(newpr)

    def fromJson(self,json_str):
        """
        Take a json string and load it into a list of rows. Then load that into
        PrefRows and load those into a PrefArray.
        """
        # turn the json into a list of lists (rows)
        #print "json str: %s" % json_str
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
        qset = QSettings(CONF_QSETTINGS_DEVELOPER,CONF_QSETTINGS_APPLICATION)
        stag = "habitats"
        super(HabPrefArray, self).__init__(rowList=rowList,settings=qset,settings_tag=stag,widget=widget)

    def toHabList(self):
        outlist = []
        for r in self.rows:
            outlist.append(r.name)
        return outlist
