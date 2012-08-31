import pyexiv2 as exiv # see not about pyexiv2 in notes.txt
from depth_temp_log_io import *
from configuration import *
from gps_log_io import *
from common import *
import os

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
    def position(self):
        """
        Look at the exif data and return a position object as defined in
        gps_log_io. Return None if there's no GPSInfo in the exif.
        """
        lat = latitude.from_exif_coord(self.exif_lat_tag.value,self.exif_latref_tag.value)
        lon = longitude.from_exif_coord(self.exif_lon_tag.value,self.exif_lonref_tag.value)
        return position(lat,lon)
            
    def set_exif_position(self,pos):
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
            print "%s = %s" % (str(k),str(v))
            self.md[k] = exiv.ExifTag(k,v)
        self.md.write()
        return True
            
    def geotag(self):
        """
        Get a position that matches the time of creation for the image out
        of the database and set the exif data accordingly. We assume that 
        the photo timestamp is local and the gps position is utc.
        """
        pos = get_position_for_time(self.utc_datetime)
        return self.set_exif_position(pos)

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


    
    
    
    
    
    
    
