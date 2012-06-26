'''
Created 25 June 2012

To enable qick formatting of figures using some common matplotlib RC commands.

The module is simply imported, no methods exist
'''

from matplotlib import rc,rcParams


# make the font helvetica (thin, appaerntly)
rc('font', **{'family':'sans-serif', 'sans-serif':
     ['Helvetica']})
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'