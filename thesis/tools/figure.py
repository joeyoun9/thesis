'''
Created 25 June 2012

To enable qick formatting of figures using some common matplotlib RC commands.

The module is simply imported, no methods exist
'''

from matplotlib import rc,rcParams,font_manager as fm,pyplot as plt

#font = fm.FontProperties().set_family('Helvetica')
print fm.FontProperties().get_family() 
# make the font helvetica (thin, appaerntly)
rc('font', **{'family':'sans-serif', 'sans-serif':
     'Arial','weight':'heavy'})
# print font information

'''
Method for outlining available fonts...
'''
'''
for font in fm.OSXInstalledFonts():
    print font
'''

rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['axes.linewidth']=.5 # set the outer border to be thin

def bottomcolorbar(data=None):
    plt.colorbar(data,**{
        'orientation':'horizontal',
        'fraction':0.04,
        'pad':0.1,
        #'format':tk.FormatStrFormatter(r"%1.1f\linebreak$\displaystyle m^{-1}sr^{-1}$"),
        'aspect':40,
        'drawedges':False
    })