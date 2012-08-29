import pyexiv2 as exiv
from depth_temp_log_io import *
from configuration import *
from gps_log_io import *
from common import *
import os

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

def add_position_to_photo(img,reject_threshold=30):
    """Open up the image's exif data, find out when it was taken, then look in our
    position database, find a position fix with a coresponding time stamp, put that
    position into the proper format and write it to the image's exif data."""
    md = get_photo_metadata(img)
    ptime = get_photo_datetime(md)
    if not ptime:
        print "If there's no timestamp on the image we can't continue"
        return False
    # photo time is assumed to be local time but gps log is utc
    utctime = utc_from_local(ptime)
    
    pdict = get_position_for_time(utctime,reject_threshold=reject_threshold)
    
    if not pdict:
        print "Couldn't find a position close enough to the time handed in"
        return False
        
    exgps = 'Exif.GPSInfo.GPS'
    add_dict = {    'Latitude': pdict['lat']['fract'],
                    'LatitudeRef': pdict['lat']['hemi'],
                    'Longitude': pdict['lon']['fract'],
                    'LongitudeRef': pdict['lon']['hemi'] }
    for k,v in add_dict.iteritems():
        key = exgps + k
        print "%s: %s" % (str(key),str(v))
        md[key] = exiv.ExifTag(key,v)
    md.write()
    # This isn't working to assign values because these keys don't exist
    #md[exgps + 'Latitude'].value = pdict['lat']['fract']
    #md[exgps + 'LatitudeRef'].value = pdict['lat']['hemi']    
    #md[exgps + 'Longitude'].value = pdict['lon']['fract']
    #md[exgps + 'LongitudeRef'].value = pdict['lon']['hemi']
    
    #md.write()
    return True

    
    
    
    
    
    
    
    
