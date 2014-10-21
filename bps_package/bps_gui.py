#!/usr/bin/env python

import sys, os, operator, random
from slugify import slugify
try:
    from bps_package.depth_temp_log_io import *
    from bps_package.photo_tagging import *
    from bps_package.gps_log_io import *
    from bps_package.bps_export import *
except ImportError:
    from depth_temp_log_io import *
    from photo_tagging import *
    from gps_log_io import *
    from bps_export import *

from PyQt4 import QtCore
from PyQt4.QtCore import QSettings
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox, QDialog, QColor, QColorDialog, QTableWidgetItem, QDoubleSpinBox, \
    QInputDialog
from preference_array import HabPrefArray, PrefRow
from ui_bps import Ui_MainWindow
from ui_preferences import Ui_PrefDialog
import pytz

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class StartPrefs(QDialog, Ui_PrefDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.settings = QSettings(CONF_QSETTINGS_DEVELOPER,CONF_QSETTINGS_APPLICATION)
        self.habPrefArray = HabPrefArray(widget=self.habTableWidget)
        self.habPrefArray.loadFromSettings()
        # setup habitat table
        self.habTableWidget.setRowCount(self.habPrefArray.rowCount)
        if self.habPrefArray.rowsValid:
            self.habPrefArray.addToTableWidget()
        self.habTableWidget.setHorizontalHeaderLabels(["Code","Habitat","Color"])
        # setup general tab
        self.db_path = str(self.__settings_extract("db_path",CONF_DB_PATH))
        self.databaseLineEdit.setText( self.db_path )
        self.working_dir = self.__settings_extract("working_dir",CONF_WORKING_DIR)
        self.workingDirLineEdit.setText( self.working_dir )
        self.inputEPSG = int( self.__settings_extract("inputEPSG",CONF_INPUT_EPSG) )
        self.inputEPSGLineEdit.setText( str(self.inputEPSG) )
        self.outputEPSG = int( self.__settings_extract("outputEPSG",CONF_OUTPUT_EPSG) )
        self.outputEPSGLineEdit.setText( str(self.outputEPSG) )
        # setup time zone tab
        self.timezone = self.__settings_extract("timezone",LOCAL_TIME_ZONE)
#        self.ktimezonewidget.setSelected( self.timezone, True )
        # setup substrate tab
        self.substList = self.__settings_extract("substList",CONF_SUBSTRATES,isList=True)
        self.timeZoneListWidget.addItems( pytz.common_timezones )
        tzitem = self.timeZoneListWidget.findItems( self.timezone, QtCore.Qt.MatchFixedString )[0]
        self.timeZoneListWidget.setCurrentItem( tzitem )
#        self.substkeditlistwidget.setItems( self.substList )
        
    def __settings_extract(self,settings_tag,default,isList=False):
        try:
            if isList:
                val = self.settings.value(settings_tag,default).toStringList()
            else:
                val = self.settings.value(settings_tag,default).toString()
        except AttributeError:
            val = self.settings.value(settings_tag,default)
        return val            
        
    def accept(self):
        newpa = HabPrefArray(widget=self.habTableWidget)
        newpa.loadFromWidget()
        if newpa.saveToSettings(): # ensure habitat settings don't bork
            # then save other settings
            self.generalSaveSettings()
            self.timezone = self.timeZoneListWidget.selectedItems()[0]
#            self.timezone = self.ktimezonewidget.selection()[0]
            self.settings.setValue( "timezone",self.timezone )
#            self.substList = self.substkeditlistwidget.items()
            self.settings.setValue( "substList",self.substList )
            super(StartPrefs, self).accept()
        else:
            pass
        
    def generalSaveSettings(self):
        self.db_path = str(self.databaseLineEdit.text())
        self.working_dir = self.workingDirLineEdit.text()
        self.inputEPSG = self.inputEPSGLineEdit.text()
        self.outputEPSG = self.outputEPSGLineEdit.text()
        set_list = ['db_path','working_dir','inputEPSG','outputEPSG']
        for s in set_list:
            self.settings.setValue( s, self.__getattribute__(s) )
        
    def generalHelp(self):
        pass
    
    def generalChooseDB(self):
        new_db_path = QFileDialog.getSaveFileName(self,"Choose or Create Database File",self.db_path,filter="SQLite db(*.db)",options=QFileDialog.DontConfirmOverwrite)
        if new_db_path:
            self.db_path = str( new_db_path )
            self.databaseLineEdit.setText( self.db_path )
        else:
            return False
    
    def generalChooseWorkingDir(self):
        new_wdir = QFileDialog.getExistingDirectory(self,"Choose a Working Directory",self.working_dir)
        if new_wdir:
            self.working_dir = new_wdir         
            self.workingDirLineEdit.setText( self.working_dir )
        else:
            return False
    
    def timezoneHelp(self):
        pass
    
    def substratesHelp(self):
        pass
    
    def addHabRow(self):
        self.habTableWidget.setRowCount( self.habTableWidget.rowCount() + 1 )
    
    def removeHabRow(self):
        currRow = self.habTableWidget.currentRow()
        self.habTableWidget.removeRow( currRow )
    
    def moveHabUp(self):
        row = self.habTableWidget.currentRow()
        column = self.habTableWidget.currentColumn();
        if row > 0:
            self.habTableWidget.insertRow(row-1)
            for i in range(self.habTableWidget.columnCount()):
               self.habTableWidget.setItem(row-1,i,self.habTableWidget.takeItem(row+1,i))
               self.habTableWidget.setCurrentCell(row-1,column)
            self.habTableWidget.removeRow(row+1)
            
    def moveHabDown(self):
        row = self.habTableWidget.currentRow()
        column = self.habTableWidget.currentColumn();
        if row < self.habTableWidget.rowCount()-1:
            self.habTableWidget.insertRow(row+2)
            for i in range(self.habTableWidget.columnCount()):
               self.habTableWidget.setItem(row+2,i,self.habTableWidget.takeItem(row,i))
               self.habTableWidget.setCurrentCell(row+2,column)
            self.habTableWidget.removeRow(row)
    
    def changeHabColor(self):
        currRow = self.habTableWidget.currentRow()
        color_item = QTableWidgetItem()
        new_qcolor = QColorDialog.getColor(parent=self)
        if new_qcolor.isValid():
            color_item.setBackgroundColor( new_qcolor )
            color_item.setText( new_qcolor.name() )
            self.habTableWidget.setItem(currRow,2,color_item)
    
    def habHelp(self):
        widg = self.habTableWidget
        currRow = widg.currentRow()
        pr = PrefRow()
        pr.code = widg.item(currRow,0).text()
        pr.name = widg.item(currRow,1).text()
        pr.color = widg.item(currRow,2).text()
        #print pr
        
    def habItemDoubleClicked(self,qwtItem):
        if qwtItem.column()==2:
            self.changeHabColor()
    

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = QSettings(CONF_QSETTINGS_DEVELOPER,CONF_QSETTINGS_APPLICATION)                                    
        self.setupUi(self)
        self.imageDirectoryObj = None
        # imf will be the current image file object        
        self.imf = None 
        self.currentPhotoIndex = 0
        self.applySettings()
        self.db_path = str( self.__settings_extract("db_path",CONF_DB_PATH) )
        
    def __settings_extract(self,settings_tag,default,isList=False):
        try:
            if isList:
                val = self.settings.value(settings_tag,default).toStringList()
            else:
                val = self.settings.value(settings_tag,default).toString()
        except AttributeError:
            val = self.settings.value(settings_tag,default)
        return val    
        
    def resizeEvent( self, event ):
        super(MainWindow, self).resizeEvent( event )
        self.setPhotoDisplay()
        
    def setupHabSelector(self):
        habList = self.getHablistSettings()
#        self.habLED.off()
        htw = self.habitatTableWidget
        for sb in htw.findChildren(QDoubleSpinBox):
            # it turns out that this is crucial
            # segmentations faults if you don't do this
            sb.setParent(None)
        htw.clear()
        htw.setRowCount( len(habList) )
        htw.setColumnCount( 1 )
        htw.setVerticalHeaderLabels(habList)
        for i,hab in enumerate(habList):
            newsb = self.spinBoxFromHabName(hab)
            htw.setCellWidget(i,0,newsb)
            QtCore.QObject.connect(newsb, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), self.checkHabValues)
        if self.imf:
            self.loadExifData()
            
    def loadHabSelector(self,hab_dict):
        for hab,num in hab_dict.items():
            sb = self.spinBoxFromHabName(hab)
            sb.setValue(num)
        self.checkHabValues()
            
    def zeroHabSelector(self):
        habList = self.getHablistSettings()
        for hab in habList:
            sb = self.spinBoxFromHabName(hab)
            sb.setValue(0.0)
            
    def checkHabValues(self):
        tot = self.totalFromHabSelector
        if tot<1.0:
#            self.habLED.off()
#            self.habLED.setColor( QColor('green') )
            self.habSaveButton.setDisabled(True)
        elif tot==1.0:
#            self.habLED.on()
#            self.habLED.setColor( QColor('green') )
            self.habSaveButton.setDisabled(False)
        else:
#            self.habLED.off()
#            self.habLED.setColor( QColor('red') )
            self.habSaveButton.setDisabled(True)
        
    @property
    def totalFromHabSelector(self):
        habList = self.getHablistSettings()
        tot = 0.0
        for hab in habList:
            sb = self.spinBoxFromHabName(hab)
            tot += sb.value()
        return round(tot,4)
            
    def spinBoxFromHabName(self,habname):
        """
        If the spin box exists, return it. If not make it and return it.
        """
        #print "looking for habname: %s" % habname
        sbname = slugify( unicode(habname) ) + u"SpinBox"
        htw = self.habitatTableWidget
        try:
            sb = htw.findChild(QDoubleSpinBox,sbname)
            assert( sb!=None )
            return sb
        except AssertionError:
            #print "making SB: %s" % sbname
            newsb = QDoubleSpinBox(self.habitatTableWidget)
            newsb.setMaximum(1.0)
            newsb.setSingleStep(0.1)
            newsb.setObjectName(_fromUtf8(sbname))
            return newsb
            
    def setHabitat(self):
        htw = self.habitatTableWidget
        hab_dict = {}
        for row in range(htw.rowCount()):
            hab = str( htw.verticalHeaderItem(row).text() )
            sb = self.spinBoxFromHabName(hab)
            hab_dict[hab] = round( sb.value(), 4 )
        self.imf.set_xmp_fuzzy_habitats( hab_dict )
        # find the most common habitat and set that as the hard classification
        # first see if how many are tied for 1st place
        hdv = sorted(hab_dict.values())
        hdv.reverse()
        ties = hdv.count(hdv[0])
        # turn the dict into a sorted list of tuples        
        habs_sorted = sorted(hab_dict.iteritems(), key=operator.itemgetter(1))
        habs_sorted.reverse() # in place, so now sorted high to low
        if ties==1: # no ties, only one maxiumum. easy.
            # store the first 'key' value as the hard hab classification
            self.imf.set_xmp_habitat( habs_sorted[0][0] )
        else:
            # if I just used the first one here, I'd always get the lower
            # alphabetic label in the case of a tie. This way, I will get
            # a random choice in the event of a tie.
            tiedlist = habs_sorted[0:ties]
            hab_name = random.choice(tiedlist)[0]
            self.imf.set_xmp_habitat( hab_name )
        self.loadExifData()
                
    def applySettings(self):
        self.setupHabSelector()
        self.substrateListWidget.clear()
        self.substrateListWidget.addItems( self.getSubstSettings() )
        self.working_dir = self.__settings_extract("working_dir",CONF_WORKING_DIR)
        self.db_path = str( self.__settings_extract("db_path",CONF_DB_PATH) )
        
    def getHablistSettings(self):
        hpa = HabPrefArray()
        hpa.loadFromSettings()
        return hpa.toHabList()
        
    def getSubstSettings(self):
        try:
            return self.settings.value("substlist",CONF_SUBSTRATES).toStringList()
        except AttributeError:
            return self.settings.value("substlist",CONF_SUBSTRATES)
        
    def setPhotoDisplay(self):
        """
        If there's a currently set imageDirectoryObj, set the current image file
        (self.imf) to match the currentPhotoIndex, size it properly and set it to
        display.
        """
        if self.imageDirectoryObj:
            self.imf = self.imageDirectoryObj.images[ self.currentPhotoIndex ]
            photo_pixmap = QPixmap( self.imf.file_path )
            self.scaled_photo = photo_pixmap.scaled(self.photoDisplay.size(), QtCore.Qt.KeepAspectRatio)
            self.photoDisplay.setPixmap( self.scaled_photo )
            
    def setPhotoData(self):
        self.loadExifData()
        self.loadPhotoDirectoryData()
        
    def loadPhotoDirectoryData(self):
        self.filenameValue.setText(self.imf.file_name)
        direc = '...' + self.imageDirectoryObj.path[-30:]
        self.directoryValue.setText(direc)
        num_str = "%i of %i" % (self.currentPhotoIndex + 1, self.imageDirectoryObj.image_count )
        self.photoCountValue.setText(num_str)
            
    def loadExifData(self):
        if self.imf.datetime:
            pdate = self.imf.datetime.strftime('%d/%m/%Y')
            ptime = self.imf.datetime.strftime('%H:%M:%S')
        else:
            pdate = 'None'
            ptime = 'None'
        self.timeValue.setText( ptime )
        self.dateValue.setText( pdate )
        if self.imf.position:
            latstr, lonstr = unicode(self.imf.position).split(',')
        else:
            latstr, lonstr = 'None','None'
        self.latitudeValue.setText( latstr )
        self.longitudeValue.setText( lonstr )
        self.directionValue.setText( str(self.imf.exif_direction) )
        if self.imf.exif_depth:
            dstr = "%.2f m" % self.imf.exif_depth
        else:
            dstr = 'None'
        self.depthValue.setText( dstr )
        if self.imf.xmp_temperature:
            tstr = str(self.imf.xmp_temperature) + ' ' + self.imf.xmp_temp_units
        else:
            tstr = 'None'
        self.temperatureValue.setText( tstr )
        hab = self.imf.xmp_habitat
        self.habitatValue.setText( str(hab) )
        fuzzy_hab_dict = self.imf.xmp_fuzzy_hab_dict
        if fuzzy_hab_dict: # Set the values in the habitat selector
            self.loadHabSelector( fuzzy_hab_dict )
        else:
            self.zeroHabSelector()
            
        subs = self.imf.xmp_substrate
        self.substrateValue.setText( str(subs) )
        if subs:
            subst_list_item = self.substrateListWidget.findItems( str(subs), QtCore.Qt.MatchFlags() )[0]
            self.substrateListWidget.setCurrentItem( subst_list_item )
        else:
            self.substrateListWidget.setCurrentItem( None )

    def loadPhotoDirectory(self):
        default_dir = os.path.join( str(self.working_dir), "images" )
        if not os.path.exists( default_dir ):
            os.mkdir( default_dir )
        photo_dir = str( QFileDialog.getExistingDirectory(self, 'Open Photo Directory', directory=default_dir) )
        if photo_dir:
            self.imageDirectoryObj = image_directory( photo_dir )
            self.currentPhotoIndex = 0
            self.setPhotoDisplay()
            self.setPhotoData()
            msg = "Photo Directory Set to: %s" % photo_dir
            self.statusBar().showMessage( msg, 8000)
            #print self.imageDirectoryObj.fuzzy_habitat_dict
            self.checkPhotoSettingCompatibility() # this is a bit useless right
            # now. May beef this up later.
        else: # User hit cancel
            return False
            
    def photoDirSettingsCompatibility(self):
        """
        Take a look at the photos in this directory and see if they are 
        compatable with the current habitat settings.
        """
        photo_habs = self.imageDirectoryObj.fuzzy_habitat_dict
        habList = self.getHablistSettings()
        not_in_photos = {}
        not_in_settings = {}
        for hab in habList:
            if hab not in photo_habs.keys():
                try:
                    not_in_photos[hab] += 1
                except KeyError:
                    not_in_photos[hab] = 1
        for hab in photo_habs:
            if hab not in habList:
                try:
                    not_in_settings[hab] += 1
                except KeyError:
                    not_in_settings[hab] = 1
        return not_in_photos, not_in_settings
        
    def checkPhotoSettingCompatibility(self):
        """
        See if the current photo directory's photo metadata is compatible with
        the current habitat settings.
        """
        not_in_photos,not_in_settings = self.photoDirSettingsCompatibility()
        if not_in_photos or not_in_settings:
            if not_in_photos:
                print "%i habitats in your preferences are not represented in any photos." % len(not_in_photos)
            if not_in_settings:
                print "%i habitats in your photos are not represented in your preferences." % len(not_in_settings)
                print "Photo habitats are ",
                for hab in not_in_settings:
                    print "%s " % hab,
                print "\n"
            return False
        else:
            return True
            
    def actionTimeShiftPhotos(self):
        """
        This method will be triggered when a user chooses the "Time Shift Photos"
        option from the action menu.
        """
        dialogtxt = "Warning: Only use this if you know what you're doing."
        hours, ok = QInputDialog.getDouble(self,'Offset in Hours', dialogtxt,decimals=4)
        if ok:
            try:
                tdelta = td(hours=float(hours))
                conf_msg = "Are you sure you want to shift the timestamp on your \
                            photos by %f hours?" % float(hours)
                reply = QMessageBox.warning(None,"Confirm",conf_msg,QMessageBox.Yes,QMessageBox.No)
                if reply==QMessageBox.Yes:
                    self.timeShiftPhotos(tdelta)
                    result_str = "Great Success: photos time shifted."
                    self.statusBar().showMessage( result_str, 8000)
                    return True
                else:
                    return False
            except ValueError:
                msg = QMessageBox()
                msg.setText("You must enter a float or integer value. Try again.")
                msg.setText("You lose")
                msg._exec()
                return False
                
    def timeShiftPhotos(self,tdelta):
        """
        Shift all the photos in the current photo directory by the time delta
        tdelta.
        """
        self.imageDirectoryObj.__shift_datetimes__(tdelta)
        
    def removeIncompatibleHabTags(self):
        """
        Inspect the habitat tags in each photo. If they are incompatible with
        the habitats in settings, the tags will be removed.
        """
        habList = self.getHablistSettings()
        for imf in self.imageDirectoryObj.images:
            if imf.xmp_habitat not in habList:
                imf.remove_habitattagging()
        
    def nextPhoto(self):
        if self.currentPhotoIndex < self.imageDirectoryObj.image_count - 1:
            self.currentPhotoIndex += 1
        else:
            self.currentPhotoIndex = 0
        self.setPhotoDisplay()
        self.setPhotoData()
        
    def previousPhoto(self):
        if self.currentPhotoIndex == 0:
            self.currentPhotoIndex = self.imageDirectoryObj.image_count - 1
        else:
            self.currentPhotoIndex -= 1
        self.setPhotoDisplay()
        self.setPhotoData()
        
    def setSubstrate(self, item_index):
        item = self.substrateListWidget.itemFromIndex( item_index )
        hab = str( item.text() )
        self.imf.set_xmp_substrate( hab )
        self.loadExifData()
    
    def geoTag(self):
        if self.imf:
            r = self.imf.geotag(self.db_path)
            if not r:
                msg = QMessageBox( )
                msg.setText('I could not tag this image with depth and temp. Either I could not find a record with a close enough time code or perhaps something more horrible happened.')
                msg.setWindowTitle("Epic Failure")
                msg.exec_()
                return False
            else:
                self.loadExifData()
                return True
        else:
            msg = QMessageBox()
            msg.setText("Please load a photo directory using the file menu.")
            msg.setWindowTitle("What photo?")
            msg.exec_()
            return False
            
    def geoTagAll(self):
        rg_cnt = 0
        if self.imageDirectoryObj and self.imageDirectoryObj.image_count > 0:
            for imf in self.imageDirectoryObj.images:
                if imf.geotag(self.db_path):
                    rg_cnt += 1
            if rg_cnt==self.imageDirectoryObj.image_count:
                title_str = 'Great Success!'
            else:
                title_str = 'Moderate Success'
            info_str = "Out of %i total photos, I geotagged %i. You\'re welcome." % (self.imageDirectoryObj.image_count,rg_cnt)
            
            self.loadExifData()
        else:
            info_str = 'I couldn\'t tag any images. It looks like there aren\'t any images loaded. Try loading a directory of photos with the File menu. Good luck.'
            title_str = 'Epic Failure'
        mbox = QMessageBox()
        mbox.setText( info_str )
        mbox.setWindowTitle( title_str )
        mbox.exec_()
    
    def depthTempTag(self):
        if self.imf:
            r = self.imf.depth_temp_tag(self.db_path)
            if not r:
                msg = QMessageBox( )
                msg.setText('I could not tag this image with depth and temp. Either I could not find a record with a close enough time code or perhaps something more horrible happened.')
                msg.setWindowTitle("Epic Failure")
                msg.exec_()
                return False
            else:
                self.loadExifData()
                return True
        else:
            msg = QMessageBox()
            msg.setText("Please load a photo directory using the file menu.")
            msg.setWindowTitle("What photo?")
            msg.exec_()
            return False
            
    def depthTempTagAll(self):
        rg_cnt = 0
        if self.imageDirectoryObj.image_count > 0:
            for imf in self.imageDirectoryObj.images:
                if imf.depth_temp_tag(self.db_path):
                    rg_cnt += 1
            if rg_cnt==self.imageDirectoryObj.image_count:
                title_str = 'Great Success!'
            else:
                title_str = 'Moderate Success'
            info_str = "Out of %i total photos, I tagged %i with depth and temperature. You\'re welcome." % (self.imageDirectoryObj.image_count,rg_cnt)
            
            self.loadExifData()
        else:
            info_str = 'I couldn\'t tag any images. It looks like there aren\'t any images loaded. Try loading a directory of photos with the File menu. Good luck.'
            title_str = 'Epic Failure'
        mbox = QMessageBox()
        mbox.setText( info_str )
        mbox.setWindowTitle( title_str )
        mbox.exec_()
    
    def depthPlot(self):
        self.imageDirectoryObj.depth_plot(self.db_path)
    
    def exportShapefile(self):
        default_dir = os.path.join( str(self.working_dir), "shapefiles" )
        if not os.path.exists( default_dir ):
            os.mkdir( default_dir )
        shp_filepath = str( QFileDialog.getSaveFileName(self, 'Save Shapefile',
                                                        directory=default_dir,
                                                        filter='Shapefiles (*.shp)') )
        if shp_filepath:
            #try:
            inputEPSG = int( self.__settings_extract("inputEPSG",CONF_INPUT_EPSG) )
            outputEPSG = int( self.__settings_extract("outputEPSG",CONF_OUTPUT_EPSG) )
            bpse = bps_shp_exporter(shp_filepath,qsettings=self.settings,epsg_in=inputEPSG,epsg_out=outputEPSG)
            returned_path = bpse.write_shapefile( self.imageDirectoryObj )
            result_str = "Great Success: Shapefile written to: %s" % returned_path
            self.statusBar().showMessage( result_str, 8000)
            return True
#            except:
#                import traceback
#                exc_type, exc_value, exc_traceback = sys.exc_info()
#                mbox = QMessageBox()
#                mbox.setText("Oops. Seems like that didn't work.")
#                mbox.setDetailedText('\n'.join(traceback.format_tb(exc_traceback)))
#                mbox.setWindowTitle("Epic Failure")
#                mbox.exec_()
#                return False
        else: # User hit cancel
            return False
                
    
    def loadGpsLog(self):
        default_dir = os.path.join( str(self.working_dir), "gps" )
        if not os.path.exists( default_dir ):
            os.mkdir( default_dir )
        log_filepath = str( QFileDialog.getOpenFileName(self, 'Load GPS log', directory=default_dir, filter='GPS Files (*.gpx *.log)') )
        if log_filepath:            
            try:            
                if log_filepath.lower().endswith('.gpx'):
                    gf = gpx_file( log_filepath )
                    result_str = gf.read_to_db(self.db_path)
                else:
                    result_str = read_gps_log( log_filepath )
                msg = "Great Success: %s" % result_str
                self.statusBar().showMessage( msg, 8000)
                return True
            except:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                mbox = QMessageBox()
                mbox.setText("Something bad happened. Are you sure that was a GPS log file?")
                mbox.setDetailedText('\n'.join(traceback.format_tb(exc_traceback)))
                mbox.setWindowTitle("Epic Failure")
                mbox.exec_()
                return False
        else: # This means the user hit 'cancel'
            return False
            
        
    def loadDepthLog(self):
        default_dir = os.path.join( str(self.working_dir), "sensus" )
        if not os.path.exists( default_dir ):
            os.mkdir( default_dir )
        log_filepath = str( QFileDialog.getOpenFileName(self, 'Load Depth / Temp log', directory=default_dir, filter='Sensus Log Files (*.csv)') )
        if log_filepath:
            try:        
                result_str = read_depth_temp_log( log_filepath,self.db_path )
                msg = "Great Success: %s" % result_str
                self.statusBar().showMessage( msg, 8000)
                return True
            except:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                mbox = QMessageBox()
                mbox.setText("Your CSV file was probably not formatted as expected. Are you sure it was a sensus log file?")
                mbox.setDetailedText('\n'.join(traceback.format_tb(exc_traceback)))
                mbox.setWindowTitle("Epic Failure")
                mbox.exec_()
                return False
        else: # This means the user hit 'cancel' 
            return False
            
    def preferenceDialog(self):
        #write this dialog launching code
        dlg = StartPrefs(parent=self)
        if dlg.exec_():
            self.applySettings()

                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    