from datetime import timedelta as td
from datetime import datetime as dt
from configuration import *
import numpy as np
import sqlite3
import pytz

def connection_and_cursor(path_to_db):
    """Connect to the db and pass back the connection and cursor"""
    conn = sqlite3.connect(path_to_db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    return conn,cur

def make_aware_of_local_tz(unaware):
    """Make an unaware time object aware of the local time zone. I'd like to 
    introspect the system and get the TZ but I can't figure out how to do that
    reliably so you'll have to se the LOCAL_TIME_ZONE parameter. Lame."""
    local_zone = pytz.timezone(LOCAL_TIME_ZONE)
    return local_zone.localize(unaware)

def utc_from_local(aware_local):
    """Given a local datetime, return the UTC datetime equivalent."""
    if not aware_local.tzinfo: # make sure it really is aware
        aware_local = make_aware_of_local_tz(aware_local)
    return aware_local.astimezone(pytz.UTC)
