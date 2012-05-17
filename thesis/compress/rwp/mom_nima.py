"""
Joe Young March 2012
Read RWP NIMA Moment datasets
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
	size = 38 # this is how long the profiles are (FOR PCAPS - they were 45 during the run-up to PCAPS)
	# NOTE this code is disregarding many of the potentially interesting datasets within this data...
	doc.create(height=size,beamnum=1,elevation=1,az=1,vel=size,snr=size,sw=size,noise=size,mom1Conf=size,mom2Conf=size,power=size,poptemp=size,
		qc=size,interpv=size,iverr=size,clutter=size,othersig=size)

	print "Finding RWP Files";
	for file_dir in sorted(files):
		
		fname = file_dir.split("/")[-1]
		if 'mom' not in fname or 'rass' in fname: continue #rass and rwp riffraf.
		print file_dir
		try:
			nc = ncf(file_dir)
		except:
			# something there did not work, either in the name, or in the netcdf reading in general
			continue
		# check to make sure this is the right kind of data, a full 38 obs
		l  = nc.dimensions['height']
		if l > size:
			print "Wrong length:",l
			nc.close()
			continue
		begin = s2t(getattr(nc,'Data_start_time'),'%a %b  %d %H:%M:%S %Y %Z') #should work for PCAPS data
		for t in range(len(nc.variables['time'][:])):
			obtime = begin + nc.variables['time'][t] # yay, this still works!
			# now fetch all the desired variables and save them!
			beamnum = nc.variables['beamNum'][t]
			elevation = nc.variables['elevation'][t]
			az = nc.variables['azimuth'][t]
			height = nc.variables['heights'][t] # THIS ACTUALLY CHANGES HERE...
			snr = nc.variables['sigNoiseRatio'][t]
			vel = nc.variables['vel'][t] # constant, vs linear
			sw = nc.variables['specWid'][t] # ditto
			noise = nc.variables['noise'][t] # ditto
			m1c = nc.variables['mom1Conf'][t] # velocity
			m2c = nc.variables['mom2Conf'][t] # spectrum width
			power = nc.variables['power'][t]
			poptemp = nc.variables['popTemp'][t]
			qc = nc.variables['qualityControl'][t]
			interpv = nc.variables['interpVel'][t]
			iverr = nc.variables['errorVel'][t]
			clutter = nc.variables['clutter'][t]
			os = nc.variables['othersig'][t] #non-atmospheric signals
			
			#print "Appending",obtime
			doc.append(obtime,persist=True,height=height,beamnum=[beamnum],elevation=[elevation],az=[az],vel=vel,sw=sw,snr=snr,noise=noise,mom1Conf=m1c,
				mom2Conf=m2c,power=power,poptemp=poptemp,qc=qc,interpv=interpv,iverr=iverr,clutter=clutter,othersig=os)
			
		nc.close()
	doc.close()
	return True
