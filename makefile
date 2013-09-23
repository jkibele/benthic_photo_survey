all : bps_package/ui_bps.py bps_package/ui_preferences.py
.PHONY : all

bps_package/ui_bps.py : qt_gui.ui
	pyuic4 -o bps_package/ui_bps.py qt_gui.ui

bps_package/ui_preferences.py : preferences.ui
	pyuic4 -o bps_package/ui_preferences.py preferences.ui
