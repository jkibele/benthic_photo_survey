#!/usr/bin/env python

from distutils.core import setup

setup(name='BenthicPhotoSurvey',
      version='0.3.18',
      description='Benthic Photo Survey',
      author='Jared Kibele',
      author_email='jkibele@gmail.com',
      url='https://bitbucket.org/jkibele/benthic_photo_survey',
      packages=['bps_package'],
      package_data={'bps_package': 
                                 ['test_data/gps/gb*.gpx',
                                  'test_data/sensus/gb*.csv',
                                  'test_data/images/*.JPG'
                                  'docs/build/html/*',
                                  'docs/build/html/_images/*',
                                  'docs/build/html/_modules/*',
                                  'docs/build/html/_sources/*',
                                  'docs/build/html/_static/*',
                                  'data/db/*.py',
                                  'data/images/*.py',
                                  'data/gps/*.py',
                                  'data/sensus/*.py']},
      scripts=['scripts/benthic_photo_survey.py'],
      
     )

