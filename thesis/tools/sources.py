'''
Created on Feb 18, 2013

@author: jyoung

This is not to be included with a PUBLIC version of this repo. Somehow I willl
need to remove references to the existence of this module
'''
from thesis.tools.objects import go as o

data_dir = '/uufs/chpc.utah.edu/common/home/whiteman-group1/jyoung/'
dropbox = '../../../Dropbox/figures/'
# pcaps data
pcaps = o()
pcaps.raw = '/uufs/chpc.utah.edu/common/home/horel-group/pcaps.utah.edu/'
pcaps.ncar = o()
pcaps.sodar = data_dir + 'hdf5/pcaps/sodar.h5'
pcaps.ncar.ceil = data_dir + 'hdf5/pcaps/ncar_ceil.h5'
pcaps.ncar.rass = data_dir + 'hdf5/pcaps/ncar_rass_nima.h5'  # nima filtered
pcaps.ncar.rwp = data_dir + 'hdf5/pcaps/ncar_rwp_nima.h5'
pcaps.ncar.rwpm = data_dir + 'hdf5/pcaps/ncar_rwp_mom_nima.h5'
pcaps.ncar.rawinsondes = data_dir + 'hdf5/pcaps/ncar_rawinsondes.h5'
pcaps.ditto = data_dir + 'hdf5/pcaps/ditto_ceil.h5'
pcaps.horizontal = data_dir + 'hdf5/pcaps/horizontal_ceil.h5'


# bingham data
bcm = o()
bcm.year1 = o()
bcm.year2 = o()
bcm.year2.hobos_rh = data_dir + 'hdf5/BCM/kenne_rh_hobos2011.h5'
bcm.year2.hobos_t = data_dir + 'hdf5/BCM/kenne_t_hobos2011.h5'
# some HOBO data from year 1 is actually with PCAPS -
bcm.year1.hobos = data_dir + 'projects/bmcap/year1/hobo_locations.txt'
bcm.year1.locations = data_dir + 'projects/bmcap/year1/kenne_locations.txt'




# Ceilometer Network Data
ceil = o()
# at present, there are actually no ceilometer datasets available from this set

# digital elevation models:
dem = o()
dem.slv = data_dir + 'hdf5/pcaps/dem_slc_10m.h5'
dem.bcm2011 = data_dir + 'hdf5/BCM/dem_BCM2011_10m.h5'
dem.bcm2010 = data_dir + 'hdf5/BCM/dem_BCM2010_10m.h5'

# surface data sets...
pcaps.hobo = o()
pcaps.hobo.harker = data_dir + 'hdf5/pcaps/harker_hobos.h5'
pcaps.hobo.grandeur = data_dir + 'hdf5/pcaps/gradneur_hobos.h5'
pcaps.isfs = o()
pcaps.isfs.nc = o()
pcaps.isfs.nc.nov = data_dir + '/projects/pcaps/'
# Also make sure you add ISS2 - that is where the ceilometer was


