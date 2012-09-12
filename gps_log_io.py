from pynmea.streamer import NMEAStream
from dateutil import parser as dt_parser
from fractions import Fraction
from itertools import groupby
from math import modf
from common import *
try:
    import ogr
except ImportError:
    from osgeo import ogr
    
def fraction_to_rational(fra):
    """
    Take a fraction and return a stupid Rational to make stupid damned 
    pyexiv2 happy. If it's not a fraction, just hand it back and hope
    for the best.
    """
    from pyexiv2.utils import Rational
    if fra.__class__.__name__=='Fraction':
        return Rational(fra.limit_denominator().numerator,fra.limit_denominator().denominator)
    else:
        return fra    

class coord(object):
    """
    Store a latitude or a longitude and provide some methods for converting to
    various formats. Coord will be reclassed by latitude and longitude classes
    that will provide methods specific to those types of coordinates.
    """
    def __init__(self,degrees,minutes):
        # Apparently all my type checking is bad form for python. Maybe 
        # I will take it out at some point but probably not
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
        
    def __unicode__(self):
        return u'%i\u00B0 %g\'' % (self.degrees,self.minutes)
        
    def __str__(self):
        return unicode(self).encode('utf-8')
        
    @property
    def dms(self):
        """
        Return coordinates in a tuple of degrees,minutes,seconds.
        """
        seconds = 60 * modf( self.minutes )[0]
        return (self.degrees,int(self.minutes),seconds)
        
    @property
    def decimal_degrees(self):
        """
        Return the coordinate in decimal degrees.
        """
        from math import copysign as cps
        return self.degrees + cps(self.minutes,self.degrees) / 60.0
        
    @property
    def nmea_string(self):
        """
        Return coordinates in a nmea style string.
        """
        return str(abs(self.degrees)) + str(self.minutes)
    
    @property
    def exif_coord(self):
        """
        Return the coordinate in the format that can be used to assign to an
        exif tag using the pyexiv2 library.
        """
        from pyexiv2.utils import Rational
        (d,m,s) = self.dms
        return ( Rational(abs(d),1),Rational(m,1),Rational(s * 1e7,1e7) )
        
    def __adjust_sign(self,hemi):
        """
        If given 'N' or 'E' for the hemisphere, set the sign of the degrees to positive.
        If given 'S' or 'W' for the hemisphere, set the sign of the degrees to negative.
        If hemi is None, do nothing.
        """
        pos = ['N','E']
        neg = ['S','W']
        if hemi:
            if hemi.upper() in neg:
                self.degrees = -abs(self.degrees)
            elif hemi.upper() in pos:
                self.degrees = abs(self.degrees)
            else:
                raise ValueError( "Hemisphere should be N, S, E, or W. Why are you giving me %s?" % (hemi,) )
        
    @staticmethod
    def from_dms( d,m,s,hemi=None ):
        """
        Take degrees minutes and seconds and return a coord object in degrees
        and float minutes.
        """
        minutes = float(m) + s / 60.0
        c = coord( d, minutes )
        c.__adjust_sign(hemi)
        return c
        
    @staticmethod
    def from_dd( dec_deg, hemi=None ):
        """
        Take decimal degrees and return a coord object with integer degrees and
        float minutes.
        """
        m,d = modf(dec_deg)
        m = abs(m) * 60
        c = coord(d,m)
        c.__adjust_sign(hemi)
        return c
        
    @staticmethod
    def from_exif_coord( (fracdeg,fracmin,fracsec), hemi=None ):
        """
        Take a tuple of Fractions (that's how they're given from pyexiv2)
        and translate into a coord.
        """
        fracdeg = fraction_to_rational(fracdeg)
        fracmin = fraction_to_rational(fracmin)
        fracsec = fraction_to_rational(fracsec)
        d = int( fracdeg.to_float() )
        c = coord.from_dms( d, fracmin.to_float(), fracsec.to_float() )
        c.__adjust_sign(hemi)
        return c
        
    @staticmethod
    def from_nmea_string(nstr,hemi=None):
        """
        Take a coordinate in the format given in NMEA log files and return a
        coord object. Hemi is optional. If supplied, we will determine the 
        sign of the degrees value based on the value of hemi regardless of
        original sign handed in.
        """
        l = str(nstr).split('.')
        deg = int( l[0][:-2] )
        minute = float( l[0][-2:] + '.' + l[1] )
        c = coord(deg,minute)
        c.__adjust_sign(hemi)
        return c
        
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
    def from_dms( d,m,s,hemi=None ):
        """
        Take degrees minutes and seconds and return a coord object in degrees
        and float minutes.
        """
        c = coord.from_dms( d,m,s,hemi )
        return latitude(c.degrees,c.minutes)
        
    @staticmethod
    def from_dd( dec_deg, hemi=None ):
        """
        Take decimal degrees and return a coord object with integer degrees and
        float minutes.
        """
        c = coord.from_dd( dec_deg, hemi )
        return latitude(c.degrees,c.minutes)
        
    @staticmethod
    def from_exif_coord( (fracdeg,fracmin,fracsec), hemi=None ):
        """
        Take a tuple of Fractions (that's how they're given from pyexiv2)
        and translate into a coord.
        """
        c = coord.from_exif_coord( (fracdeg,fracmin,fracsec), hemi )
        return latitude(c.degrees,c.minutes)
    
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
        
    @staticmethod
    def from_dms( d,m,s,hemi=None ):
        """
        Take degrees minutes and seconds and return a coord object in degrees
        and float minutes.
        """
        c = coord.from_dms( d,m,s,hemi )
        return longitude(c.degrees,c.minutes)
        
    @staticmethod
    def from_dd( dec_deg, hemi=None ):
        """
        Take decimal degrees and return a coord object with integer degrees and
        float minutes.
        """
        c = coord.from_dd( dec_deg, hemi )
        return longitude(c.degrees,c.minutes)
        
    @staticmethod
    def from_exif_coord( (fracdeg,fracmin,fracsec), hemi=None ):
        """
        Take a tuple of Fractions (that's how they're given from pyexiv2)
        and translate into a coord.
        """
        c = coord.from_exif_coord( (fracdeg,fracmin,fracsec), hemi )
        return longitude(c.degrees,c.minutes)
    
    @staticmethod
    def from_nmea_string(nstr,hemi=None):
        c = coord.from_nmea_string(nstr,hemi)
        return longitude(c.degrees,c.minutes)
        
    @property
    def hemisphere(self):
        if self.degrees < 0:
            return 'W'
        else:
            return 'E'
            
class position(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
        
    def __repr__(self):
        return "%s, %s" % (repr(self.lat),repr(self.lon))
        
    def __unicode__(self):
        return u'%s, %s' % (self.lat,self.lon)
        
    def __str__(self):
        return "%s, %s" % (self.lat,self.lon)
        
    @property
    def ogr_point(self):
        """
        Return the coordinate as an ogr point geometry.
        """
        geom = ogr.Geometry(ogr.wkbPoint)
        geom.SetPoint(0, self.lon.decimal_degrees, self.lat.decimal_degrees)
        return geom

class gpx_file(object):
    def __init__(self,file_path):
        self.file_path = file_path

    def __repr__(self):
        return "GPX file: %s" % (self.file_path,)
        
    @property
    def ogr_ds(self):
        gpx_driver = ogr.GetDriverByName('GPX')
        return gpx_driver.Open(self.file_path)
        
    @property
    def layer_names(self):
        ds = self.ogr_ds
        return [ds.GetLayerByIndex(x).GetName() for x in range(ds.GetLayerCount())]
    
    @property    
    def track_points(self):
        ds = self.ogr_ds
        try:
            lyr = ds.GetLayerByName('track_points')
        except AttributeError:
            return None
            
        result = []
        for feat in lyr:
            lon = longitude.from_dd( feat.geometry().GetX() )
            lat = latitude.from_dd( feat.geometry().GetY() )
            pos = position(lat,lon)
            try:
                result.append([dt_parser.parse( feat.time ),pos])
            except AttributeError:
                pass # If we get here it's because there is a track point with no timestamp so we don't want it
        return result
        
    def read_to_db(self, dbp=db_path):
        if not self.track_points:
            print "The file %s has no track points." % (self.file_path,)
            return None
        conn,cur = connection_and_cursor(dbp)
        # Make sure the table is there
        create_gpslog_table(cur)
        rec_count = 0
        for tp in self.track_points:
            utctime = tp[0]
            pos = tp[1]
            latitude = pos.lat.nmea_string
            lat_hemi = pos.lat.hemisphere
            longitude = pos.lon.nmea_string
            lon_hemi = pos.lon.hemisphere
            t = ( None, utctime.replace(tzinfo=None), latitude, lat_hemi, longitude, lon_hemi, None )
            cur.execute("INSERT INTO GPSLog VALUES (?,?,?,?,?,?,?)", t)
            rec_count += 1
        conn.commit()
        cur.close()
        return "Read %i records from %s to %s." % (rec_count,os.path.basename(self.file_path),os.path.basename(dbp))

def create_gpslog_table(cur):
    cur.execute("create table if not exists GPSLog ( validity text, utctime datetime, latitude real, lat_hemi text,\
                longitude real, lon_hemi text, num_sats integer, UNIQUE (utctime) ON CONFLICT REPLACE)")

def get_position_for_time(dt_obj,reject_threshold=30,return_pretty=False,verbose=False):
    """Given a datetime object, find the position for the nearest position
    fix. I may want to interpolate between positions at some point but I'll
    leave that for later."""
    if not dt_obj:
        return None
    conn,cur = connection_and_cursor(db_path)
    t = ( dt_obj,dt_obj )
    result = cur.execute("select abs(strftime('%s',?) - strftime('%s',utctime) ), \
                        latitude, lat_hemi, longitude, lon_hemi, rowid from GPSLog order by \
                        abs( strftime('%s',?) - strftime('%s',utctime) ) LIMIT 1", t).fetchone()
    time_diff = result[0]
    lat = latitude.from_nmea_string( result[1], result[2] )
    lon = longitude.from_nmea_string( result[3], result[4] )
    if verbose:
        print "Position from rowid: %i ---> %s, %s.  Time difference = %i" % (result[5], str(lat), str(lon), time_diff)
    if time_diff > reject_threshold:
        return None
    else:
        if return_pretty:
            return unicode( lat ) + u', ' + unicode( lon )
        else:
            return position(lat,lon)

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

def read_gps_log(filepath,path_to_db=db_path):
    """Read in a single nmea gps log into the sqlite database. Currently requiring
    the GPRMC sentence and optionally reading the number of satellites from the
    GPGGA sentence when it is available.
    """
    conn,cur = connection_and_cursor(path_to_db)
    # Make sure the table is there
    create_gpslog_table(cur)
    
    data = extract_gps_data(filepath,these_sentences=('GPRMC','GPGGA',))
    
    grouped = group_nmea_sentences_by_timestamp(data)
    rec_count = 0
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
            rec_count += 1
    
    conn.commit()
    cur.close()
    return "Read %i records from %s to %s." % (rec_count,os.path.basename(filepath),os.path.basename(path_to_db))
    
def batch_read_gps_logs(directory):
    """Iteratively use read_gps_log on all files in a directory. Restrict to a 
    range of dates?"""
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Import a GPS log file into the database. The GPS log can either be an NMEA text log file with a \'.log\' extension or a GPX file with a \'.gpx\' extension.")
    parser.add_argument('input_path', type=str, help='The directory of log files or the individual file that you want to import.')
    parser.add_argument('output_db', nargs='?', type=str, help='The database you would like to read the log into. If left blank, the %s will be used as specified in configuration.py.' % (db_path,), default=db_path)
    args = parser.parse_args()

    if os.path.isdir(args.input_path): # this means a directory has been handed in
        for fname in os.listdir(args.input_path):
            if fname.lower().endswith('.log'):
                read_gps_log(os.path.join(args.input_path,fname),args.output_db)
            elif fname.lower().endswith('.gpx'):
                gpx_file(os.path.join(args.input_path,fname)).read_to_db(args.output_db)
    else:
        if args.input_path.lower().endswith('.log'):
            read_gps_log(args.input_path,args.output_db)
        elif args.input_path.lower().endswith('.gpx'):
            gf = gpx_file(args.input_path)
            gf.read_to_db(args.output_db)





