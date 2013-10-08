import pyexiv2 as exiv # see note about pyexiv2 in notes.txt
import json
from ast import literal_eval
from depth_temp_log_io import *
from configuration import *
from gps_log_io import *
from common import *
# That namespace url doesn't really exist. The custom tags seem to work
# without it. Perhaps I should figure out if I really need it or not.
exiv.xmp.register_namespace('http://svarchiteuthis.com/benthicphoto/', 'BenthicPhoto')

class image_directory(object):
    def __init__(self, dir_path):
        if os.path.isdir(dir_path):
            jpgs = [ os.path.join(dir_path,f) for f in os.listdir(dir_path) if f.lower().endswith('.jpg') ]
        else:
            raise ValueError("%s is not a directory." % dir_path)
        self.path = dir_path
        self.images = [ image_file(img) for img in jpgs ]
        self.images.sort(key=lambda i: i.datetime) # sort the images by datetime of the image
        self.image_count = len( self.images )
        
    def __shift_datetimes__(self, time_delta_obj, verbose=True):
        """
        Shift the 'date original' values of all photos in the directory. See the
        warnings in the image_file.__set_datetime__ method doc string. You should
        be careful about using this method.
        """
        for img in self.images:
            new_dt = img.__shift_datetime__( time_delta_obj, verbose=verbose )
        
    @property
    def local_datetimes(self):
        return [ x.datetime for x in self.images ]
    
    @property
    def utc_datetimes(self):
        return [ x.utc_datetime for x in self.images ]
        
    @property
    def exif_depths(self):
        d_list = []
        for img in self.images:
            if img.exif_depth:
                d_list.append(img.exif_depth * -1)
            else:
                d_list.append(0.0)
        return np.array(d_list)
        
    def depth_plot(self):
        """
        Create a plot of the depth profile with photo times and depths marked.
        """
        drs = dive_record_set( min(self.local_datetimes), max(self.local_datetimes) )
        y = -1 * drs.depth_time_array[:,0] # depths * -1 to make negative values
        x = drs.depth_time_array[:,1] # datetimes
            
        fig = plt.figure() # imported from matplotlib
        ax = fig.add_subplot(111)
        ax.plot_date(x,y,marker='.',linestyle='-',tz=pytz.timezone(LOCAL_TIME_ZONE) ) # LOCAL_TIME_ZONE from configuration.py)
        ax.plot(self.local_datetimes,self.exif_depths,'r*',markersize=10,picker=5)
        plt.xlabel('Date and Time')
        plt.ylabel('Depth (meters)')
        fig.suptitle('Photos with Depth and Time')
        #print "Before def onpick"
        def onpick(event):
            global ann
            try:
                ann.remove()
            except NameError:
                pass
            ind = event.ind[0]
            fname = os.path.basename( self.images[ind].file_path )
            ann_text = "Photo: %s\ndepth: %g\ndate: %s" % ( fname, self.exif_depths[ind], self.local_datetimes[ind].strftime('%Y/%m/%d %H:%M:%S') )
            ann = ax.annotate(ann_text, xy=(self.local_datetimes[ind], self.exif_depths[ind]), xytext=(-20,-20), 
                                textcoords='offset points', ha='center', va='top',
                                bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.5', 
                                                color='red'))
            plt.draw()
            print "Photo: %s, index: %i, depth: %g, date: %s" % ( fname, ind, self.exif_depths[ind], self.local_datetimes[ind].strftime('%Y/%m/%d %H:%M:%S') )
        #print "Before mpl_connect"    
        fig.canvas.mpl_connect('pick_event', onpick)
        plt.show()
        #print "after plt show"
        
    def depth_temp_tag(self,verbose=False):
        """
        Depth tag all the photos in the directory.
        """
        for img in self.images:
            img.depth_temp_tag(verbose)

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
        
    def __get_exiv_tag(self,tag_string):
        """
        Try to get a pyexiv2 tag. If the tag doesn't exist, return None.
        """
        try:
            return self.md[tag_string]
        except KeyError:
            return None
    
    def __get_exiv_tag_value(self,tag_string):
        """
        Try to get a pyexiv2 tag value. If the tag doesn't exist, return None.
        """
        try:
            return self.md[tag_string].value
        except KeyError:
            return None
            
    def __get_exiv_tag_human_value(self,tag_string):
        """
        Try to get a pyexiv2 tag human value. If the tag doesn't exist, return None.
        """
        try:
            return self.md[tag_string].human_value
        except KeyError:
            return None
            
    def exif_dict(self, exclude_panasonic_keys=True):
        """
        Return a dict with all exif and xmp keys and values.
        """
        exif_dict = {}
        for key in self.md.xmp_keys:
            if self.__get_exiv_tag_value(key):
                exif_dict.update( { key : self.__get_exiv_tag_value(key) } )
        for key in self.md.exif_keys:
            if not ( exclude_panasonic_keys and 'Panasonic' in key.split('.') ):
                if self.__get_exiv_tag_human_value(key):
                    exif_dict.update( { key : self.__get_exiv_tag_human_value(key)[:100] } )
        return exif_dict
    
    @property
    def file_name(self):
        return os.path.basename(self.file_path)
    
    @property
    def datetime(self):
        """
        Try to get a datetime object for the image's creation from the 
        Exif.Photo.DateTimeOriginal value via pyexiv2.
        """
        if self.__get_exiv_tag_value('Exif.Photo.DateTimeOriginal').tzname():
            return self.__get_exiv_tag_value('Exif.Photo.DateTimeOriginal')
        else:
            return make_aware_of_local_tz( self.__get_exiv_tag_value('Exif.Photo.DateTimeOriginal') )
            
    @property
    def utc_datetime(self):
        if self.datetime:
            return utc_from_local(self.datetime)
        else:
            return None
    
    @property
    def exif_direction(self):
        if self.__get_exiv_tag_value('Exif.GPSInfo.GPSImgDirection'):
            return float( self.__get_exiv_tag_value('Exif.GPSInfo.GPSImgDirection') )
    
    @property
    def exif_lat_tag(self):
        return self.__get_exiv_tag('Exif.GPSInfo.GPSLatitude')
        
    @property
    def exif_latref_tag(self):
        return self.__get_exiv_tag('Exif.GPSInfo.GPSLatitudeRef')
        
    @property
    def exif_lon_tag(self):
        return self.__get_exiv_tag('Exif.GPSInfo.GPSLongitude')
        
    @property
    def exif_lonref_tag(self):
        return self.__get_exiv_tag('Exif.GPSInfo.GPSLongitudeRef')
            
    @property
    def exif_depth_tag(self):
        return self.__get_exiv_tag('Exif.GPSInfo.GPSAltitude')
        
    @property
    def exif_depth(self):
        try:
            ret_val = float( self.__get_exiv_tag_value('Exif.GPSInfo.GPSAltitude') )
        except TypeError:
            try:
                ret_val = self.__get_exiv_tag_value('Exif.GPSInfo.GPSAltitude').to_float()
            except AttributeError:
                ret_val = None
        return ret_val
            
    @property
    def __exif_depth_temp_dict(self):
        """
        This is a bit of a hack. I couldn't find a good place to store temperature
        data in the exif so I went with storing a python dictionary as a string
        in Exif.Photo.UserComment. I think I'm going to stop using this and store
        this stuff in custom xmp tags instead. UserComment is accessible to many
        photo management apps so it seems likely to get corrupted. I made it a 
        private method but maybe I should have just deleted it.
        """
        try:
            dstr = self.md['Exif.Photo.UserComment'].value
            return literal_eval(dstr)
        except KeyError:
            return None
            
    @property
    def __exif_temperature(self):
        """
        This just exposes the temperature value from the hack mentioned in the
        doc string for exif_depth_temp_dict. I'm going to stop writing to this
        tag so don't be surprised if this returns nothing. Actually, I think I
        may just make it a private method because I don't want to delete it.
        """
        if self.exif_depth_temp_dict:
            return self.exif_depth_temp_dict['temp']
        else:
            return None
            
    @property
    def xmp_temperature(self):
        return self.__get_exiv_tag_value('Xmp.BenthicPhoto.temperature')
            
    @property
    def xmp_temp_units(self):
        return self.__get_exiv_tag_value('Xmp.BenthicPhoto.temp_units')
        
    @property
    def xmp_substrate(self):
        return self.__get_exiv_tag_value('Xmp.BenthicPhoto.substrate')
        
    @property
    def xmp_habitat(self):
        return self.__get_exiv_tag_value('Xmp.BenthicPhoto.habitat')
        
    @property
    def xmp_fuzzy_hab_dict(self):
        hd_json = self.__get_exiv_tag_value('Xmp.BenthicPhoto.fuzzy_hab_dict')
        if hd_json:
            return json.loads(hd_json)
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
        but I did want to once. If you lose the origination time for your 
        image you can not sync it to your gps track or your depth log so 
        leave this alone unless you're sure you know what you're doing. 
        If you screw up your data don't come crying to me. I tried to warn
        you.
        """
        key = 'Exif.Photo.DateTimeOriginal'
        self.md[key] = exiv.ExifTag(key,dt_obj)
        self.md.write()
        return self.datetime
        
    def __shift_datetime__(self,time_delta_obj,verbose=True):
        """
        Shift the 'date original' in the exif by the given time delta. See the
        warnings in the doc string of __set_datetime__ method. You should be 
        careful with this.
        """
        current_dt = self.datetime
        self.__set_datetime__( current_dt + time_delta_obj )
        if verbose:
            print "datetime of %s changed from %s to %s." % ( self.file_name, current_dt.strftime('%X, %x'), self.datetime.strftime('%X, %x') )
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
        if depth < 0: # This can happen because there's a bit of slop in the conversion from pressure to depth
            if verbose:
                print "Given depth was a negative value."
            depth = 0
        if not depth:
            return None
        if not temp:
            temp = 0.0 # temperature isn't important at this point so if it's not there we'll just call it zero
        pre = 'Exif.GPSInfo.GPS'
        #dt_str = "{'depth':%g,'temp':%g}" % (depth,temp)
        dfrac = Fraction.from_float(depth).limit_denominator()
        add_dict = {pre+'Altitude': Rational(dfrac.numerator,dfrac.denominator),
                    pre+'AltitudeRef': bytes(1),
                    }
                    #'Exif.Photo.UserComment': dt_str }
        for k,v in add_dict.iteritems():
            if verbose:
                print "%s = %s" % (str(k),str(v))
            self.md[k] = exiv.ExifTag(k,v)
        self.md.write()
        return True
        
    def __set_xmp_depth_temp(self,depth,temp):
        if not depth:
            return None
        if not temp:
            temp = 0.0 # temperature isn't important at this point so if it's not there we'll just call it zero
        pre = 'Xmp.BenthicPhoto.'
        self.md[pre+'depth'] = str(depth)
        self.md[pre+'depth_units'] = 'meters'
        self.md[pre+'temperature'] = str(temp)
        self.md[pre+'temp_units'] = 'celsius'
        self.md.write()
        
    def set_xmp_substrate(self, subst_str):
        pre = 'Xmp.BenthicPhoto.'
        self.md[pre+'substrate'] = subst_str
        self.md.write()
        
    def set_xmp_habitat(self, subst_str):
        pre = 'Xmp.BenthicPhoto.'
        self.md[pre+'habitat'] = subst_str
        self.md.write()
        
    def set_xmp_fuzzy_habitats(self, habdict):
        habdict_json_str = json.dumps(habdict)
        pre = 'Xmp.BenthicPhoto.'
        self.md[pre+'fuzzy_hab_dict'] = habdict_json_str
        self.md.write()
        
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
        
    def depth_temp_tag(self,verbose=False):
        """
        Get the depth and temp readings out of the db that match the photo's origination
        time (considering that the photo's time stamp is in the local timezone and the
        logs are in UTC) and write those values to the image's exif data.
        """
        self.__set_exif_depth_temp(self.logger_depth,self.logger_temp,verbose=verbose)
        self.__set_xmp_depth_temp(self.logger_depth,self.logger_temp)
        if self.exif_depth_tag:
            return self.exif_depth_tag.value
        else:
            return None
        
    def geotag(self,verbose=True):
        """
        Get a position that matches the time of creation for the image out
        of the database and set the exif data accordingly. We assume that 
        the photo timestamp is local and the gps position is utc.
        """
        pos = get_position_for_time(self.utc_datetime,verbose=verbose)
        if verbose and pos:
            print "-------------------GeoTagg--------------------------------"
            print "%s is going to get set to %s as %s, %s" % ( os.path.basename( self.file_path ), unicode( pos ), str(pos.lat.exif_coord), str(pos.lon.exif_coord) )
            print "%s, %s in dms" % ( str(pos.lat.dms), str(pos.lon.dms) )
        if pos:
            self.__set_exif_position(pos,verbose)
        return self.position
        
    def __compare_position__(self):
        """
        This is just for testing. Check to see if the value stored in the db
        matches what we display after conversion. I want to make sure I'm not
        throwing away precision in coordinate conversions.
        """
        pos = get_position_for_time(self.utc_datetime,verbose=True)
        print "  db says: %s, %s \nexif says: %s, %s" % ( pos.lat.nmea_string, pos.lon.nmea_string, self.position.lat.nmea_string, self.position.lon.nmea_string )
        if pos.lat.nmea_string == self.position.lat.nmea_string:
            print "Latitudes match"
        if pos.lon.nmea_string == self.position.lon.nmea_string:
            print "Longitudes match"
        
    def remove_geotagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        geokeys = ['Latitude','LatitudeRef','Longitude','LongitudeRef']
        pre = 'Exif.GPSInfo.GPS'
        for key in [pre+gk for gk in geokeys]:
            if self.md.__contains__(key):
                self.md.__delitem__(key)
                self.md.write()
                
    def remove_depthtagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        geokeys = ['Altitude','AltitudeRef']
        pre = 'Exif.GPSInfo.GPS'
        for key in [pre+gk for gk in geokeys]:
            if self.md.__contains__(key):
                self.md.__delitem__(key)
                self.md.write()
                
    def remove_temptagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        geokeys = ['depth','depth_units','temperature','temp_units']
        pre = 'Xmp.BenthicPhoto.'
        for key in [pre+gk for gk in geokeys]:
            if self.md.__contains__(key):
                self.md.__delitem__(key)
                self.md.write()
                
    def remove_substratetagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        key = 'Xmp.BenthicPhoto.substrate'
        if self.md.__contains__(key):
            self.md.__delitem__(key)
            self.md.write()
                
    def remove_habitattagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        key = 'Xmp.BenthicPhoto.habitat'
        if self.md.__contains__(key):
            self.md.__delitem__(key)
            self.md.write()
                
    def remove_all_tagging(self):
        """
        You probably won't need to do this but I did a few times during testing.
        """
        self.remove_geotagging()
        self.remove_depthtagging()
        self.remove_temptagging()
        self.remove_substratetagging()
        self.remove_habitattagging()

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
#### Why don't I delete it? Good question.       #######

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
            
def shift_time_for_photos(direc,time_delta):
    for fname in os.listdir(direc):
        if fname.lower().endswith('.jpg'):
            imf = image_file( os.path.join( direc,fname ) )
            orig_time = imf.datetime
            imf.__set_datetime__( orig_time + time_delta )
            print "Changed %s from %s to %s." % ( fname, orig_time.strftime('%H:%M'), imf.datetime.strftime('%H:%M') )
            
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


    
    
    
    
    
    
    
