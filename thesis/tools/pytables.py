"""
Tools for checking times and whatont
"""
import tables
import numpy as np


def createhdf(file,**variables):
	# create an hdf5 table for use with datasets, ideally of known size...
	# variables specifies what variables will be filled in this archive
	#FIXME  - only one category available.
	f = tables.openFile(file,mode='w', title='ms')
	filters =  tables.Filters(complevel=6, complib='zlib')#blosc
	for k in variables:
		# create the variable called k, with length variables[k]
		f.createEArray('/',k,tables.Float32Atom(),(0,variables[k]),filters=filters.copy())	
	# the time table is a permenant feature
	time_desc = {'time': tables.FloatCol(pos=1),
		'key':tables.IntCol(8,pos=2),
	}
	time = f.createTable('/','time',time_desc,filters=filters.copy())
	meta = f.createTable('/','meta',{'high_key': tables.IntCol(8),'max_time':tables.FloatCol()},filters=filters.copy())
	meta.append([(0,0)]) # give an initial value

	return f # and produce the file




