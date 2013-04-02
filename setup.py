#!/usr/bin/env python

from distutils.core import setup

setup(name='BenthicPhotoSurvey',
      version='0.3.9',
      description='Benthic Photo Survey',
      author='Jared Kibele',
      author_email='jkibele@gmail.com',
      url='https://bitbucket.org/jkibele/benthic_photo_survey',
      packages=['benthic_photo_survey','docs','test_data'],
      package_data={'test_data': ['test_data/gps/gb*.gpx',
                                  'test_data/sensus/gb*.csv',
                                  'test_data/images/great_barrier_island/*.JPG'],
                    'docs': ['build/html/*',
                             'docs/build/html/_images/*',
                             'docs/build/html/_modules/*',
                             'docs/build/html/_sources/*',
                             'docs/build/html/_static/*',]},
      scripts=['benthic_photo_survey/benthic_photo_survey.py'],
      
     )

