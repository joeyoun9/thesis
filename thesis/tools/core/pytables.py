"""
Class wrappers for thesis formatted HDF5 documents, for both saving and acquiring data
from these files.

This entire operation is deprecated, and shall only be used on thesis-format
documents. But no more. There is another, and it is superior.
"""
import tables
import numpy as np
from objects import CoreObject


class h5(object):
	'''
	Class for interacting with HDF5 files in the format created by this class
	'''

	def __init__(self, fname):
		"""
		Create the object for interaction by simply providing the location of the 
		HDF5 document
		
		Parameters
		----------	
		fname : str
			String location of HDF5 source file (.h5,hdf5,etc...)
			
		"""
		self.filename = fname
		self.doc = False

	def create(self, close=True, indices=False, group='/', **variables):
		# create an hdf5 table for use with datasets, ideally of known size...
		# variables specifies what variables will be filled in this archive
		"""
		Create 
		
		Parameters
		----------
			close : bool
				tell if the file should be returned or closed
			indexes : dict
				A dict of {'name':[length(integer),]} values to save as single valued indices (Carrays)
			group: str,opt
				The textual representation of the group the dataset will reside in
			**variables:
				name=[length,length,...] values to state the expandable variables for the dataset
		"""
		# FIXME  - only one category available.
		if not self.doc:
			# if the doc has been opened before, then reopen it for appending.
			self.doc = h5openw(self.filename)
		elif not self.doc.isopen:
			self.doc = h5opena(self.filename)

		if group  is not '/':
			# FIXME - if the group ends in '/', then we may have a problem, but at the same time, it ought to end in that!!
			gp = group.split('/')
			# then create the group
			drop = '/'.join(gp[:-1]) + '/'
			self.doc.createGroup(drop, name=gp[-1])

		filters = tables.Filters(complevel=6, complib='zlib')  # blosc
		for k in variables:
			# create the variable called k, with length variables[k]
			dims = (0,)
			if type(variables[k]) == tuple:
				# then this is multidimensional
				for i in variables[k]:  # it had better be a list
					dims = dims + (i,)
			else:
				dims = (0, variables[k])  # hmm
			self.doc.createEArray(group, k, tables.Float32Atom(), dims, filters=filters.copy())

		if indices:
			for k in indices:
				if type(indices[k]) == tuple:
					dims = ()
					for i in indices[k]:
						dims = dims + (i,)
				else:
					dims = (indices[k],)

				self.doc.createCArray(group, k, tables.Float32Atom(), dims, filters=filters.copy())


		# the time table is a permenant feature
		time_desc = {'time': tables.FloatCol(pos=1),
			'key':tables.IntCol(8, pos=2),
		}
		time = self.doc.createTable(group, 'time', time_desc, filters=filters.copy())
		del time_desc
		# file attributes
		self.doc.setNodeAttr('/', 'creator', 'Joe Young\'s Thesis HDF5')
		self.doc.setNodeAttr('/', 'version', '1.1')
		# and group attributes
		self.doc.setNodeAttr(group, 'maxtime', 0)  # metadata?
		self.doc.setNodeAttr(group, 'maxkey', -1)  # metadata information - start at -1 so that maxkey +1 initially = 0


		if close:
			self.doc.close()  # and close the file, we do not exchange open handles here
		return True


	def listNodes(self):
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		nodes = self.doc.listNodes()
		self.close()
		return nodes


	def slice(self, variables, begin=False, end=False, duration=False,
			timetup=False, indices=False, group='/', persist=False):
		"""
		Read a specific temporal subset of various variables, as well as fetch indices
		
		Parameters
		----------
		variables: list
			a list of strings indicating all the variables which should be read.
		timetup: tuple
			Tuple of (begin,end) epoch timestamps which specify the begin/end times of the slice.
		begin: int, opt
			epoch time stamp to begin. If only given, then dataset will be read to the end.
		end: int, opt
			epoch time of slice end. If no other value given dataset is read from beginning 
			to this specified point.
		duration: int, opt
			Number of seconds to observe relative to either END of dataset, or one of the provided
			begin/end values (begin takes priority).
		indices: list, opt
			indices are same-shape time independent data, of which only one 'ob' is pulled
			duration in seconds
		group: str/group, opt
			specify the HDF5 group where this dataset exists.
		persist" bool, opt
			should the HDF document be closed after each iteration? If true the
			obj.close() method will have to be called at the end of the process
			
		Returns
		-------
		out: dict
			a dictionary keyed by the variables and indices given, their values are numpy arrays
			corresponding to the time sliced and ordered datasets requested.
			
		Note
		----
		If no time information (timetuple,begin,etc.) is given, the entire dataset will be returned,
		similar to a multivariable dump.
		
		Time is ALWAYS returned as an index on the output variable from a slice operation
		
		See Also
		--------
		index : grab only dataset indices.
		dump : fetch data independent of time.
		
		
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		# determine the time boundaries, timetups can be lists too now.
		if not type(timetup) == bool:
			begin = timetup[0]
			end = timetup[-1]
		elif duration and not end and not begin:
			# then
			end = self.doc.getNodeAttr(group, 'maxtime')
			begin = end - duration  # duration is in seconds?
		elif duration and begin:
			end = begin + duration
		elif duration and end:
			begin = end - duration
		elif not duration and not begin and not end:
			# you gave me nothing
			raise Exception('You must specify a time tuple (timetup), begin/end or a duration in order to slice. Use dump() so see an entire dataset')

		index = self.doc.getNode(group).time.readWhere('(time >= ' + str(begin) + ')&(time <= ' + str(end) + ')')

		out = CoreObject()
		if len(index) > 0:
			timekeys = zip(index['time'], index['key'])
			timekeys.sort()
			times, keys = zip(*timekeys)
			x = max(keys) + 1
			n = min(keys)
			out['time'] = np.array(times)

			if not type(variables) == list:
				variables = [variables]
			for v in variables:
				out[v] = self.doc.getNode(group, name=v)[n:x][keys - n]  # FIXME!!! DO YOU WORK>!>!>!>!>!>!
		else:
			self.doc.close()
			raise Exception('This dataset does not have any data within the times specified')
		if indices:
			for i in indices:
				out[i] = self.doc.getNode(group, name=i)[0]
				# indices should only have one value in time dimension
				# note, it is [currently] your job to keep track of which variable is an index.
		if not persist:
			self.doc.close()
		return out

	def index(self, index, group='/'):
		"""
		Read out the entire value of the specified data indexing value. 
		No searching is performed
		
		Parameters
		----------
		index: str
			string representation of the index name.
		group: str/group, opt
			string representation of the group where the indices are read from.
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		return self.doc.getNode(group, name=index)[0]
		# take the first value ([0]) because indices are time invariant in that dimension

	def loadIndices(self, group='/', **indices):
		"""
		Insert index variable arrays into the document
		
		Parameters
		----------
		group: str, opt
			Specify the group in the file where the data are read from
		**indices:
			name=value pairs of the values to assign (and create) the indices for 
			any specific dataset.
		
		"""
		# simply stick the values of indices into their places
		if not self.doc or not self.doc.isopen:
			self.doc = h5opena(self.filename)

		for i in indices:
			self.doc.getNode(group, name=i)[:] = indices[i]  # that is all!

		self.close()


	def append(self, time, persist=False, group='/', **data):
		"""
		Adds a single entry for multiple variables as well as updates the
		metadata attributes for the referred group. Appends only one row at a time
		
		
		Parameters
		----------
		time: int
			Unix timestamp of entry
		persist: bool
			set to true for the file to be left open between append rounds,
			this is recommended, as it will be much easier on the filesystem, and faster.
		group: str,group Object
			textual or objective reference to the group branch where the 
			variable array is located
		**data: 
			keyword arguments of variable=value
	
	
		Note
		----
		This does not check that you are appending to every array, so
		if you don't, your indices will get all mucked up, be warned
		-- this does mean you can contain variables which are not actually functions of time
		like height, x, y, etc. you must specify these as indices for readout purposes
		
		"""

		if not self.doc or not self.doc.isopen:
			self.doc = h5opena(self.filename)

		# determine high key
 		i = self.doc.getNodeAttr(group, 'maxkey') + 1

		# Add this information to the keys table
		self.doc.getNode(group, name='time').append([(time, i)])

		if time > self.doc.getNodeAttr(group, 'maxtime'):
			self.doc.setNodeAttr(group, 'maxtime', time)
		self.doc.setNodeAttr(group, 'maxkey', i)

		i += 1  # Wait until after the maxkey is set.

		# now loop through the given variables
		for v in data:
			# print 'writing',v
			self.doc.getNode(group, name=v).append([data[v]])  # brackets = reshape, must be array appended.
		if not persist:
			self.doc.close()
		return True


	def dump(self, variable, group='/'):
		"""
		A method to quickly output the entire contents of any specific variable/index
		array. 
			
		Warning
		-------
		This does not currently make any checks for dataset size, so if you dump too large
		a dataset, a significant amount of memory can be used accidentally
			
		Parameters
		----------
		variable: str
			The variable or index array to be output.
		group: str/group, opt
			The group the dataset is stored in.
		"""
		if not self.doc or not self.doc.isopen:
			self.doc = h5openr(self.filename)
		out = self.doc.getNode(group, name=variable)[:]
		self.close()
		return out

	def close(self):
		if self.doc.isopen:
			self.doc.close()






def h5openr(f):
	f = tables.openFile(f, mode='r')
	return f

def h5opena(f):

	f = tables.openFile(f, mode='a')
	return f

def h5openw(f):
	f = tables.openFile(f, mode='w', title='ms')  # have to give it a title
	return f
