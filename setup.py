#!/usr/bin/env python

from distutils.core import setup

setup(name='thesis',
      version='0.01',
      description="Joe Young\'s Thesis code",
      author='Joe Young',
      author_email='joe.young@utah.edu',
      url='http://www.jsyoung.us/code/',
      packages=['thesis','thesis.formats','thesis.formats.rass','thesis.tools',
	'thesis.formats.ceil','thesis.formats.dem','thesis.rwp',
	'thesis.formats.isfs','thesis.formats.sonde','thesis.formats.lidar',
	'thesis.formats.hobo','thesis.formats.sodar'],
     )

