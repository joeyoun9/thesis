"""
Tool for reading and compressing a small number of ceilometer record files

Joe Young, June 2012
"""
all=['ct12','cl31','ct25']

import ct25,ct12,cl31
from thesis.tools.pytables import *
from thesis.tools import s2t
import numpy as np


#WARNING -> this is quite slow!!!

def h5compress(files,ceilometer,creator='vaisala',save=False):
	"""
		Compress a ceilometer raw ascii file into the thesis-formatted HDF5
		file for quicker analysis. The methods here are rather slow, and are
		only formatted for the ceilometer types and ascii formats from
		
		Vaisala recording software (ceilview)(leading string)
		UUnetwork formatting (leading epoch)
		Horel (trailing strings)
		
		

		Parameters
		----------
		files : str/list
			a string or list of strings pertaining to files to be opened
		ceilometer : string:
				a string of either 
				ct12, ct25, cl31 
				specifying what kind of ceilometer this is
		creator: str, opt
				a string representing what program created this file
				a seclection of : vaisala, uunet, horel
				which represent their respective formats.
		save : str
			the location for the HDF5 document to be created
	"""
	#FIXME - this is going to account for the settings on the ceilometers in pcaps and uunet ct12s(which do not vary)
	
	if not save:
		raise Exception('Yeah, we needed you to specify an output file')
		exit() # though raise should have done that
	# 1. Create the output document
	doc = h5(save)

	A = unichr(001) # ct25/cl31 BOM (pre code)
	B = unichr(002) # beginning of message - after code
	C = unichr(003) # end of message
	D = unichr(004) # end of string - cl31
	if ceilometer == 'ct12':
		doc.create(indices={'height':250},status=25,bs=250) # that is all
		# determine splits
		if creator == 'vaisala' or creator == 'uunet':
			split = C
			tsplit = B # times are before
			tkey = 0
		if creator == 'horel':
			split = B
			tsplit = C
			tkey = -1

	elif ceilometer == 'ct25':
		doc.create(indices={'height':240},status=11,bs=240) 
		if creator == 'vaisala' or creator == 'uunet':
			split = C
			tsplit = A # times are before
			tkey = 0
		if creator == 'horel':
			split = A
			tsplit = C
			tkey = -1
	elif ceilometer == 'cl31':
		doc.create(indices={'height':770},status=13,bs=770) # this can vary!!! but, you might just have to know that in advance
		if creator == 'vaisala' or creator == 'uunet':
			split = D
			tsplit = A # times are before
			tkey = 0
		if creator == 'horel':
			split = A
			tsplit = D
			tkey = -1
	else:
		raise ValueError('Your input for ceilometer type was not valid')
	print "File Initialized"
	# now read the file, and get the times as per the formatting
	# always split by one thing, to get ob plus time, and then split by the other to isolate the time
	if type(files) == str:
		files = [files]
	f_prev = '' # keep track to prevent doubling up
	for f in sorted(files): # sort the darn things
		# no binary files!
		fname = f.split('/')[-1]
		if fname[0] == '.': continue #binary
		print 'reading',fname
		if f == f_prev:
			continue # we already read a file with this name #FIXME - filenames can double???
		# open the file
		fh = open(f,'r')
		text = fh.read().split(split)#ugh, read the whole thing!
		fh.close()

		for o in text: #SLOW
			# determine the time
			tt = o.split(tsplit)[tkey].strip()# try to clear the riffraff off
			try: 
				if creator == 'vaisala':
					t = s2t(tt+"UTC","-%Y-%m-%d %H:%M:%S%Z")
				elif creator == 'uunet':
					t = float(tt) # my favorite format...
				elif creator == 'horel':
					t = s2t(tt.replace('"','').strip()+"UTC","%m/%d/%Y %H:%M:%S%Z") # might be an error in that...
					#FIXME - he may be saving data in local time...
			except ValueError:
				continue #a sign that this is not a proper ob
			# then read the ob

			ob = o.split(tsplit)[tkey+1].strip() 
			if ceilometer == 'ct12':
				out = ct12.read(ob)
			elif ceilometer == 'cl31':
				out = cl31.read(ob)
			else:
				out = ct25.read(ob)
			if not out:
				continue

			if f_prev == '':
				doc.loadIndices(height=out['height'])
				f_prev = f
			doc.append(t, persist=True, status=out['status'],bs=out['bs'])
		f_prev = f
		doc.close()


