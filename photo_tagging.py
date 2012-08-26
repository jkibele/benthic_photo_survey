from datetime import timedelta as td
from datetime import datetime as dt
from scipy import interpolate
#import pyexiv2 as exiv
import numpy as np
import sqlite3
import csv

db_path = 'data/db/raw_log.db'
dt_testlog = 'test_data/sensus/sensus_test.csv'
gps_testlog = 'test_data/gps/GPS_20120722_194204.log'

def connection_and_cursor(path_to_db):
    """Connect to the db and pass back the connection and cursor"""
    conn = sqlite3.connect(path_to_db, detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    return conn,cur

def read_gps_log(filepath):
    """Read in a single gps log and keep it in memory so we can search through
    it and find time stamped positions. We will want this to be additive so
    we can read in multiple log files and be able to search through all the 
    timestamped positions.
    
    To be decided:
    - Read in NMEA and GPX or just one? Other formats?
    - In addition to timestamp and position, should we read anything else? Accuracy?
    
    For reading NMEA, I can use pynmea. My gps logger records: '$GPGSA','$GPRMC',
     '$GPVTG','$GPGGA','$ADVER','$GPGSV'. pynmea will handle all except for $ADVER.
    """
    pass
    
def batch_read_gps_logs(directory):
    """Iteratively use read_gps_log on all files in a directory. Restrict to a 
    range of dates?"""
    pass
    
def depth_from_pressure(mbars):
    """Return a depth (in meters) from a pressure in millibars. Calculated using
    1 atm = 1013.25 millibar and assuming 1 atm for every 9.9908 meters of sea
    water."""
    return (mbars - 1013.25)/102.02488795116682

def read_depth_temp_log(filepath):
    """Read in a single depth / temp csv file  into a sqlite db for persistence 
    and easy searching. Records must have a unique combination of device identifier,
    file number, and datetime stamp. If a conflict is found, the old record will be
    overwritten by the new one. This should insure that duplicates will not be 
    created if a csv file is loaded in multiple times."""
    # Connect to the db
    conn,cur = connection_and_cursor(db_path)
    # Make sure the table is there
    cur.execute("create table if not exists DepthTempLog ( device text, file integer, datetime datetime, kelvin real, celsius real, mbar integer, depthm real, UNIQUE (device, file, datetime) ON CONFLICT REPLACE)")
    # Read the csv file
    reader = csv.reader(open(filepath,'rb'),delimiter=',')
    
    for row in reader:
        device = row[1]
        file_id = int(row[2])
        # put the date and time in a datetime object so it can be manipulated
        start_time = dt(int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7]),int(row[8]))
        # I'm not sure if the start time from the logger will be in local time or UTC
        # I suspect it is in local time so I will want to convert to UTC so I can store
        # everything in UTC and avoid screwups related to DST and whatnot
        time_offset = td(seconds=float(row[9]))
        record_time = start_time + time_offset
        # time_string = record_time.strftime('%Y-%m-%d %H:%M:%S')
        mbar = int(row[10])
        kelvin = float(row[11])
        celsius = kelvin - 273.15
        depthm = depth_from_pressure(mbar)
        t = (device,file_id,record_time,kelvin,celsius,mbar,depthm)
        
        # stick it in the table
        cur.execute("insert into DepthTempLog values (?,?,?,?,?,?,?)", t)
    conn.commit()
    cur.close()

def interpolate_depth(t_secs,t1_secs,t2_secs,d1m,d2m):
    """Given depth d1m at time t1_secs and depth d2m at time t2_secs, interpolate
    to find the depth at time t_secs."""
    #print "t_secs=%f;t1_secs=%f;t2_secs=%f;d1m=%f;d2m=%f" % (t_secs,t1_secs,t2_secs,d1m,d2m)
    # the order of arguements matters
    d = { float(t1_secs):d1m, float(t2_secs):d2m}
    x = np.array([min(d.keys()),max(d.keys())])
    y = np.array([ d[min(d.keys())], d[max(d.keys())] ])
    f = interpolate.interp1d(x,y)
    return float( f( float(t_secs) ) )

def get_depth_for_time(dt_obj, verbose=False, reject_threshold=30):
    """For a given datetime object, return the depth from the raw_log db. Go through the 
    extra hassle of interpolating the depth if the time falls between two depth measurements.
    If a record is not found within the number of seconds specified by reject_threshold,
    just return False."""
    # Connect to the db
    conn,cur = connection_and_cursor(db_path)
    # make a tuple with the time handed in as seconds so we can pass it to the query
    t = ( dt_obj, ) 
    rows = cur.execute("select datetime, depthm from DepthTempLog order by abs( strftime('%s',?) - strftime('%s',datetime) ) LIMIT 2", t).fetchall()
    t1 = dt.strptime(rows[0][0],'%Y-%m-%d %H:%M:%S')
    t1_secs = float( t1.strftime('%s') )
    t2 = dt.strptime(rows[1][0],'%Y-%m-%d %H:%M:%S')
    t2_secs = float( t2.strftime('%s') )
    d1m = rows[0][1]
    d2m = rows[1][1]
    # Clean up
    cur.close()
    conn.close()
    
    # It is possible that the two closest time stamps do not sandwich our given
    # time (dt_obj). They could both be before or after. By putting the times in
    # an array, we can easily get the min and max time so we can check.
    times = np.array( [t1_secs,t2_secs] )
    dt_obj_secs = float( dt_obj.strftime('%s') ) + dt_obj.microsecond * 1E-6
    
    # if the closest available time stamp is further away than our threshold
    # then we will return False
    if verbose:
        print "Min: %i Given: %.3f Max: %i" % (times.min(),dt_obj_secs,times.max())
    if ( abs(times.min() - dt_obj_secs) > reject_threshold ):
        print "Target time: %s, %s seconds, Closest time: %s, %s seconds, 2nd Closest: %s,%s seconds" % ( dt_obj.strftime('%Y-%m-%d %H:%M:%S'),dt_obj.strftime('%s'),t1.strftime('%Y-%m-%d %H:%M:%S'),t1.strftime('%s'),t2.strftime('%Y-%m-%d %H:%M:%S'),t2.strftime('%s') )
        return False
    elif times.min() < dt_obj_secs < times.max(): # if dt_obj is between the two closest times, interpolate the depth
        return interpolate_depth( dt_obj_secs, t1_secs, t2_secs, d1m, d2m )
    else: # just return the closest depth if our given time is not between the two closest logged times
        return d1m
        
def get_temp_for_time(dt_obj, reject_threshold=30):
    """Get a temperature in Celsius for a given time if there is a record within the
    number of seconds specified by reject_threshold. If there's no record that close,
    return False. I'm not going to bother with interpolation here because I don't 
    expect temperature to change that quickly relative to the sampling interval."""
    conn,cur = connection_and_cursor(db_path)
    t = ( dt_obj,dt_obj )
    result = cur.execute("select abs(strftime('%s',?) - strftime('%s',datetime) ), celsius from DepthTempLog order by abs( strftime('%s',?) - strftime('%s',datetime) ) LIMIT 1", t).fetchone()
    time_diff = result[0]
    celsius = result[1]
    if time_diff > reject_threshold:
        return False
    else:
        return celsius
