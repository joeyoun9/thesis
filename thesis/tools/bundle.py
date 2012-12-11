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
from pylab import *
from scipy import *
import matplotlib.pyplot as plt
from thesis.tools import *
from thesis.tools.pytables import h5
import thesis.tools.figure as TFigure
from thesis.tools.figure import *
import cleanfig as cf
from cleanfig import *
from thesis.pcaps import *
import thesis.pcaps.ceilometer.mlh as mlh
from thesis.pcaps.ceilometer.particle import *
from matplotlib.backends.backend_pdf import PdfPages
'Import structues for unique datasets'
import tables
from scipy.io import netcdf

reserved_words = ['np','h5','cf','s2t','plt','iop','events','mlh']
'there are more, i have just been lazy.'


print __name__,'imported'