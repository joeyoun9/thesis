"""
Tools for checking times and whatont
"""
import tables
import numpy as np


def h5create(f,close=True,**variables):
	# create an hdf5 table for use with datasets, ideally of known size...
	# variables specifies what variables will be filled in this archive
	"""
		Inputs:
		close        - boolean to tell if the file should be returned or closed
		**variables  - dict of {'name':[length(integer),]} values to tell the variables
	"""
	#FIXME  - only one category available.
	f = openw(f)
	filters =  tables.Filters(complevel=6, complib='zlib')#blosc
	for k in variables:
		# create the variable called k, with length variables[k]
		# allow for multi-dimensional data
		dims = (0,)
		if type(variables[k]) == list:
			# then this is multidimensional
			for i in variables[k]: #it had better be a list
				dims = dims + (i,)
		else:
			dims = (0,variables[k])#hmm
		f.createEArray('/',k,tables.Float32Atom(),dims,filters=filters.copy())	
	# the time table is a permenant feature
	time_desc = {'time': tables.FloatCol(pos=1),
		'key':tables.IntCol(8,pos=2),
	}
	time = f.createTable('/','time',time_desc,filters=filters.copy())
	meta = f.createTable('/','meta',{'high_key': tables.IntCol(8),'max_time':tables.FloatCol()},filters=filters.copy())
	meta.append([(0,0)]) # give an initial value

	if close:
		f.close() # and close the file, we do not exchange open handles here
		return True
	else:
		return f
	

def h5slice(file,variables,begin,end=False,indices=False):
	# open the file for reading
	"""
		variables is a simple string list of the variables wished
		indices are same-shape time indipendent data, of which only one 'ob' is pulled
	"""
	f = h5openr(file)
	if not end:
		end = f.root.meta[0]['max_time'] # then the max of the file is the end
	index = f.root.time.readWhere('(time >= '+str(begin)+')&(time <= '+str(end)+')')
	# and then sort the values
	timekeys = zip(index['time'],index['key'])
	timekeys.sort()#sort by time
	times,keys = zip(*timekeys)
	x = max(keys)+1
	n = min(keys)
	out = {}# return a dict keyed like the input
	# slice the data from the file, and then sort it
	out['time'] = np.array(times) # return times with the data
	for v in variables:
		out[v] = np.array(f.root[v][n:x])[keys - n]
	# now read out indices
	for i in indices:
		out[i] = np.array(f.root[i][0]) # I only grab the first value for such a value
		# note, it is your job to keep track of which variable is an index.
	
	f.close()
	return out





def h5append(f, time, persistent=False, **data)
	# add the specified dictionary of data to the file
	# appends only a single row to the elastic arrays! Plus the metadata arrays
	"""
		inputs
		f = file name of hdf file to write to
		time = unix timestamp of observation
		persistent = should file be treated as already open tables object
		**data = a dict of name:numpyarray s of data

		note, i do not check that you are appending to every array, so
		if you dont, your indices will get all mucked up, be warned
		-- this does mean you can contain variables which are not actually functios of time
			like height, x, y, etc. you must specify these as indices for readout purposes
	"""
	if not persistent:
		f = opena(f)
	# presumably f is a tables object now
	# determine high key
	try:
 		i = f.root.meta[0]['high_key'] # get the current maximum key
	except:
		i = 0 # empty array
	f.root.time.append([(time,i)])
	i+=1 # yes, we do this before appending max keys
	m = f.root.meta
	for row in m: #there is only one
		row['high_key'] = i
		if time > row['max_time']:
			row['max_time'] = time
		row.update()
	# now loop through the given variables
	for v in data:
		memory.root[v].append(data[v])
	# ok, the deed is done
	if not persistent:
		f.close()








"These functions can have the lockout functionality applied to them later"
def h5openr(f):
	# open the file f for reading, but check if it is open.. nevermind, forget safety
	#DANGEROUS
	f = tables.openFile(f,mode='r')
	return f

def h5opena(f):
	# open the file f for appending
	#DANGEROUS
	f = tables.openFile(f,mode='a')
	return f

def h5openw(f):
	#this will destroy whatever file it is opening, note
	f = tables.openFile(f,mode='w', title='ms') # have to give it a title
	return f
