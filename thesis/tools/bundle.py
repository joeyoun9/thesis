'''
This is a simple script which can be imported to the effect of 
compressing and streamlining other import operations for analysis
into a single simple 

from thesis.tools.bundle import *

Won't be fast, but it should be complete.
'''
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

logging.info('Execution Initiated')
import matplotlib
matplotlib.use('Agg')

# import the whole of numpy, it will be used everywhere.
import numpy as np
# Get NetCDF as well, it will also be needed.
from scipy.io.netcdf import netcdf_file as nc
import os, sys
from pylab import *
from scipy import *
import matplotlib.pyplot as plt
from thesis.tools import *
from thesis.tools.pytables import h5
import thesis.tools.figure as TFigure
from thesis.tools.figure import *
from thesis.tools.sounding import *
logging.debug('Importing Cleanfig')
import cleanfig as cf
from cleanfig import *
logging.debug('Cleanfig imported')
from thesis.pcaps import *
import thesis.pcaps.ceilometer.mlh as mlh
# Libraries for particle tracing in ceilometers.
from thesis.pcaps.ceilometer.particle import *
# Import structures for making mutliple page PDFs.
from matplotlib.backends.backend_pdf import PdfPages
# Import mapping libraries developed by myeslf in this package.
import thesis.tools.mymap as mymap
'Import structures for unique datasets'
import tables

from scipy.io import netcdf


reserved_words = ['np', 'h5', 'cf', 's2t', 'plt', 'iop', 'events', 'mlh', 'map']
'there are more, i have just been lazy.'


logging.info(__name__ + ' imported')
