'''
Created 25 June 2012

To enable qick formatting of figures using some common matplotlib RC commands.

The module is simply imported, no methods exist
'''

from matplotlib import rc,rcParams,font_manager as fm,pyplot as plt

#font = fm.FontProperties().set_family('Helvetica')
print fm.FontProperties().get_family() 
# make the font helvetica (thin, appaerntly)
rcParams['font.sans-serif']='Geneva, Helvetica, Arial, sans-serif, Bitstream Vera Sans'
rcParams['font.weight']='light,lighter,bold,normal'
try:
    'wrapped for safety'
    rcParams['axes.labelweight']='light'
except:
    pass

#rc('font', **{'family':'sans-serif', 'sans-serif':
#     'Helvetica','weight':'bold'})
# print font information

'''
Method for outlining available fonts on macs
'''
if False:
    for font in fm.OSXInstalledFonts():
        print font


rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['axes.linewidth']=.5 # set the outer border to be thin

#rcParams['text.usetex']= True

plt.grid()
'this does not seem to robustly add grids to everything'

def bottomcolorbar(data=None,label=None):
    plt.colorbar(data,**{
        'orientation':'horizontal',
        'fraction':0.04,
        'pad':0.1,
        #'format':tk.FormatStrFormatter(r"%1.1f\linebreak$\displaystyle m^{-1}sr^{-1}$"),
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
def title(str):
    plt.suptitle(str)
def xlabel(str):
    plt.xlabel(str)
def ylabel(s):
    plt.ylabel(s)
    