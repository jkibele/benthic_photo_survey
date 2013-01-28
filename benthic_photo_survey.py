import sys
#from photo_tagging import *
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog
from ui_bps import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)                                         
        self.setupUi(self)
        self.actionLoad_Image_Directory.triggered.connect(self.loadPhotoDirectory)

    def loadPhotoDirectory(self):
        photo_dir = QFileDialog.getExistingDirectory(self, 'Open Photo Directory', directory='~')
        print photo_dir
        self.statusBar().showMessage('File menu: New selected', 8000)
                
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
    