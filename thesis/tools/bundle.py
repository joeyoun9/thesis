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
import matplotlib.pyplot as plt
from thesis.tools import *
from thesis.pytables import h5
import thesis.tools.figure as TFigure
import cleanfig as cf
from cleanfig import *
from thesis.pcaps import *
from matplotlib.backends.backend_pdf import PdfPages

reserved_words = ['np','h5','cf','s2t','plt','iop','events']
'there are more, i have just been lazy.'


print __name__