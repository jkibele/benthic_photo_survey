#!/usr/bin/env python

from distutils.core import setup

setup(name='BenthicPhotoSurvey',
      version='0.3.8',
      description='Benthic Photo Survey',
      author='Jared Kibele',
      author_email='jkibele@gmail.com',
      url='https://bitbucket.org/jkibele/benthic_photo_survey',
      packages=['benthic_photo_survey','docs','test_data'],
      include_package_data = True,
      scripts=['benthic_photo_survey/benthic_photo_survey.py'],
#      data_files=[('docs',['docs/build/html/*']),
#                  ('test_data/gps', ['test_data/gps/*.gpx']),
#                  ('test_data/images', ['test_data/images/great_barrier_island/*.JPG']),
#                  ('test_data/sensus', ['test_data/sensus/*.csv'])]
     )

