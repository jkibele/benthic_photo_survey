all : ui_bps ui_preferences ui_pref_help resources
.PHONY : all

ui_bps : qt_gui.ui
	pyuic4 -o bps_package/ui_bps.py qt_gui.ui

ui_preferences : preferences.ui
	pyuic4 -o bps_package/ui_preferences.py preferences.ui
	
ui_pref_help : pref_help.ui
	pyuic4 -o bps_package/ui_pref_help.py pref_help.ui

resources : qt_resources.qrc
	pyrcc4 -o bps_package/qt_resources_rc.py qt_resources.qrc
