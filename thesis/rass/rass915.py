"""
Joe Young March 2012
"""

import sys,time,datetime,calendar,array,os
from thesis.tools import *
from numpy import absolute,append,nanmax,nanmin,nan,zeros

from scipy.io.netcdf import netcdf_file as ncf


def rass (files,variable='tv',plot_levels=15, first_cutoff=2.5):
	"""
		ingest 915MhZ RASS

	"""
	files=sorted(files) # an attempt at orgainzing
	# initialize output lists
	X = zeros(len(files),dtype=int)
	Y = array.array('f')
	T = zeros((len(files),20)) # set a numpy array # FIXME - that 20 may not be stable!!!
	print "Finding RASS Files";
	n = 0 # a counter
	for file_dir in files:
		# EACH NETCDF FILE IS AN OBSERVATION!!!
		fname = file_dir.split("/")[-1]
		print file_dir
		# ok, begin/end check
		###if obtime < self.data.begin or obtime > self.data.end: continue
		try:
			nc = ncf(file_dir)
			obtime = calendar.timegm(time.strptime(fname.split(".")[1]+fname.split(".")[2]+"UTC",'%Y%m%d%H%M%S%Z'))
		except:
			# something there did not work, either in the name, or in the netcdf reading in general
			continue
		if variable not in nc.variables.keys():
			print variable,"Is not a valid RASS variable..."
			# be ince and return the valid variables
			print "Here are the valid variables: ",nc.variables.keys()
			exit()
		T[n] = nc.variables[variable][:]
		Y = nc.variables['height'][0] # numpy array! # heights
		X[n]=obtime
		nc.close()
		n+=1
	T[T==9999.] = nan # set T to be nan wherever it equals the null value

	return X,Y,T	

		
