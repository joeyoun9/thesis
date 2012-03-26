#!/usr/bin/env python

from distutils.core import setup

setup(name='thesis',
      version='0.01',
      description="Joe Young\'s Thesis code",
      author='Joe Young',
      author_email='joe.young@utah.edu',
      url='http://www.jsyoung.us/code/',
      packages=['thesis','thesis.rass',
	'thesis.ceil','thesis.dem','thesis.rwp',
	'thesis.isfs','thesis.sonde','thesis.lidar'],
     )

