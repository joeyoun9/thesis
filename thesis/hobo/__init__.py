"""
Hobo processing, from Hoch files
"""
import numpy as np
from thesis.tools.pytables import *
import time

def read(f,save):
	"""
		hobo lines are all in single files, so there should never be multiple files to read.
	"""
	# here is how the files are built, they are all nicely CSV
	# 5 colums M,D,Y,H,M (UTC) then
	# line 2 = latitude
	# line 3 = longitude
	# line 4 = elevation (best guess)
	# line 8 (9th line) is the beginning of data!
	
	fl = open(f,'rb')
	out=fl.read(3000) # that should be safe
	out = out.split('\r') # fun fact about hobo files, they are split exclusively with carriage returns
	fl.close()
	lats = out[2].split(',')[5:]
	lons = out[3].split(',')[5:]
	el = out[4].split(',')[5:]
	
	# so, those are the indices, where the positions of the hobos, and their best guess elevations
	# and yes, we will have to loop over the entire dataset, sadly
	
	# 1. create the hdf file
	doc = h5(save)
	doc.create(lats=len(lats),lons=len(lons),elev=len(el),temp=len(el))
	print "Reading the file"
	dat = np.loadtxt(f,skiprows=8,delimiter=',')
	
	print "Writing the data!"
	index_written=False
	for ob in dat:
		# this is the slow ugly part
		t = time.mktime((int(ob[2]),int(ob[0]),int(ob[1]),int(ob[3]),int(ob[4]),0,0,0,0))#hmm
		# this apppears to correctly assign the times
		if not index_written:
			index_written=True
			# save the data plus the indices
			doc.append(t,persist=True,lats=lats,lons=lons,elev=el,temp=ob[5:])
		else:
			doc.append(t,persist=True,temp=ob[5:])
	doc.close()
			
