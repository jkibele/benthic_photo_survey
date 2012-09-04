import pyexiv2 as exiv # see not about pyexiv2 in notes.txt
from ast import literal_eval
from depth_temp_log_io import *
from configuration import *
from gps_log_io import *
from common import *

class image_file(object):
    """
    An object to make accessing image files and metadata easier.
    """
    def __init__(self,img_path):
        if os.path.exists(img_path):
            self.file_path = img_path
            md = exiv.ImageMetadata(img_path)
            md.read()
            self.md = md
        else:
            raise ValueError( "The file %s does not exist." % (img_path,) )
            
    def __repr__(self):
        return "Image file: %s" % (self.file_path,)
        
    @property
    def datetime(self):
        """
        Try to get a datetime object for the image's creation from the 
        Exif.Photo.DateTimeOriginal value via pyexiv2.
        """
        try:
            return self.md['Exif.Photo.DateTimeOriginal'].value
        except KeyError:
            return None
            
    @property
    def utc_datetime(self):
        if self.datetime:
            return utc_from_local(self.datetime)
        else:
            return None
    
    @property
    def exif_lat_tag(self):
        try:
            return self.md['Exif.GPSInfo.GPSLatitude']
        except KeyError:
            return None
        
    @property
    def exif_latref_tag(self):
        try:
            return self.md['Exif.GPSInfo.GPSLatitudeRef']
        except KeyError:
            return None
        
    @property
    def exif_lon_tag(self):
        try:
            return self.md['Exif.GPSInfo.GPSLongitude']
        except KeyError:
            return None
        
    @property
    def exif_lonref_tag(self):
        try:
            return self.md['Exif.GPSInfo.GPSLongitudeRef']
        except KeyError:
            return None
            
    @property
    def exif_depth_tag(self):
        try:
            return self.md['Exif.GPSInfo.GPSAltitude']
        except KeyError:
            return None
            
    @property
    def exif_depth_temp_dict(self):
        """
        This is a bit of a hack. I couldn't find a good place to store temperature
        data in the exif so I went with storing a python dictionary as a string
        in Exif.Photo.UserComment.
        """
        try:
            dstr = self.md['Exif.Photo.UserComment'].value
            return literal_eval(dstr)
        except KeyError:
            return None
            
    @property
    def exif_temperature(self):
        """
        This just exposes the temperature value from the hack mentioned in the
        doc string for exif_depth_temp_dict.
        """
        if self.exif_depth_temp_dict:
            return self.exif_depth_temp_dict['temp']
        else:
            return None
            
    @property
    def position(self):
        """
        Look at the exif data and return a position object (as defined in
        gps_log_io). Return None if there's no GPSInfo in the exif.
        """
        if self.exif_lat_tag and self.exif_lon_tag and self.exif_latref_tag and self.exif_lonref_tag:
            lat = latitude.from_exif_coord(self.exif_lat_tag.value,self.exif_latref_tag.value)
            lon = longitude.from_exif_coord(self.exif_lon_tag.value,self.exif_lonref_tag.value)
            return position(lat,lon)
        else:
            return None
            
    def __set_datetime__(self,dt_obj):
        """
        Set the date original in the exif. I don't think you want to do this
        but I did want to once.
        """
        key = 'Exif.Photo.DateTimeOriginal'
        self.md[key] = exiv.ExifTag(key,dt_obj)
        self.md.write()
        return self.datetime
            
    def __set_exif_position(self,pos,verbose=False):
        """
        Set the relevant exif tags to match the position object handed in.
        The position object is defined over in gps_log_io.py
        """
        pre = 'Exif.GPSInfo.GPS'
        add_dict = {pre+'Latitude': pos.lat.exif_coord,
                    pre+'LatitudeRef': pos.lat.hemisphere,
                    pre+'Longitude': pos.lon.exif_coord,
                    pre+'LongitudeRef': pos.lon.hemisphere }
        for k,v in add_dict.iteritems():
            if verbose:
                print "%s = %s" % (str(k),str(v))
            self.md[k] = exiv.ExifTag(k,v)
        self.md.write()
        return True
        
    def __set_exif_depth_temp(self,depth,temp,verbose=False):
        from pyexiv2.utils import Rational
        if not depth:
            return None
        if not temp:
            temp = 0.0 # temperature isn't important at this point so if it's not there we'll just call it zero
        pre = 'Exif.GPSInfo.GPS'
        dt_str = "{'depth':%g,'temp':%g}" % (depth,temp)
        dfrac = Fraction.from_float(depth).limit_denominator()
        add_dict = {pre+'Altitude': Rational(dfrac.numerator,dfrac.denominator),
                    pre+'AltitudeRef': bytes(1),
                    'Exif.Photo.UserComment': dt_str }
        for k,v in add_dict.iteritems():
            if verbose:
                print "%s = %s" % (str(k),str(v))
            self.md[k] = exiv.ExifTag(k,v)
        self.md.write()
        return True
        
    @property
    def logger_depth(self):
        """
        Get the logged depth out of the db that matches the photo's timestamp.
        """
        if self.utc_datetime:
            depth = get_depth_for_time(self.utc_datetime,reject_threshold=30)
            return depth
        else:
            return None
        
    @property
    def logger_temp(self):
        """
        Get the logged temperature out of the db that matches the photo's timestamp.
        """
        if self.utc_datetime:
            temp = get_temp_for_time(self.utc_datetime,reject_threshold=30)
            return temp
        else:
            return None
        
    def depth_temp_tag(self):
        self.__set_exif_depth_temp(self.logger_depth,self.logger_temp)
        if self.exif_depth_tag:
            return self.exif_depth_tag.value
        else:
            return None
        
    def geotag(self):
        """
        Get a position that matches the time of creation for the image out
        of the database and set the exif data accordingly. We assume that 
        the photo timestamp is local and the gps position is utc.
        """
        pos = get_position_for_time(self.utc_datetime)
        if pos:
            self.__set_exif_position(pos)
        return self.position
        
    def remove_geotagging(self):
        geokeys = ['Latitude','LatitudeRef','Longitude','LongitudeRef']
        pre = 'Exif.GPSInfo.GPS'
        for key in [pre+gk for gk in geokeys]:
            if self.md.__contains__(key):
                self.md.__delitem__(key)
                self.md.write()

def exif_tag_jpegs(photo_dir):
    for fname in os.listdir(photo_dir):
        if fname.lower().endswith('.jpg'):
            imf = image_file( os.path.join(photo_dir,fname) )
            imf.depth_temp_tag()
            imf.geotag()
            if imf.exif_depth_tag:
                dstr = imf.exif_depth_tag.human_value
            else:
                dstr = 'None'
            if imf.exif_temperature:
                tstr = "%g C" % imf.exif_temperature
            else:
                tstr = 'None'
            print "Image: %s - Depth: %s, Temp %s, Position: %s" % (fname,dstr,tstr,imf.position)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag a photos with position, depth, and temperature from a gps and a Sensus Ultra depth and temperature logger.')
    parser.add_argument('photo_dir', nargs='?', type=str, help='The directory that contains photos you would like tagged.')
    
    args = parser.parse_args()
    
    exif_tag_jpegs(args.photo_dir)
    





#### Pretty much just testing garbage below here #######

def check_time_tags(img):
    md = get_photo_metadata(img)
    timetags = [tag for tag in md.exif_keys if tag.find('Time')<>-1]
    for t in timetags:
        print "%s: %s" % (t,md[t])

def read_gps_crap(img):
    md = get_photo_metadata(img_path)
    try:
        gpstag = md['Exif.Image.GPSTag'].human_value
    except KeyError:
        gpstag = 'not set'
    try:
        lat = md['Exif.GPSInfo.GPSLatitude'].human_value
    except KeyError:
        lat = 'not set'
    try:
        lon = md['Exif.GPSInfo.GPSLongitude'].human_value
    except KeyError:
        lon = 'not set'
    
    print "GPSTag: %s, Lat: %s, Lon: %s" % ( str(gpstag), str(lat), str(lon) )

def read_gps_crap_from_dir(dir):
    for fname in os.listdir(dir):
        if fname.lower().endswith('.jpg'):
            read_gps_crap(os.path.join(dir,fname))
            
def photo_times_for_dir(dir):
    for fname in os.listdir(dir):
        if fname.lower().endswith('.jpg'):
            img = os.path.join(dir,fname)
            md = get_photo_metadata(img)
            ptime = get_photo_datetime(md)
            if ptime:
                ending = ptime.strftime('%Y-%m-%d %H:%M:%S')
            else:
                ending = 'no time tag'
            print "%s: %s" % (fname,ending)

def get_photo_metadata(img_path):
    md = exiv.ImageMetadata(img_path)
    md.read()
    return md
    
def get_photo_datetime(md):
    """If I find inconsistency in exif tags, I may have to get a little more creative
    here."""
    try:
        ptime = md['Exif.Photo.DateTimeOriginal'].value
    except KeyError:
        ptime = False
    return ptime


    
    
    
    
    
    
    
