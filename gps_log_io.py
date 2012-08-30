from pynmea.streamer import NMEAStream
from fractions import Fraction
from itertools import groupby
from common import *

class coord(object):
    def __init__(self,degrees,minutes):
        # Apparently all my type checking is bad form for python. Maybe 
        # I will take it out at some point
        if degrees == None:
            self.degrees = None
        elif int(degrees) <> degrees:
            raise ValueError( "The value of %s changes when cast to an integer so it can not be used for degrees" % str(degrees) )
        elif abs(degrees) > 180:
            raise ValueError( "Degrees can not exceed 180." )
        else:
            self.degrees = int(degrees)
        
        if minutes == None:
            self.minutes = None
        elif not 0 <= float(minutes) < 60:
            raise ValueError( "Minutes must be between 0 and 60." )
        else:
            self.minutes = float(minutes)
            
    def __setattr__(self,name,value):
        if name=='degrees':
            if int(value) <> value:
                raise ValueError( "The value of %s changes when cast to an integer so it can not be used for degrees" % str(degrees) )
            elif abs(value) > 180:
                raise ValueError( "Degrees can not exceed 180." )
            else:
                super(coord,self).__setattr__(name,value)
        elif name=='minutes':
            if not 0 <= float(value) < 60:
                raise ValueError( "Minutes must be between 0 and 60." )
            else:
                super(coord,self).__setattr__(name,value)
                
    def __repr__(self):
        return "%i %g" % (self.degrees,self.minutes)
        
    @staticmethod
    def from_nmea_string(nstr,hemi=None):
        pos = ['N','E']
        neg = ['S','W']
        l = str(nstr).split('.')
        deg = int( l[0][:-2] )
        minute = float( l[0][-2:] + '.' + l[1] )
        if hemi:
            if hemi.upper() in neg:
                deg = -abs(deg)
            elif hemi.upper() in pos:
                deg = abs(deg)
            else:
                raise ValueError( "Hemisphere should be N, S, E, or W. Why are you giving me %s?" % (hemi,) )
        return coord(deg,minute)
        
    def __unicode__(self):
        return u'%i\u00B0 %g\'' % (self.degrees,self.minutes)
        
    def __str__(self):
        return unicode(self).encode('utf-8')
        
class latitude(coord):
    def __init__(self,degrees,minutes):
        if degrees <> None and abs(degrees) > 90:
            raise ValueError( "Latitude degrees can not exceed 90" )
        coord.__init__(self,degrees,minutes)
        
    def __setattr__(self,name,value):
        if name=='degrees' and abs(value) > 90:
            raise ValueError( "Degrees of latitude can not exceed 90." )
        else:
            super(coord,self).__setattr__(name,value)
            
    @staticmethod
    def from_nmea_string(nstr,hemi=None):
        c = coord.from_nmea_string(nstr,hemi)
        return latitude(c.degrees,c.minutes)
        
    @property
    def hemisphere(self):
        if self.degrees < 0:
            return 'S'
        else:
            return 'N'
        
class longitude(coord):
    def __init__(self,degrees,minutes):
        coord.__init__(self,degrees,minutes)
        
    @property
    def hemisphere(self):
        if self.degrees < 0:
            return 'W'
        else:
            return 'E'
    
def coord_to_dict(coord, hemi):
    """Take a coordinate in the format given in NMEA log files and put it into
    a dictionary.
    
    >>>coord_to_dict(12345.67891234,'E')
    {'deg': 123, 'hemi': 'E', 'min': 45.6789123}
    """
    c_dict = {  'deg': coord_deg(coord),
                'min': coord_min(coord),
                'fract': coord_fractions(coord), 
                'hemi': hemi }
    return c_dict
    
def coord_deg(coord):
    """Pull the degrees from NMEA style coordinate"""
    l = str(coord).split('.')
    return int( l[0][:-2] )
    
def coord_min(coord):
    """Pull the decimal minutes from NMEA style coordinate"""
    l = str(coord).split('.')
    return float( l[0][-2:] + '.' + l[1] )
    
def coord_fractions(coord):
    deg = Fraction.from_decimal( coord_deg(coord) )
    minutes = Fraction.from_float( coord_min(coord) )
    sec = Fraction.from_decimal( 0 )
    return (deg,minutes,sec)

def parse_coordinates_to_dict(lat,lat_hemi,lon,lon_hemi):
    lat_dict = coord_to_dict(lat,lat_hemi)
    lon_dict = coord_to_dict(lon,lon_hemi)
    return { 'lat': lat_dict, 'lon': lon_dict }

def get_position_for_time(dt_obj,reject_threshold=30,return_pretty=False):
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
    result_str = "%s %s, %s %s" % ( parse_coordinate_pretty(lat), lat_hemi.upper(), parse_coordinate_pretty(lon), lon_hemi.upper() )
    result_dict = parse_coordinates_to_dict( lat,lat_hemi,lon,lon_hemi )
    if time_diff > reject_threshold:
        return False
    else:
        if return_pretty:
            return result_str
        else:
            return result_dict

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
