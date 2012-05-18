"""
Tools for checking times and whatont
"""
import tables
import numpy as np

class h5(object):
	def __init__(self,fname):
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
			
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		if not end:
			end = self.doc.getNode(group).meta[0]['max_time'] # then the max of the file is the end
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
			for v in variables:
				out[v] = self.doc.getNode(group,name=v)[n:x][keys - n]
		# now read out indices
		for i in indices:
			out[i] = self.doc.getNode(group,name=i) # indices should only have one value in time dimension
			#FIXME - converting to a numpy array can take a lot of time - give it a flavor?
			# note, it is your job to keep track of which variable is an index.
		
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
		try:
 			i = self.doc.getNodeAttr(group,'maxkey')+1#root.meta[0]['high_key'] # get the current maximum key
		except:
			i = 0 # empty array, though above should always work...
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


	def dump(self,variable):
		"""
			simply output the entire contents of a specific variable, for all times
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		out = self.doc.getNode('/',name=variable)[:]
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
