#!/usr/bin/env python
"""
This is part of BenthicPhotoSurvey. https://bitbucket.org/jkibele/benthic_photo_survey

@author: jkibele
"""
import sys
from PyQt4.QtGui import QApplication
from bps_package.bps_gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()