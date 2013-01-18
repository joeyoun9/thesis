'''
This is a simple script which can be imported to the effect of 
compressing and streamlining other import operations for analysis
into a single simple 

from thesis.tools.bundle import *

Won't be fast, but it should be complete.
'''
import matplotlib
matplotlib.use('Agg')

import numpy as np
'this may be a painful addition'
import os,sys
from pylab import *
from scipy import *
import matplotlib.pyplot as plt
from thesis.tools import *
from thesis.tools.pytables import h5
import thesis.tools.figure as TFigure
from thesis.tools.figure import *
from thesis.tools.sounding import *
import cleanfig as cf
from cleanfig import *
from thesis.pcaps import *
import thesis.pcaps.ceilometer.mlh as mlh
from thesis.pcaps.ceilometer.particle import *
from matplotlib.backends.backend_pdf import PdfPages
import thesis.tools.mymap as mymap # this is a risky thing to use as a reserved word
'Import structures for unique datasets'
import tables
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

from scipy.io import netcdf


reserved_words = ['np','h5','cf','s2t','plt','iop','events','mlh', 'map']
'there are more, i have just been lazy.'


logging.info(__name__+'imported')