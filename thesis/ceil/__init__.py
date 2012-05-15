"""
This will house the three different readers, there is minimal intelligence here

you tell the reader the timestamp format (what created the file) and the datatype, I do the rest

"""
all=['ct12','cl31','ct25']

import ct25,ct12,cl31
from thesis.tools.pytables import *
from thesis.tools import s2t
import numpy as np


#WARNING -> this is quite slow!!!

def h5compress(files,ceilometer,creator='vaisala',save=False):
	"""
		create a h5 document from the file(s) given

		Inputs:
		files : a string or list of strings pertaining to files to be opened
		ceilometer : a string of either 
				ct12, ct25, cl31 
				specifying what kind of ceilometer this is
		creator: a string representing what program created this file
				a seclection of : vaisala, uunet, horel
				which represent their respective formats.
	"""
	"this function is basically a bunch of switches, it does depend on some knowledge about the instrument"
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
		doc.create(status=25,bs=250,height=250) # that is all
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
		doc.create(status=11,bs=250,height=250) 
		if creator == 'vaisala' or creator == 'uunet':
			split = C
			tsplit = A # times are before
			tkey = 0
		if creator == 'horel':
			split = A
			tsplit = C
			tkey = -1
	elif ceilometer == 'cl31':
		doc.create(status=13,bs=770,height=770) # this can vary!!! but, you might just have to know that in advance
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

		for o in text: #SLOOOOOOOOOOOOOW, but, this is the best way to do it
			# determine the time
			tt = o.split(tsplit)[tkey].strip()# try to clear the riffraff off

			# now use the specified time format
			try: 
				if creator == 'vaisala':
					t = s2t(tt+"UTC","-%Y-%m-%d %H:%M:%S%Z")
				elif creator == 'uunet':
					t = float(tt) # my favorite format...
				elif creator == 'horel':
					t = s2t(tt.replace('"','').strip()+"UTC","%m/%d/%Y %H:%M:%S%Z") # might be an error in that...
					#FIXME - he may be saving data in local time...
			except ValueError:
				# hmm, time format aint right, usually a sign of other issues, move along
				continue
			# then read the ob

			ob = o.split(tsplit)[tkey+1].strip() # hah! it works so simply!
			#FIXME - only split the ob once
			if ceilometer == 'ct12':
				out = ct12.read(ob)
			elif ceilometer == 'cl31':
				out = cl31.read(ob)
			else:
				out = ct25.read(ob)
			# and out is formatted to return a list of stats, a list of heights, and a list of backscatters
			if not out:
				# the processor did not like something, move on
				continue

			if f_prev == '':
				doc.append(t, persist=True, status=out['status'],bs=out['bs'],height=out['height']) # NON PERSISTENT
				f_prev = f
			else:
				doc.append(t, persist=True, status=out['status'],bs=out['bs']) # Don't save height anymore
		f_prev = f

		doc.close()# cleanup, since the append is persisent open


