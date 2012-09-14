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
	doc.create(time2=size,pres=size,temp=size,dewpt=size,rh=size,wdir=size,wspd=size,dz=size,Z=size,lat=size,lon=size,gpsz=size)
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
			print 'bad file name'
			continue
		'''
		For the raw files, we have to go line by line... sad I know
		'''
		ts = np.empty(size)
		p  = np.empty(size)
		tc = np.empty(size)
		tdc = np.empty(size)
		rh = np.empty(size)
		wdir = np.empty(size)
		wspd = np.empty(size)
		dz = np.empty(size)
		ln = np.empty(size)
		lt = np.empty(size)
		Z = np.empty(size)
		gpsZ = np.empty(size)
		l=0 #keeps track of the current line
		f = open(f)
		for line in f:
			print line[10]
			if not line[10]=='S': continue #dont record pre-launch
			line  = line.split()
			if not line[1] == 'S00': continue #not satisfactory
			#NOTE TIMES ARE NOT INCLUDED HERE!!!
			p[l]=line[5]
			tc[l]=line[6]
			#tdc[l]=line[7]
			rh[l]=line[7]
			wdir[l]=line[8]
			wspd[l]=line[9]
			dz[l]=line[10]
			ln[l]=line[11]
			lt[l]=line[12]
			Z[l]=line[13]
			gpsZ[l]=line[19]
			print 'ob',len(tc)
			
			l+=1
			
		f.close()
		
		doc.append(t0,persist=True,time2=ts,pres=p,temp=tc,dewpt=tdc,rh=rh,wspd=wspd,wdir=wdir,dz=dz,Z=Z,lat=lt,lon=ln,gpsz=gpsZ)
	doc.close()
