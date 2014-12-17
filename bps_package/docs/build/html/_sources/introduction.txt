Introduction
============

Quantitative methods for the derivation of habitat maps from satellite and aerial imagery require reference data (sometimes called ground truth data) to create training sets for supervised classification and for the accuracy assessment of the resulting maps. These data generally need to represent the real world habitat type at many points and, in the case of benthic habitat mapping, the depth at each of those points can also be quite useful. Collecting and processing these data can be a challenging and time consuming task and may be part of the reason that too few benthic habitat mapping studies include adequate accuracy assessment. Benthic Photo Survey (BPS) was created to make this process less painful and, hopefully, make it easier to collect training data and produce an accuracy assessment of the resulting map.

What You Need to use BPS
------------------------

Benthic Photo Survey is designed to work with inexpensive and relatively easy to acquire equipment, partly because that's all that's really required and partly because that's all I can afford. Here's what you'll need:

1. A submersible digital camera that produces jpeg images. I use a `Panasonic Lumix DMC-TS4`_ in an `Ikelite housing`_. This camera has a built in compass that records the direction that the camera is facing when the photo is taken and BPS passes the direction into the shapefile that is created. However, this is not a requirement and any camera that produces jpeg images should be compatible with BPS.

2. A GPS that can be towed by a snorkeler or diver. If you're working with fairly high resolution imagery, you'll want a GPS receiver with WAAS capability. I am using a Garmin GPS 60 CSX. I tow mine in a small waterproof plastic box on a float. See `GPS Photo Transects for Benthic Cover Manual`_ by Roelfsema and Phinn [RP2010]_ for details on how to build a float. BPS can import NMEA text files and GPX files.

3. A depth logger is optional but if you're going to spend the time and money to go in the field, it seems worthwhile. BPS is set up to import log files from the `Sensus Ultra`_ depth and temperature logger. It should be fairly easy to adapt it to deal with a different logger but that would require a bit of coding.

4. A computer to run BPS. BPS was developed on Ubuntu but is also available for Windows. In theory it will run on Mac as well but has almost no testing there.


What BPS Actually Does
----------------------

There are 4 steps to what BPS does. 

1. It imports your GPS and/or depth and temperature logs into a database. 

2. It writes data from those logs to the Exif portion of each of your jpeg photos based on the time stamp on each photo and the time stamps in the respective logs. 

3. You use BPS to tag each photo with habitat and/or substrate information. This is also written to the Exif portion of each photo.

4. BPS can export a point shapefile with a point at each location where a photo was taken. Each point is attributed with the habitat, substrate, depth, temperature, direction, and file path to the photo.



.. _Panasonic Lumix DMC-TS4:
    http://panasonic.net/avc/lumix/compact/ts4_ft4/index.html
.. _Ikelite housing:
    http://www.ikelite.com/web_two/pan_ts3.html
.. _GPS Photo Transects for Benthic Cover Manual:
    http://ww2.gpem.uq.edu.au/CRSSIS/publications/GPS_Photo_Transects_for_Benthic_Cover_Manual.pdf
.. _Sensus Ultra: 
    http://reefnet.ca/products/sensus/

.. rubric:: References

.. [RP2010] Roelfsema, C., Phinn, S., 2010. Integrating field data with high spatial resolution 
    multispectral satellite imagery for calibration and validation of coral reef benthic community 
    maps. J. Appl. Remote Sens 4, 043527–043527.



