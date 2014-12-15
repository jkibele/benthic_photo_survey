.. Benthic Photo Survey documentation master file, created by
   sphinx-quickstart on Fri Mar  8 15:07:10 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Benthic Photo Survey's documentation!
================================================

Benthic Photo Survey (BPS) is a software tool (written in Python) that is intended to simplify the task of collecting reference data (sometimes called groundtruth data) for remote sensing of the marine environment. Using a digital camera in a water proof housing, a consumer grade handheld GPS, and (optionally) a depth logger a user can collect data in the field.

The photos and logs (GPS and Depth) are then loaded into BPS. BPS can then tag the photos with position, depth, and temperature (if using the Sensus Ultra depth/temperature logger). The the users can view each photo in BPS and tag each photo with a substrate and habitat type. All data (position, depth, temperature, habitat, and substrate) are stored in the exif portion of the jpeg photos. 

Once the photos are all tagged, BPS can export a GIS Shapefile with habitat, substrate, depth, and temperature attributed points for each photo's location. This shapefile can then be used to create a training set for supervised classification or as reference data for accuracy assessment.

.. image:: images/BPS_overview.png

Contents
--------

.. toctree::
   :maxdepth: 3

   introduction
   installation
   tutorial
   code
