from photo_tagging import *
import osr

## Crap. Need to refactor to work with settings instead of CONF_BLAH.
## should pass img_dir object in to exporter while I'm at it. Maybe hand in
## QSettings obj.

class bps_shp_exporter(object):
    def __init__(self, file_path, overwrite=True,lyr_name='bps_points',qsettings=None,epsg_in=CONF_INPUT_EPSG,epsg_out=CONF_OUTPUT_EPSG):
        """
        An object with the necessary attributes and methods to turn a directory
        of tagged images into a shapefile.
        
        Attributes:
            file_path: The path to write out the shapefile to. This must be a 
                valid file path that ends with .shp. String type.
            overwrite: A boolean indicating whether the file_path should be
                overwritten if it already exists.
            lyr_name: A string that will be used to name the feature layer in 
                the shapefile.
            qsettings: A PyQt4 QSettings object that will be inspected to get
                EPSG values for input and output. If supplied, the qsettings 
                EPSG values will be used and the those supplied directly will 
                be ignored.
            epsg_in: An int value representing the input EPSG value. This will 
                be ignored if specified in qsettings.
            epsg_out: An int value representing the output EPSG value. This will 
                be ignored if specified in qsettings.
        """
        self.overwrite = overwrite
        self.file_path = self.__validate_fp(file_path)
        #-----Set up the shapefile-------------------------
        self.spatialRefIn = osr.SpatialReference()
        if qsettings:
            epsg_in = int( qsettings.value("inputEPSG",CONF_INPUT_EPSG) )
            epsg_out = int( qsettings.value("inputEPSG",CONF_OUTPUT_EPSG) )
        print "epsg_in type: %s" % str(type(epsg_in))
        print "epsg_in = %s" % epsg_in
        self.spatialRefIn.ImportFromEPSG(epsg_in)
        # if epsg_out is None, we want to output in the epsg_in spatial reference
        if epsg_out:
            self.spatialRefOut = osr.SpatialReference()
            self.spatialRefOut.ImportFromEPSG(epsg_out)
            self.sr_trans = osr.CoordinateTransformation(self.spatialRefIn,self.spatialRefOut)
        else:
            self.spatialRefOut = self.spatialRefIn
            self.sr_trans = None
        self.driver = ogr.GetDriverByName('ESRI Shapefile')
        self.ds = self.driver.CreateDataSource(self.file_path)
        self.lyr = self.ds.CreateLayer(lyr_name, self.spatialRefOut, ogr.wkbPoint)
        self.f_dict = { 'date_loc'  : ogr.OFTString,
                        'date_utc'  : ogr.OFTString,
                        'time_loc'  : ogr.OFTString,
                        'time_utc'  : ogr.OFTString,
                        'img_path'  : ogr.OFTString,
                        'direction' : ogr.OFTReal,
                        'depth'     : ogr.OFTReal,
                        'temp'      : ogr.OFTReal,
                        'habitat'   : ogr.OFTString,
                        'hab_color' : ogr.OFTString,
                        'hab_num'   : ogr.OFTInteger,
                        'subst'     : ogr.OFTString, }
        for k,v in self.f_dict.iteritems():
            new_field = ogr.FieldDefn(k, v)
            if k == 'img_path':
                new_field.SetWidth(180)
            self.lyr.CreateField(new_field)
        
        self.lyrDefn = self.lyr.GetLayerDefn()
        self.feat_index = 0
        
    def __create_fuzzy_hab_fields(self,imgdir):
        """
        Create fields in the output shapefile to hold the fuzzy habitat
        classification data.
        """
        fhd = imgdir.fuzzy_habitat_dict
        habs = fhd.keys()
        for hab in habs:
            print "%s, type: %s" % (hab,str(type(hab)))
            print "%s, type: %s" % (str(ogr.OFTReal),str(type(ogr.OFTReal)))
            new_field = ogr.FieldDefn(str(hab),ogr.OFTReal)
            self.lyr.CreateField(new_field)
        
        
    def __validate_fp(self, file_path):
        """
        Validate a file path.
        """
        if os.path.basename(file_path).lower().endswith('.shp'):
            if os.path.exists(file_path):
                if self.overwrite:
                    os.remove(file_path)
                    return file_path
                else:
                    raise ValueError('That shapefile already exists and the bps_shp_exporter is not set to overwrite files.')
                    return None
            else:
                return file_path
        else:
            raise ValueError('That is not a shapefile.')
            return None
    
    def add_point_from_image(self, imf):
        """
        Take an image_file object (defined in photo_tagging.py) and make a 
        shapefile feature out of it.
        """
        hcd = CONF_HAB_COLOR_DICT
        hnd = CONF_HAB_NUM_DICT
        if imf.position:
            feat = ogr.Feature(self.lyrDefn)
            geom = imf.position.ogr_point
            geom.AssignSpatialReference(self.spatialRefIn)
            if self.sr_trans:
                geom.Transform(self.sr_trans)
            feat.SetGeometry(geom)
            feat.SetFID(self.feat_index)
            feat.SetField( 'date_loc', imf.datetime.strftime('%d/%m/%Y') )
            feat.SetField( 'date_utc', imf.utc_datetime.strftime('%d/%m/%Y') )
            feat.SetField( 'time_loc', imf.datetime.strftime('%H:%M:%S') )
            feat.SetField( 'time_utc', imf.utc_datetime.strftime('%H:%M:%S') )
            feat.SetField( 'img_path', str(imf.file_path) )
            if imf.exif_direction:
                feat.SetField( 'direction', imf.exif_direction )
            if imf.exif_depth:
                feat.SetField( 'depth', imf.exif_depth )
            if imf.xmp_temperature:
                feat.SetField( 'temp', imf.xmp_temperature )
            if imf.xmp_habitat:
                feat.SetField( 'habitat', imf.xmp_habitat )
                feat.SetField( 'hab_color', hcd[imf.xmp_habitat] )
                feat.SetField( 'hab_num', hnd[imf.xmp_habitat] )
            if imf.xmp_substrate:
                feat.SetField( 'subst', imf.xmp_substrate )
            # set fuzzy hab values
            if imf.xmp_fuzzy_hab_dict:
                for hab,val in imf.xmp_fuzzy_hab_dict:
                    feat.SetField( hab, val )
            self.lyr.CreateFeature(feat)
            feat.Destroy()
            self.feat_index += 1
            
    def write_prj(self):
        """
        create the *.prj file
        """
        outSpatialRef = self.spatialRefOut
        outSpatialRef.MorphToESRI()
        prj_fname = self.file_path[:-3] + 'prj'
        f = open(prj_fname, 'w')
        f.write(outSpatialRef.ExportToWkt())
        f.close()
        
    def write_shapefile(self, image_dir):
        """
        Create a shapefile from an image_directory object (defined in 
        photo_tagging.py).
        """
        #file_paths = [ os.path.join(image_dir,fp) for fp in os.listdir(image_dir) if fp.lower().endswith('.jpg') ]
        self.__create_fuzzy_hab_fields(image_dir)
        for imf in image_dir.images:
            self.add_point_from_image( imf )
        self.write_prj()
        self.ds.Destroy() # This makes the driver actually write out the shapefile
        return self.file_path
    
    
    
    
