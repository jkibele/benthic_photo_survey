all : ui_mainwindow.py ui_testpref.py
.PHONY : all

ui_mainwindow.py : mainwindow.ui
	pyuic4 -o ui_mainwindow.py mainwindow.ui

ui_testpref.py : testpref.ui
	pyuic4 -o ui_testpref.py testpref.ui
