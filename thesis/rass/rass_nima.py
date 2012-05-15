"""
Joe Young March 2012
"""

import sys,time,datetime,calendar,array,os
from thesis.tools import *
from thesis.tools.pytables import *
from numpy import absolute,append,nanmax,nanmin,nan,zeros

from scipy.io.netcdf import netcdf_file as ncf

def rass (files,variable='wspd',nanvalue=nan,save=False):
	"""
		ingest RWP NIMA processed Data from the NCAR NetCDFs
		each file here is a day, with times as an element!

		This will use for loops, and it will go slowly...
	"""
	if save:
		# then create the new file unless save is a file handle, in which case just save to that
		doc = h5(save) # establish the hdf5 object.
		doc.create(tvu=20,tvc=20,height=20,snrtv=20)
	else:
		# i Only save
		raise Exception('Sorry, this requires somewhere to write the HDF5')
		exit()

	files = sorted(files) # a last resort effort to sort these turkies
	# initialize output lists
	X = zeros(len(files),dtype=int)
	Y = array.array('f')
	T = zeros((len(files),38)) # set a numpy array # FIXME - that 20 may not be stable!!!
	print "Finding RASS Files";
	for file_dir in files:
		
		fname = file_dir.split("/")[-1]
		if 'mom' in fname or 'winds' in fname: continue #wind profiler and moment riffraf.
		print file_dir
		try:
			nc = ncf(file_dir)
		except:
			# something there did not work, either in the name, or in the netcdf reading in general
			continue
		# check to make sure this is the right kind of data, full 45 obs, not a low 38
		l  = nc.dimensions['height']
		if l > 20:
			nc.close()
			continue
		begin = s2t(getattr(nc,'Data_start_time'),'%a %b  %d %H:%M:%S %Y %Z') #should work for PCAPS data
		for t in range(len(nc.variables['time'][:])):
			obtime = begin + nc.variables['time'][t]
			# now fetch all the desired variables and save them!
			tvu = nc.variables['tv'][t] # uncorrected virtual temp
			tvc = nc.variables['tvc'][t] # vertical motion corrected
			snrtv = nc.variables['snrtv'][t]
			height = nc.variables['heights'][t]
			
			print "Appending",obtime
			doc.append(obtime,persist=True,height=height,tvu=tvu,tvc=tvc,snrtv=snrtv)
			
		nc.close()
	doc.close()
	return True


		
