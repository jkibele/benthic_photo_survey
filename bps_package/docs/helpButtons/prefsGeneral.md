General Preferences
===================

Database
--------
Use the '...' button to choose where to save your database. You should choose a file name with a .db extention. If you designate a file that doesn't exist it will be created for you. This database will be used to store GPS and depth records so that they can be synced up with photos.


Working Directory
-----------------
This is the directory that BPS will look in when you choose 'Load GPS Log', 'Load Depth Log', or 'Load Photos' from the file menu.


Input EPSG
----------
This is the projection that your GPS is recording in. You should probably just set your GPS to WGS84 and leave this set to 4326 - (that's the WGS84 EPSG). If you don't know what I'm talking about, you should probably just leave it set to 4326.


Output EPSG
-----------
BPS will try to save your shapefile using the projection referenced by this EPSG. If you're in New Zealand you might want to use 2193 (NZTM 2000). If you're not sure, you should set it to 4326 (WGS84).


Dodgy Features
--------------
If this box is checked you'll have access to some features that will allow you to potentially confuse you and muck up your data. You'll be able to shift the time codes in your photos and/or depth records. You might need to do that but BACK UP YOUR DATA first. 
