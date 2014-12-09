all : gui button_help
gui : bps_package/ui_bps.py bps_package/ui_preferences.py  bps_package/ui_pref_help.py bps_package/qt_resources_rc.py
.PHONY : all gui

bps_package/ui_bps.py : qt_gui.ui
	pyuic4 -o bps_package/ui_bps.py qt_gui.ui

bps_package/ui_preferences.py : preferences.ui
	pyuic4 -o bps_package/ui_preferences.py preferences.ui
	
bps_package/ui_pref_help.py : pref_help.ui
	pyuic4 -o bps_package/ui_pref_help.py pref_help.ui

bps_package/qt_resources_rc.py : qt_resources.qrc
	pyrcc4 -o bps_package/qt_resources_rc.py qt_resources.qrc

#bhdir := bps_package/docs/helpButtons/

button_help : bps_package/docs/helpButtons/*.md
	cd bps_package/docs/helpButtons && (make)
