'''
Created 25 June 2012

To enable qick formatting of figures using some common matplotlib RC commands.

The module is simply imported, no methods exist
'''
import logging as l

from matplotlib import rc, rcParams, font_manager as fm, pyplot as plt
rc('font', **{'family':'sans-serif', 'sans-serif':['Helvetica', 'Arial'],
              'weight': ['lighter', 'normal']})
rc('text', usetex=True)
rc('axes', labelweight='light')
rc('xtick', direction='out')
rc('ytick', direction='out')
rc('axes', linewidth=.5)
# set outer border to be thin.

def bottomcolorbar(data=None, label=None):
    plt.colorbar(data, **{
        'orientation':'horizontal',
        'fraction':0.04,
        'pad':0.1,
        # 'format':tk.FormatStrFormatter(r"%1.1f\linebreak$\displaystyle m^{-1}sr^{-1}$"),
        'aspect':40,
        'drawedges':False
    }).set_label(label)

def equalaxis():
    '''
    Set the dimensions of the plot to be equal
    
    Equivalent To
    -------------
    >>> plt.axis('equal')
    
    '''
    plt.axis('equal')

# quick hacks.
def title(string):
    plt.suptitle(string)
def xlabel(string):
    plt.xlabel(string)
def ylabel(string):
    plt.ylabel(string)
