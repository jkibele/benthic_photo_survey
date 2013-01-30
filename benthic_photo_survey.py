import sys, os
import glob
#from photo_tagging import *
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog
from ui_bps import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)                                         
        self.setupUi(self)
        self.picPaths = []
        self.currentPhotoIndex = 0
        self.actionLoad_Photo_Directory.triggered.connect(self.loadPhotoDirectory)

    def loadPhotoDirectory(self):
        photo_dir = str( QFileDialog.getExistingDirectory(self, 'Open Photo Directory', directory='data/images') )
        self.picPaths = glob.glob(photo_dir + os.path.sep + "*.JPG") + glob.glob(photo_dir + os.path.sep + "*.jpg")
        self.picPaths.sort()
        
        self.statusBar().showMessage('Photo Directory Set to: %s', 8000) % photo_dir
        
    def nextPhoto(self):
        
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    