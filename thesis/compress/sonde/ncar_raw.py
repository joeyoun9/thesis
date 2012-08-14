"""
read ncar QC'd soundings, and compress them into a single hdf5 document
"""
import numpy as np
from thesis.tools.pytables import *
from thesis.tools import s2t

def read(files,save):
	"""
		each file is a sounding (an ob) so, read the file, and save it at save
	"""
	#NOTE all soundings are size obs long, they must be filled in with zeros for this data format...
	# create the HDF5 document
	doc = h5(save)
	size = 5500 # this hopefully exceeds the size of the arrays
	doc.create(time2=size,pres=size,temp=size,dewpt=size,rh=size,u=size,v=size,dz=size,Z=size,lat=size,lon=size,gpsz=size)
	#Z=geopotenital height
	
	# now read the files!
	for f in sorted(files):
		fname = f.split('/')[-1]
		print 'reading',fname
		# get the initialization time from the filename -- risky, i know
		try:
			t0 = s2t(fname[1:15]+"UTC","%Y%m%d_%H%M%S%Z")
		except:
			#well, you do not meet our high standards for naming
			continue
		ts,hh,mm,ss,p,tc,tdc,rh,u,v,ws,wd,dz,Z,ln,lt,gpsZ = np.loadtxt(f,skiprows=14,unpack=True)
		# and append this data! I will trust the time seconds, instead of recomputing the time
		ts += t0
		# but, before that, we have to make them all the same size - size long
		nl = np.zeros(size - ts.shape[0])-999.00 # -999 array to fluff the end
		ts = np.concatenate((ts,nl))
		p  = np.concatenate((p,nl))
		tc = np.concatenate((tc,nl))
		tdc = np.concatenate((tdc,nl))
		rh = np.concatenate((rh,nl))
		u = np.concatenate((u,nl))
		v = np.concatenate((v,nl))
		dz = np.concatenate((dz,nl))
		ln = np.concatenate((ln,nl))
		lt = np.concatenate((lt,nl))
		Z = np.concatenate((Z,nl))
		gpsZ = np.concatenate((gpsZ,nl))
		doc.append(t0,persist=True,time2=ts,pres=p,temp=tc,dewpt=tdc,rh=rh,u=u,v=v,dz=dz,Z=Z,lat=lt,lon=ln,gpsz=gpsZ)
	doc.close()
