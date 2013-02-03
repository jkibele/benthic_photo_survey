import sys, os
import glob
from depth_temp_log_io import *
from photo_tagging import *
from gps_log_io import *
from bps_export import *
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QPixmap, \
    QMessageBox
from ui_bps import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)                                         
        self.setupUi(self)
        self.imageDirectoryObj = None
        # imf will be the current image file object        
        self.imf = None 
        self.currentPhotoIndex = 0
        self.habitatListWidget.addItems( CONF_HABITATS )
        self.substrateListWidget.addItems( CONF_SUBSTRATES )
        self.actionLoad_Photo_Directory.triggered.connect(self.loadPhotoDirectory)
        
    def resizeEvent( self, event ):
        super(MainWindow, self).resizeEvent( event )
        self.setPhotoDisplay()        
        
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
        """"""
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
            
        subs = self.imf.xmp_substrate
        self.substrateValue.setText( str(subs) )
        if subs:
            subst_list_item = self.substrateListWidget.findItems( str(subs), QtCore.Qt.MatchFlags() )[0]
            self.substrateListWidget.setCurrentItem( subst_list_item )

    def loadPhotoDirectory(self):
        photo_dir = str( QFileDialog.getExistingDirectory(self, 'Open Photo Directory', directory='data/images') )
        self.imageDirectoryObj = image_directory( photo_dir )
        self.setPhotoDisplay()
        self.setPhotoData()
        msg = "Photo Directory Set to: %s" % photo_dir
        self.statusBar().showMessage( msg, 8000)
        
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
    
    
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    