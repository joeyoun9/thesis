#!/usr/bin/env python

from distutils.core import setup

setup(name='thesis',
      version='0.1',
      description="Joe Young\'s Thesis code",
      author='Joe Young',
      author_email='joe.young@utah.edu',
      url='http://www.jsyoung.us/code/',
      packages=['thesis',
                'thesis.compress',
                'thesis.compress.rass',
                'thesis.tools',
                'thesis.tools.core',
                'thesis.compress.ceil',
                'thesis.compress.dem',
                'thesis.compress.rwp',
                'thesis.compress.isfs',
                'thesis.compress.sonde',
                'thesis.compress.lidar',
                'thesis.compress.hobo',
                'thesis.compress.sodar',
                'thesis.analysis',
                'thesis.analysis.lidar',
                'thesis.analysis.pcaps',
                'thesis.analysis.lidar.mlh'
                ],
     )

