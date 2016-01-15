"""
Copyright (c) 2014, Jared Kibele
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of Benthic Photo Survey nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from photo_tagging import *
from preference_array import HabPrefArray
import osr

## Crap. Need to deal with hab color dict. Currently created in configuration.py
# that won't work with qsettings stuff

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
        self.settings = qsettings
        #-----Set up the shapefile-------------------------
        self.spatialRefIn = osr.SpatialReference()
        if self.settings:
            epsg_in, ok_in = qsettings.value("inputEPSG",CONF_INPUT_EPSG).toInt()
            epsg_out, ok_out = qsettings.value("outputEPSG",CONF_OUTPUT_EPSG).toInt()
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
        # stupid shapefile field names can only have 10 characters
        for hab in [ h[0:10] for h in habs ]:
#            print "%s, type: %s" % (hab,str(type(hab)))
#            print "%s, type: %s" % (str(ogr.OFTReal),str(type(ogr.OFTReal)))
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
        hpa = HabPrefArray().loadFromSettings()
        hcd = hpa.hab_color_dict
        hnd = hpa.hab_number_dict
        #print hcd
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
                #print "Setting color for %s to %s." % (type(imf.xmp_habitat),type(hcd[imf.xmp_habitat]))
                feat.SetField( 'hab_color', hcd[imf.xmp_habitat] )
                feat.SetField( 'hab_num', hnd[imf.xmp_habitat] )
            if imf.xmp_substrate:
                feat.SetField( 'subst', imf.xmp_substrate )
            # set fuzzy hab values
            if imf.xmp_fuzzy_hab_dict:
                for hab,val in imf.xmp_fuzzy_hab_dict.items():
                    # have to slice hab name to get only 10 characters
                    # because of stupid 10 ch limit for shapefiles
                    feat.SetField( str(hab[0:10]), val )
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
        self.__create_fuzzy_hab_fields(image_dir)
        for imf in image_dir.images:
            self.add_point_from_image( imf )
        self.write_prj()
        self.ds.Destroy() # This makes the driver actually write out the shapefile
        return self.file_path
