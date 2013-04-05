#!/usr/bin/env python

from distutils.core import setup

setup(name='thesis',
      version='1.6',
      description="Joe Young\'s Thesis code",
      author='Joe Young',
      author_email='joe.young@utah.edu',
      url='http://www.jsyoung.us/code/',
      packages=['thesis',
                'thesis.tools',
                'thesis.tools.core',

                'thesis.compress',
                'thesis.compress.rass',
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
                'thesis.analysis.lidar.ceil',
                'thesis.analysis.lidar.basic',
                'thesis.analysis.lidar.mlh',
                'thesis.analysis.pcaps',
                ],
     )

