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

import os

LOCAL_TIME_ZONE = 'Pacific/Auckland' # Find your local timezone name here: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones

# This is all changing. User's should manage their preferences through the
# preferences dialog in the file menu of BPS. This file will should only
# affect the default values that show up the first time the application is run.
CONF_DB_PATH = os.path.join('test_data','db','raw_log.db')

CONF_WORKING_DIR = 'test_data'

CONF_QSETTINGS_DEVELOPER = 'jkibele'
CONF_QSETTINGS_APPLICATION = 'BenthicPhotoSurvey'

# the following three items are for testing and shouldn't need to be
# changed.
dt_testlog = os.path.join('test_data','sensus','sensus_test.csv')
gps_testlog = os.path.join('test_data','gps','GPS_20120722_194204.log')
test_image = os.path.join('test_data','images','P1000361.JPG')

#--------------bps_export------------------------------
CONF_INPUT_EPSG = 4326 #This is the projection that your GPS is recording in.
                        # You should probably just set your GPS to WGS84 and
                        # leave this set to 4326 - (that's the WGS84 EPSG)

CONF_OUTPUT_EPSG = 2193 # 2193 is the NZTM 2000 EPSG. This is what the exported
                        # outputs will come out as. If you're not in New Zealand
			# and you don't know what to set this too, just set it to
                        # 4326.
# The following list of habitats define your choices for tagging photos. You can
# change the habitats to whatever you want and change how many of them there are.
# Just don't mess up the brackets or quotes. If you get confused, just look up the
# syntax for a list stings in Python
CONF_HABITATS = ['Barrens', 'Kelp Forest', 'Mixed Weed', 'Red Foliose', 'Sand', 'Turf', 'Other']
# The following list of colors will at some point define how the habitats are displayed
# in outputs from BPS. For now there just needs to be the same number of items in
# this list as there is in CONF_HABITATS. So if you edit the number of habitats, just
# make sure the list of colors is the same length.
CONF_HAB_COLORS = ['#E5E5E5', '#8B6914', '#302713', '#A52A2A', '#FFC250', '#FFC0CB', '#0000FF']
# You should probably just leave these next 2 things alone
CONF_HAB_COLOR_DICT = dict( zip( CONF_HABITATS, CONF_HAB_COLORS ) )
CONF_HAB_NUM_DICT = dict( zip( CONF_HABITATS, range(1,len(CONF_HABITATS)+1) ) )
# This is the list of substrate types you can tag your photos with. Change it
# to suit your study area.
CONF_SUBSTRATES = ["Bedrock","Boulder","Cobble","Pebble","Shell","Sand","Mud"]
