LOCAL_TIME_ZONE = 'Pacific/Auckland' # Find your local timezone name here: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones

db_path = 'data/db/raw_log.db'
dt_testlog = 'test_data/sensus/sensus_test.csv'
gps_testlog = 'test_data/gps/GPS_20120722_194204.log'
test_image = 'test_data/images/P6251541.jpg'

#--------------bps_export------------------------------
CONF_INPUT_EPSG = 4326 #This is the projection that your GPS is recording in.
                        # You should probably just set your GPS to WGS84 and 
                        # leave this set to 4326 - (that's the WGS84 EPSG)
                        
CONF_OUTPUT_EPSG = 2193 # 2193 is the NZTM 2000 EPSG. This is what the exported
                        # outputs will come out as.
CONF_HABITATS = ["Sand", "Turf", "Barrens", "Mixed Weed", "Kelp Forest", "Other"]
CONF_SUBSTRATES = ["Bedrock","Boulder","Cobble","Pebble","Shell","Sand","Mud"]
