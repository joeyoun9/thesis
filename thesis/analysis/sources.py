'''
Created on Feb 18, 2013

@author: jyoung

This is not to be included with a PUBLIC version of this repo. Somehow I willl
need to remove references to the existence of this module
'''
from thesis.tools.core.objects import CoreObject as o

data_dir = '/uufs/chpc.utah.edu/common/home/whiteman-group1/jyoung/'
projects = data_dir + 'projects'

dropbox = '/uufs/chpc.utah.edu/common/home/u0713352/Dropbox/figures/'

# pcaps data
pcaps = o()
pcaps.raw = '/uufs/chpc.utah.edu/common/home/horel-group/pcaps.utah.edu/'
pcaps.data = projects + '/pcaps'
pcaps.ncar = o()
pcaps.sodar = data_dir + 'hdf5/pcaps/sodar.h5'
pcaps.ncar.ceil = data_dir + 'hdf5/pcaps/ncar_ceil.h5'
pcaps.ncar.rass = data_dir + 'hdf5/pcaps/ncar_rass_nima.h5'  # nima filtered
pcaps.ncar.rwp = data_dir + 'hdf5/pcaps/ncar_rwp_nima.h5'
pcaps.ncar.rwpm = data_dir + 'hdf5/pcaps/ncar_rwp_mom_nima.h5'
pcaps.ncar.rawinsondes = data_dir + 'hdf5/pcaps/ncar_rawinsondes.h5'
pcaps.dugway = o()
pcaps.dugway.ditto = data_dir + 'hdf5/pcaps/ditto_ceil.h5'
pcaps.dugway.horizontal = data_dir + 'hdf5/pcaps/horizontal_ceil.h5'
pcaps.daq = o()
pcaps.daq.pm10_txt = projects + '/pcaps/PM10.txt'
pcaps.daq.pm25_txt = projects + '/pcaps/PM25.txt'
pcaps.daq.pm10 = projects + '/pcaps/pm10.npz'
pcaps.daq.pm25 = projects + '/pcaps/pm25.npz'
# surface data sets...
pcaps.hobo = o()
pcaps.hobo.harker = data_dir + 'hdf5/pcaps/harker_hobos.h5'
pcaps.hobo.grandeur = data_dir + 'hdf5/pcaps/gradneur_hobos.h5'
pcaps.isfs = o()
pcaps.isfs.nc = o()
pcaps.isfs.nc.nov = data_dir + '/projects/pcaps/'
# Also make sure you add ISS2 - that is where the ceilometer was
# create a processed data object for computed datasets
pcaps.proc = o()
pcaps.proc.ceil_pm_filter = projects + '/pcaps/ceil_pm_filter.npz'

# bingham data
bcm = o()
bcm.dir = projects + '/bmcap'
bcm.year1 = o()
bcm.year2 = o()
bcm.sites = o()
# year 1 (2010-2011)
bcm.year1.hobos_rh = bcm.dir + '/year1/rh_hobos.h5'
bcm.year1.hobos_t = bcm.dir + '/year1/t_hobos.h5'
bcm.year1.lidar = bcm.dir + '/year1/lidar.h5'
# year 2 (2011 - 2012)
bcm.year2.lidar = bcm.dir + '/year2/lidar.h5'
bcm.year2.inpit = bcm.dir + '/year2/inpit_ceil.h5'
bcm.year2.outpit = bcm.dir + 'outpit_ceil.h5'
# Simple Location files
bcm.sites.year1 = bcm.dir + '/year1/kenne_locations.txt'
bcm.sites.year2 = bcm.dir + '/year2/kenne_locations.txt'
bcm.sites.hobos1 = bcm.dir + '/year1/hobo_locations.txt'
bcm.sites.hobos2 = bcm.dir + '/year2/hobo_locations.txt'


# Ceilometer Network Data
ceil = o()
# at present, there are no ceilometer datasets available from this set

# digital elevation models:
dem = o()
dem.slv = data_dir + 'hdf5/pcaps/dem_slc_10m.h5'
dem.bcm2011 = data_dir + 'projects/bmcap/year2/dem_10m.h5'
dem.bcm2010 = data_dir + 'projects/bmcap/year1/dem_10m.h5'




