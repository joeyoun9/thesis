'''
This is a simple script which can be imported to the effect of 
compressing and streamlining other import operations for analysis
into a single simple 

from thesis.tools.bundle import *

Won't be fast, but it should be complete.
'''
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s: %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S')

logging.info('Execution Initiated')
import matplotlib
matplotlib.use('Agg')
import os

# import the whole of numpy, it will be used everywhere.
import numpy as np
from scipy.io.netcdf import netcdf_file as nc
import os, sys
from pylab import *
from scipy import *
# the sources library was implemented
# in a non-standard way for various reasons
import sources as srcs
s = srcs
sources = srcs

import matplotlib.pyplot
# add a method to plt to save as the name of the file called
class newplt(matplotlib.pyplot):
    def saveF(self, ext='png'):
        f = os.path.split(__file__)[-1][:-3]
        fname = srcs.dropbox + '/paper_figures/' + f + 'ext'
        logging.debug('Saving file as ' + fname)
        self.savefig(fname)

plt = newplt()

from . import *
from core.pytables import h5
import figure as TFigure
from figure import *
from sounding import *
import cleanfig
from cleanfig import *
from thesis.analysis import *
from thesis.analysis.pcaps import *
import thesis.analysis.lidar.mlh as mlh
from thesis.analysis.lidar.particle import *
from matplotlib.backends.backend_pdf import PdfPages
import mymap as mymap
import tables


logging.info(__name__ + ' imported')
