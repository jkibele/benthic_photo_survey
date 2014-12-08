all : bps_package/ui_bps.py bps_package/ui_preferences.py bps_package/ui_pref_help.py
.PHONY : all

bps_package/ui_bps.py : qt_gui.ui
	pyuic4 -o bps_package/ui_bps.py qt_gui.ui

bps_package/ui_preferences.py : preferences.ui
	pyuic4 -o bps_package/ui_preferences.py preferences.ui
	
bps_package/ui_pref_help.py : pref_help.ui
	pyuic4 -o bps_package/ui_pref_help.py pref_help.ui
