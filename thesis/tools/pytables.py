"""
Tools for checking times and whatont
"""
import tables
import numpy as np

class h5(object):
	'''
	Initialize the object which is used to interact with an HDF5 archive created for my thesis
	'''
	def __init__(self,fname):
		"""
		Create the object for interaction by simply providing the location of the 
		HDF5 document
		
		Inputs:
			fname = source file (.h5,hdf5,etc...)
		"""
		# it does have to be initialized, sadly, but otherwise it is good to go
		self.filename = fname # this is mandatory!!!
		self.doc = False
	def create(self, close=True,indices=False, group='/', **variables):
		# create an hdf5 table for use with datasets, ideally of known size...
		# variables specifies what variables will be filled in this archive
		"""
			Inputs:
			close:       - boolean to tell if the file should be returned or closed
			indexes:     - A dict of {'name':[length(integer),]} valuse to save as single valued indices (Carrays)
			group:       - The textual representation of the group that the data should be created in...
			**variables  - dict of {'name':[length(integer),]} values to tell the variables
		"""
		#FIXME  - only one category available.
		if not self.doc:
			# if the doc has been opened before, then reopen it for appending.
			self.doc = h5openw(self.filename)
		elif not self.doc.isopen:
			self.doc = h5opena(self.filename)


		# get group parts
		# you can only create a group once
		if group  is not '/':
			#FIXME - if the group ends in '/', then we may have a problem, but at the same time, it ought to end in that!!
			gp = group.split('/')
			# then create the group ... hopefully this works!!
			drop = '/'.join(gp[:-1])+'/' # join up to the entire length minus one!
			self.doc.createGroup(drop,name=gp[-1])



		filters =  tables.Filters(complevel=6, complib='zlib')#blosc
		for k in variables:
			# create the variable called k, with length variables[k]
			# allow for multi-dimensional data
			dims = (0,)
			if type(variables[k]) == tuple:
				# then this is multidimensional
				for i in variables[k]: #it had better be a list
					dims = dims + (i,)
			else:
				dims = (0,variables[k])#hmm
			self.doc.createEArray(group,k,tables.Float32Atom(),dims,filters=filters.copy())	
		""" 
			Create metadata and indexing tables
		"""
		if indices:
			for k in indices:
				if type(indices[k]) == tuple:
					dims = ()
					for i in indices[k]:
						# loop through the specified values
						dims = dims + (i,)
				else:
					dims = (indices[k],)
				# create a static aray.
				self.doc.createCArray(group,k,tables.Float32Atom(),dims,filters=filters.copy())


		# the time table is a permenant feature
		time_desc = {'time': tables.FloatCol(pos=1),
			'key':tables.IntCol(8,pos=2),
		}
		time = self.doc.createTable(group,'time',time_desc,filters=filters.copy())

		# add a file attribute regarding the creation type/ownership? (This will just restate if file is not new)		
		self.doc.setNodeAttr('/','creator', 'Joe Young\'s Thesis HDF5')
		self.doc.setNodeAttr('/','version', '1.02')
		self.doc.setNodeAttr(group,'maxtime',0) # metadata?
		self.doc.setNodeAttr(group,'maxkey',-1) # metadata information - start at -1 so that maxkey +1 initially = 0
		
	
		if close:
			self.doc.close() # and close the file, we do not exchange open handles here
		return True




	def slice(self,variables,begin=False,end=False,duration=False,timetup=False,indices=False,group='/'):
		# open the file for reading
		"""
			variables is a simple string list of the variables wished
			indices are same-shape time indipendent data, of which only one 'ob' is pulled
			duration in seconds
			
			There are various methods for specifying times, of which at least one must be given
			
			time tuples are ideal right now...
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		# ok, well, now figure out what time period they wanted
		if timetup:
			begin = timetup[0]
			end = timetup[1]
		elif duration and not end and not begin:
			# then 
			end = self.doc.getNodeAttr(group,'maxtime')
			begin = end - duration # duration is in seconds?
		elif duration and begin:
			end = begin + duration
		elif duration and end:
			begin = end - duration
		# if it is begin and end, then those are just set nicely
		elif not duration and not begin and not end:
			# you gave me nothing
			raise Exception('You must specify a begin/end, a duration or a time tuple in order to slice. Use dump() so see an entire dataset') 

		index = self.doc.getNode(group).time.readWhere('(time >= '+str(begin)+')&(time <= '+str(end)+')')
		# and then sort the values
		out = {}# return a dict keyed like the input
		if len(index) > 0:
			timekeys = zip(index['time'],index['key'])
			timekeys.sort()#sort by time
			times,keys = zip(*timekeys)
			x = max(keys)+1
			n = min(keys)
			# create an numpy slice object.
			# slice the data from the file, and then sort it
			out['time'] = np.array(times) # return times with the data
			"""
			enable variables to be a string or list
			"""
			if not type(variables) == list:
				variables = [variables]
			for v in variables:
				out[v] = self.doc.getNode(group,name=v)[n:x][keys - n] #FIXME!!! DO YOU WORK>!>!>!>!>!>!
		else:
			"""
			the timestring requested was out of the time domain of the dataset, so no data was recovered
			"""
			self.doc.close()
			raise Exception('This dateset does not have any data within the times specified')
		# now read out indices
		if indices:
			for i in indices:
				out[i] = self.doc.getNode(group,name=i)[:] # indices should only have one value in time dimension
				#FIXME - converting to a numpy array can take a lot of time - give it a flavor?
				# note, it is [currently] your job to keep track of which variable is an index.
		
		self.doc.close()
		return out


	def loadIndices(self,group='/', **indices):
		# simply stick the values of indices into their places
		if not self.doc or not self.doc.isopen:
			self.doc = h5opena(self.filename)

		for i in indices:
			self.doc.getNode(group,name=i)[:] = indices[i] # that is all!

		self.close()


	def append(self, time, persist=False, group='/', **data):
		# add the specified dictionary of data to the file
		# appends only a single row to the elastic arrays! Plus the metadata arrays
		"""
			inputs
			time = unix timestamp of observation
			persistent = should file be treated as already open tables object
			**data = a dict of name:numpyarray s of data
	
			note, i do not check that you are appending to every array, so
			if you dont, your indices will get all mucked up, be warned
			-- this does mean you can contain variables which are not actually functios of time
				like height, x, y, etc. you must specify these as indices for readout purposes
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5opena(self.filename)# open for appending
		# presumably f is a tables object now
		# determine high key
 		i = self.doc.getNodeAttr(group,'maxkey') + 1

		# Add this information to the keys table
		self.doc.getNode(group,name='time').append([(time,i)])
		
		if time > self.doc.getNodeAttr(group,'maxtime'):
			self.doc.setNodeAttr(group,'maxtime',time)
		self.doc.setNodeAttr(group,'maxkey',i)

		i+=1 # Wait until after the maxkey is set.

		# now loop through the given variables
		for v in data:
			#print 'writing',v
			self.doc.getNode(group,name=v).append([data[v]])#brackets = reshape, must be array appended.

		# ok, the deed is done
		if not persist:
			self.doc.close()

		return True


	def dump(self,variable,group='/'):
		"""
			simply output the entire contents of a specific variable, for all times
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		out = self.doc.getNode(group,name=variable)[:]
		self.close()
		return out

	def close(self):
		if self.doc.isopen:
			self.doc.close()






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
