import sqlite3, argparse, os, pytz
from datetime import timedelta as td
from datetime import datetime as dt
from dateutil import parser as dt_parser
from configuration import *
import matplotlib as mpl
from PyQt4.QtCore import QSettings

import matplotlib.pyplot as plt
import numpy as np


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def connection_and_cursor(path_to_db):
    """Connect to the db and pass back the connection and cursor. Create db
    and directories if needed."""
    if not os.path.exists(path_to_db):
        p, db_name = os.path.split(path_to_db)
        if p:
            plist = p.split(os.path.sep)
            for i in range(len(plist)):
                dirpath = os.path.sep.join(plist[:i+1])
                if dirpath and not os.path.exists( dirpath ):
                    os.mkdir(dirpath)
        
    conn = sqlite3.connect(path_to_db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    return conn,cur

def make_aware_of_local_tz(unaware):
    """Make an unaware time object aware of the local time zone. This tries to 
    get the timezone from settings."""
    settings = QSettings(CONF_QSETTINGS_DEVELOPER,CONF_QSETTINGS_APPLICATION)
    try:
        local_zone_str = str( settings.value('timezone',LOCAL_TIME_ZONE).toString() )
    except AttributeError:
        local_zone_str = str( settings.value('timezone',LOCAL_TIME_ZONE) )
    # LOCAL_TIME_ZONE is from configuration.py
    local_zone = pytz.timezone(local_zone_str)
    return local_zone.localize(unaware)

def utc_from_local(localtime):
    """Given a local datetime, return the UTC datetime equivalent. If the time
    given is not aware, assume it is suppose to be local and make it aware."""
    if not localtime.tzinfo: # make sure it really is aware
        localtime = make_aware_of_local_tz(localtime)
    return localtime.astimezone(pytz.UTC)
    
def local_from_utc(utc_datetime):
    """Given a utc datetime, return the local equivalent."""
    if not utc_datetime.tzinfo: # make sure it is aware
        utc_datetime = pytz.utc.localize(utc_datetime)
    return utc_datetime.astimezone( pytz.timezone(LOCAL_TIME_ZONE) ) # LOCAL_TIME_ZONE from configuration.py
