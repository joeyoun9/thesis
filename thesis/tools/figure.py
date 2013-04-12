'''
Created 25 June 2012

To enable qick formatting of figures using some common matplotlib RC commands.

The module is simply imported, no methods exist
'''
import logging as l

from matplotlib import rc, rcParams, font_manager as fm, pyplot as plt
# rc('font', **{'family':'sans-serif', 'sans-serif':['Helvetica', 'Arial'],
#              'weight': ['lighter', 'normal']})
# removed in favor of latex font -JSY 12Apr2013

rc('text', usetex=True)
rc('font', family='serif', weight=['lighter', 'normal'])
# rc('axes', labelweight='light')
rc('xtick', direction='out')
rc('ytick', direction='out')
rc('axes', linewidth=1)
# set outer border to be thin. - or not (JSY 21Mar2013)

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


def frac_mm(mm, plt=plt):
    '''
    Calculate the resulting figure fractions for a specified number of mm
    Though the figure is in inches
    '''
    pass
    # pipeDream
