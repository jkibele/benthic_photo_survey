from scipy import interpolate
from common import *
import csv

class dive_record_set(object):
    """
    Provide an interface to retrieve a set of depth / temp records and do
    stuff with them. If the given start and end datetime objects are naive,
    we'll assume they're in the local time zone as defined in configuration.py
    """
    def __init__(self, start_dt, end_dt, path_to_db):
        if start_dt.tzinfo == None:
            start_dt = make_aware_of_local_tz(start_dt)
        if end_dt.tzinfo == None:
            end_dt = make_aware_of_local_tz(end_dt)        
        self.start = start_dt
        self.end = end_dt
        self.db_path = path_to_db
        
    @property
    def db_rows(self):
        """
        utctime field in db does not store time zone but should always be in
        UTC so we'll make the start and end naive so we don't screw up the 
        comparison.
        """
        stdt = self.start.astimezone(pytz.utc).replace(tzinfo=None)
        endt = self.end.astimezone(pytz.utc).replace(tzinfo=None)
        t = ( self.start.astimezone(pytz.utc), self.end.astimezone(pytz.utc), )
        conn,cur = connection_and_cursor(self.db_path)
        rows = cur.execute( "SELECT utctime, celsius, depthm FROM DepthTempLog WHERE utctime >= ? AND utctime <= ?", t ).fetchall()
        cur.close()
        return rows
        
    @property
    def depth_time_list(self):
        """
        datetimes come out of the db in UTC. Convert to local tz before returning.
        """
        return [ ( float(r[2]), local_from_utc( dt_parser.parse(r[0]) ) ) for r in self.db_rows]
        
    @property
    def depth_time_array(self):
        return np.array(self.depth_time_list)
        
    def plot_depth_time(self):
        y = -1 * self.depth_time_array[:,0] # depths * -1 to make negative values
        x = self.depth_time_array[:,1] # datetimes
        plt.plot_date(x,y,linestyle='-')
        plt.show()
        
    @property
    def temperature_time_list(self):
        """
        datetimes come out of the db in UTC. Convert to local tz before returning.
        """
        return [ ( float(r[1]), local_from_utc( dt_parser.parse(r[0]) ) ) for r in self.db_rows]
        
    @property
    def temperature_time_array(self):
        return np.array(self.temperature_time_list)
        
    @property
    def time_delta(self):
        return self.end - self.start
        

def depth_from_pressure(mbars):
    """Return a depth (in meters) from a pressure in millibars. Calculated using
    1 atm = 1013.25 millibar and assuming 1 atm for every 9.9908 meters of sea
    water. I'm also assuming that we're diving at sea level and that the ambient
    presure is 1atm. """
    return (mbars - 1013.25) / 101.41830484045322 

def read_depth_temp_log(filepath,path_to_db,verbose=False):
    """Read in a single depth / temp csv file  into a sqlite db for persistence 
    and easy searching. Records must have a unique combination of device identifier,
    file number, and datetime stamp. If a conflict is found, the old record will be
    overwritten by the new one. This should insure that duplicates will not be 
    created if a csv file is loaded in multiple times."""
    # Connect to the db
    conn,cur = connection_and_cursor(path_to_db)
    # Make sure the table is there
    cur.execute("create table if not exists DepthTempLog ( device text, file integer, utctime datetime, kelvin real, celsius real, mbar integer, depthm real, UNIQUE (device, file, utctime) ON CONFLICT REPLACE)")
    # Read the csv file
    if verbose:
        print "About to read %s" % os.path.basename(filepath)
    reader = csv.reader(open(filepath,'rb'),delimiter=',')
    rec_count = 0
    for row in reader:
        device = row[1]
        file_id = int(row[2])
        # put the date and time in a datetime object so it can be manipulated
        start_time = dt(int(row[3]),int(row[4]),int(row[5]),int(row[6]),int(row[7]),int(row[8]))
        # The time comes in as local time. I don't want conflicts with gps utc
        # time so I will store everything as utc time. This is annoying in sqlite
        # it would be better to use Postgresql but I want to keep this small 
        # and reduce the difficulty of installation.
        time_offset = td(seconds=float(row[9]))
        record_time = make_aware_of_local_tz( start_time + time_offset )
        # If I store this as timezone aware, then I have trouble parsing the 
        # times I pull out of the db. So I will store unaware by taking out tzinfo.
        utc_time = utc_from_local(record_time).replace(tzinfo=None)
        mbar = int(row[10])
        kelvin = float(row[11])
        celsius = kelvin - 273.15
        depthm = depth_from_pressure(mbar)
        t = (device,file_id,utc_time,kelvin,celsius,mbar,depthm)
        
        if verbose:
            print "--- Just read row %i, putting it in db now." % rec_count
        # stick it in the table
        cur.execute("insert into DepthTempLog values (?,?,?,?,?,?,?)", t)
        rec_count += 1
    conn.commit()
    cur.close()
    return "Read %i records from %s to %s." % (rec_count,os.path.basename(filepath),os.path.basename(path_to_db))

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
    
def seconds_since_arbitrary( dt_obj, arbitrary_ordinal=1 ):
    """
    Return seconds since an arbitrary date.
    """
    return float( ( dt_obj - dt.fromordinal( arbitrary_ordinal ) ).seconds )

def get_depth_for_time(dt_obj, db_path, verbose=False, reject_threshold=30):
    """For a given datetime object, return the depth from the raw_log db. Go through the 
    extra hassle of interpolating the depth if the time falls between two depth measurements.
    If a record is not found within the number of seconds specified by reject_threshold,
    just return False."""
    # Connect to the db
    conn,cur = connection_and_cursor(db_path)
    # For some reason TZ awareness screws up DST
    dt_obj = dt_obj.replace(tzinfo=None)
    # make a tuple with the time handed in so we can pass it to the query
    t = ( dt_obj, ) 
    rows = cur.execute("select utctime, depthm from DepthTempLog order by abs( strftime('%s',?) - strftime('%s',utctime) ) LIMIT 2", t).fetchall()
    t1 = dt.strptime(rows[0][0],'%Y-%m-%d %H:%M:%S')
    t1_secs = seconds_since_arbitrary( t1 )
    t2 = dt.strptime(rows[1][0],'%Y-%m-%d %H:%M:%S')
    t2_secs = seconds_since_arbitrary( t2 )
    d1m = rows[0][1]
    d2m = rows[1][1]
    # Clean up
    cur.close()
    conn.close()
    
    # It is possible that the two closest time stamps do not sandwich our given
    # time (dt_obj). They could both be before or after. By putting the times in
    # an array, we can easily get the min and max time so we can check.
    times = np.array( [t1_secs,t2_secs] )
    dt_obj_secs = seconds_since_arbitrary( dt_obj ) + dt_obj.microsecond * 1E-6
    
    # if the closest available time stamp is further away than our threshold
    # then we will return False
    if verbose:
        print "Min: %i Given: %.3f Max: %i" % (times.min(),dt_obj_secs,times.max())
    if ( abs(times.min() - dt_obj_secs) > reject_threshold ):
        if verbose:
            print "Target time: %s, %s seconds, Closest time: %s, %s seconds, 2nd Closest: %s,%s seconds" % ( dt_obj.strftime('%Y-%m-%d %H:%M:%S'),dt_obj.strftime('%s'),t1.strftime('%Y-%m-%d %H:%M:%S'),t1.strftime('%s'),t2.strftime('%Y-%m-%d %H:%M:%S'),t2.strftime('%s') )
        return None
    elif times.min() < dt_obj_secs < times.max(): # if dt_obj is between the two closest times, interpolate the depth
        return interpolate_depth( dt_obj_secs, t1_secs, t2_secs, d1m, d2m )
    else: # just return the closest depth if our given time is not between the two closest logged times
        return d1m
        
def get_temp_for_time(dt_obj, db_path, reject_threshold=30):
    """Get a temperature in Celsius for a given time if there is a record within the
    number of seconds specified by reject_threshold. If there's no record that close,
    return False. I'm not going to bother with interpolation here because I don't 
    expect temperature to change that quickly relative to the sampling interval."""
    conn,cur = connection_and_cursor(db_path)
    t = ( dt_obj,dt_obj )
    result = cur.execute("select abs(strftime('%s',?) - strftime('%s',utctime) ), celsius from DepthTempLog order by abs( strftime('%s',?) - strftime('%s',utctime) ) LIMIT 1", t).fetchone()
    time_diff = result[0]
    celsius = result[1]
    if time_diff > reject_threshold:
        return None
    else:
        return celsius

def adjust_all_times(time_delta):
    """
    This will shift all the times of all the records. You probably don't wan to do
    this but I did want to once. I actually did it directly in the db so I have 
    never tested this method but I figured I might want it some day.
    """
    conn,cur = connection_and_cursor(db_path)
    t = (time_delta.total_seconds(),)
    cur.execute("update DepthTempLog set utctime=datetime(utctime,'+?')", t)
    conn.commit()
    cur.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import a depth/temperature csv file into the database.')
    parser.add_argument('input_path', type=str, help='The directory of csv files or the individual file that you want to import.')
    parser.add_argument('output_db', nargs='?', type=str, help='The database you would like to read the log into. If left blank, the db specified in configuration.py will be used.', default=db_path)
    args = parser.parse_args()
    
    if os.path.isdir(args.input_path): # this means a directory has been handed in
        for fname in os.listdir(args.input_path):
            read_depth_temp_log(os.path.join(args.input_path,fname),args.output_db)
    else:
        read_depth_temp_log(args.input_path,args.output_db)
    

