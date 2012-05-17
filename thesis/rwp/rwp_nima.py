"""
Joe Young March 2012
"""

import sys,time,datetime,calendar,array,os
from thesis.tools import *
from thesis.tools.pytables import *
from numpy import absolute,append,nanmax,nanmin,nan,zeros

from scipy.io.netcdf import netcdf_file as ncf


def read (files,save):
	"""
		ingest RWP NIMA processed Data from the NCAR NetCDFs
		each file here is a day, with times as an element!

		This will use for loops, and it will go slowly...
	"""
	# then create the new file unless save is a file handle, in which case just save to that
	doc = h5(save) # establish the hdf5 object.
	doc.create(wspd=38,wdir=38,height=38,wvert=38,u=38,v=38,w=38,snrw=38,sw=38,edr=38)

	print "Finding RWP Files";
	for file_dir in sorted(files):
		
		fname = file_dir.split("/")[-1]
		if 'mom' in fname or 'rass' in fname: continue #rass and moment riffraf.
		print file_dir
		try:
			nc = ncf(file_dir)
		except:
			# something there did not work, either in the name, or in the netcdf reading in general
			continue
		# check to make sure this is the right kind of data, a full 38 obs
		l  = nc.dimensions['height']
		if l > 38:
			nc.close()
			continue
		begin = s2t(getattr(nc,'Data_start_time'),'%a %b  %d %H:%M:%S %Y %Z') #should work for PCAPS data
		for t in range(len(nc.variables['time'][:])):
			obtime = begin + nc.variables['time'][t]
			# now fetch all the desired variables and save them!
			wspd = nc.variables['wspd'][t]
			wdir = nc.variables['wdir'][t]
			wvert = nc.variables['wvert'][t]
			height = nc.variables['heights'][t]
			snrw = nc.variables['snrw'][t]
			u = nc.variables['u_classicC'][t] # constant, vs linear
			v = nc.variables['v_classicC'][t] # ditto
			w = nc.variables['w_classicC'][t] # ditto
			snrw = nc.variables['snrw'][t]
			sw = nc.variables['specWid'][t] 
			edr = nc.variables['edr'][t] # eddy dissipation rate
			
			print "Appending",obtime
			doc.append(obtime,persist=True,wspd=wspd,wdir=wdir,height=height,snrw=snrw,u=u,v=v,w=w,sw=sw,edr=edr)
			
		nc.close()
	doc.close()
	return True
