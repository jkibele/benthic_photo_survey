#!/usr/bin/env python

import sys, os, json
import glob
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
from PyQt4.QtCore import QSettings, QModelIndex
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox, QDialog, QColor, QColorDialog
from ui_bps import Ui_MainWindow
from ui_preferences import Ui_PrefDialog

class StartPrefs(QDialog, Ui_PrefDialog):
    def __init__(self,parent=None):
        QDialog.__init__(self,parent)
        self.setupUi(self)
        self.settings = QSettings("jkibele","BenthicPhotoSurvey")
        #self.settings.clear()
        self.habkeditlistbox.setItems( self.getHablistSettings() )
        self.substkeditlistwidget.setItems( self.getSubstSettings() )
        self.updateColorList()
        
    def accept(self):
        self.settings.setValue("hablist", self.habkeditlistbox.items() )
        self.settings.setValue("substlist", self.substkeditlistwidget.items() )
        super(StartPrefs, self).accept()
        
    def updateColorList(self):
        self.habColorListWidget.clear()
        self.habColorListWidget.addItems( self.habkeditlistbox.items() )
        for itemNum in range(self.habColorListWidget.count()):
            habitem = self.habColorListWidget.item(itemNum)
            habitem.setBackgroundColor( QColor( self.getHabColorList()[itemNum] ) )
    
    def editItemColor(self,qlwItem):
        new_qcolor = QColorDialog.getColor(parent=self)
        qlwItem.setBackgroundColor( new_qcolor )
        cdict = self.getHabColorDict()
        cdict[qlwItem.text().toString()] = new_qcolor.name().toString()
        
    def getHablistSettings(self):
        return self.settings.value("hablist",CONF_HABITATS).toStringList() 
        
    def getSubstSettings(self):
        return self.settings.value("substlist",CONF_SUBSTRATES).toStringList()
        
    def getHabColorList(self):
        return self.settings.value("habcolorlist", CONF_HAB_COLORS ).toStringList()
        
    def getHabColorListFromWidget(self,widget=self.habColorListWidget):
        colors = []        
        for itemNum in range(self.habColorListWidget.count()):
            habitem = self.habColorListWidget.item(itemNum)
            colors.append( habitem.backgroundColor().toString() )
        return colors
        
    def setHabColorList(self):
        colorlist = self.habColorListWidget
        self.settings.value("habcolorlist", )

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.settings = QSettings("jkibele","BenthicPhotoSurvey")                                    
        self.setupUi(self)
        self.imageDirectoryObj = None
        # imf will be the current image file object        
        self.imf = None 
        self.currentPhotoIndex = 0
        self.applySettings()
        
    def resizeEvent( self, event ):
        super(MainWindow, self).resizeEvent( event )
        self.setPhotoDisplay()        
        
    def applySettings(self):
        self.habitatListWidget.clear()
        self.habitatListWidget.addItems( self.getHablistSettings() )
        self.substrateListWidget.clear()
        self.substrateListWidget.addItems( self.getSubstSettings() )
        
    def getHablistSettings(self):
        return self.settings.value("hablist",CONF_HABITATS).toStringList()
        
    def getSubstSettings(self):
        return self.settings.value("substlist",CONF_SUBSTRATES).toStringList()
        
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
        if hab: # Set the selection in the listbox
            hab_list_item = self.habitatListWidget.findItems( str(hab), QtCore.Qt.MatchFlags() )[0]
            self.habitatListWidget.setCurrentItem( hab_list_item )
        else:
            self.habitatListWidget.setCurrentItem( None )
            
        subs = self.imf.xmp_substrate
        self.substrateValue.setText( str(subs) )
        if subs:
            subst_list_item = self.substrateListWidget.findItems( str(subs), QtCore.Qt.MatchFlags() )[0]
            self.substrateListWidget.setCurrentItem( subst_list_item )
        else:
            self.substrateListWidget.setCurrentItem( None )

    def loadPhotoDirectory(self):
        photo_dir = str( QFileDialog.getExistingDirectory(self, 'Open Photo Directory', directory=CONF_PHOTO_DIR) )
        if photo_dir:
            self.imageDirectoryObj = image_directory( photo_dir )
            self.setPhotoDisplay()
            self.setPhotoData()
            msg = "Photo Directory Set to: %s" % photo_dir
            self.statusBar().showMessage( msg, 8000)
        else: # User hit cancel
            return False
        
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
    
    def setHabitat(self, item_index):
        item = self.habitatListWidget.itemFromIndex( item_index )
        hab = str( item.text() )
        self.imf.set_xmp_habitat( hab )
        self.loadExifData()
    
    def geoTag(self):
        if self.imf:
            r = self.imf.geotag()
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
                if imf.geotag():
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
            r = self.imf.depth_temp_tag()
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
                if imf.depth_temp_tag():
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
        self.imageDirectoryObj.depth_plot()
    
    def exportShapefile(self):
        shp_filepath = str( QFileDialog.getSaveFileName(self, 'Save Shapefile',
                                                        directory='data/shapefiles',
                                                        filter='Shapefiles (*.shp)') )
        if shp_filepath:
            try:
                bpse = bps_shp_exporter(shp_filepath)
                returned_path = bpse.write_shapefile( self.imageDirectoryObj.path )
                result_str = "Great Success: Shapefile written to: %s" % returned_path
                return True
            except:
                import traceback
                exc_type, exc_value, exc_traceback = sys.exc_info()
                mbox = QMessageBox()
                mbox.setText("Oops. Seems like that didn't work.")
                mbox.setDetailedText('\n'.join(traceback.format_tb(exc_traceback)))
                mbox.setWindowTitle("Epic Failure")
                mbox.exec_()
                return False
        else: # User hit cancel
            return False
                
    
    def loadGpsLog(self):
        log_filepath = str( QFileDialog.getOpenFileName(self, 'Load GPS log', directory=CONF_GPS_DIR, filter='GPS Files (*.gpx *.log)') )
        if log_filepath:            
            try:            
                if log_filepath.lower().endswith('.gpx'):
                    gf = gpx_file( log_filepath )
                    result_str = gf.read_to_db()
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
        log_filepath = str( QFileDialog.getOpenFileName(self, 'Load Depth / Temp log', directory=CONF_DEPTH_DIR, filter='Sensus Log Files (*.csv)') )
        if log_filepath:
            try:        
                result_str = read_depth_temp_log( log_filepath )
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
        dlg.exec_()
        if dlg.Accepted==1:
            self.applySettings()

                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    