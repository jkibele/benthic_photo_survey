from pynmea.streamer import NMEAStream
from itertools import groupby
from common import *

def parse_coordinate(coord):
    """Take a coordinate of the form 12345.6789 and return in a format
    like 123 degree-symbol 45.6789'."""
    l = str(coord).split('.')
    deg = l[0][:-2]
    whole_min = l[0][-2:]
    dec_min = l[1]
    ret_str = u'%s\u00B0 %s.%s\'' % (deg,whole_min,dec_min)
    return ret_str

def get_position_for_time(dt_obj,reject_threshold=30):
    """Given a datetime object, find the position for the nearest position
    fix. I may want to interpolated between positions at some point but I'll
    leave that for later."""
    conn,cur = connection_and_cursor(db_path)
    t = ( dt_obj,dt_obj )
    result = cur.execute("select abs(strftime('%s',?) - strftime('%s',utctime) ), \
                        latitude, lat_hemi, longitude, lon_hemi from GPSLog order by \
                        abs( strftime('%s',?) - strftime('%s',utctime) ) LIMIT 1", t).fetchone()
    time_diff = result[0]
    lat = result[1]
    lat_hemi = result[2]
    lon = result[3]
    lon_hemi = result[4]
    result_str = "%s %s, %s %s" % ( parse_coordinate(lat), lat_hemi.upper(), parse_coordinate(lon), lon_hemi.upper() )
    if time_diff > reject_threshold:
        return False
    else:
        return result_str

def extract_gps_data(filepath,these_sentences=('GPRMC','GPGGA',)):
    """Use the pynmea library to read data out of an nmea log file."""
    with open(filepath, 'r') as data_file:
        streamer = NMEAStream(data_file)
        next_data = streamer.get_objects()
        data = []
        while next_data:
            for nd in next_data:
                if nd.sen_type in these_sentences:
                    data.append(nd)
            next_data = streamer.get_objects()
    return data
    
def group_nmea_sentences_by_timestamp(obj_list):
    """Take a list of nmea sentence objects parsed by pynmea and group them
    together by timestamp value. A list of lists will be returned each sub
    list item will be an nmea sentence object."""
    groups = []
    uniquekeys = []
    for k, g in groupby(obj_list, lambda x: x.timestamp):
        groups.append(list(g))      # Store group iterator as a list
        uniquekeys.append(k)
    #for g in groups:
    #    print "timestamp: %s group contains: %s" % (str(g[0].timestamp), ', '.join([z.__class__.__name__ for z in g]))
    return groups

def read_gps_log(filepath):
    """Read in a single nmea gps log into the sqlite database. Currently requiring
    the GPRMC sentence and optionally reading the number of satellites from the
    GPGGA sentence when it is available.
    """
    conn,cur = connection_and_cursor(db_path)
    # Make sure the table is there
    cur.execute("create table if not exists GPSLog ( validity text, utctime datetime, latitude real, lat_hemi text,\
                longitude real, lon_hemi text, num_sats integer, UNIQUE (utctime) ON CONFLICT REPLACE)")
    
    data = extract_gps_data(filepath,these_sentences=('GPRMC','GPGGA',))
    
    grouped = group_nmea_sentences_by_timestamp(data)
    
    for timegroup in grouped:
        # GPGGA does not have a datestamp so I don't want to use lone GPGGA sentences
        # If I have both sentences, I'll get the number of satellites.
        if 'GPRMC' in [s.sen_type for s in timegroup]:
            num_sats = None # In case there's no GPGGA sentence in this timegroup
            for sentence in timegroup:
                if sentence.sen_type=='GPRMC':
                    validity = sentence.data_validity
                    datetime_str = str(sentence.datestamp) + ' ' + str(sentence.timestamp)
                    utctime = dt.strptime(datetime_str,'%d%m%y %H%M%S.%f')
                    latitude = float(sentence.lat)
                    lat_hemi = sentence.lat_dir
                    longitude = float(sentence.lon)
                    lon_hemi = sentence.lon_dir
                elif sentence.sen_type=='GPGGA':
                    num_sats = int(sentence.num_sats)
            
            t = ( validity, utctime, latitude, lat_hemi, longitude, lon_hemi, num_sats )
            cur.execute("INSERT INTO GPSLog VALUES (?,?,?,?,?,?,?)", t)
    
    conn.commit()
    cur.close()
    
def batch_read_gps_logs(directory):
    """Iteratively use read_gps_log on all files in a directory. Restrict to a 
    range of dates?"""
    pass
