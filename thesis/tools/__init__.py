"""
Tools for checking times and whatont
"""
import calendar,time
from datetime import timedelta,datetime
import numpy as np
import thesis # ensure thesisverbose is accessible

def s2t(string,time_format):
	'''
	Convert a textual string time representation to a unix epoch time using the standard time format string
	provided. Identical to
	
		>>> calendar.timegm(time.strptime(string,time_format) 
		
	Parameters
	----------
	string: str
		a time stamp of whatever format, as long as it is information that can be interpreted by the 
		time.strptime() function
		
	
	
	Note
	----
	Specify UTC in the string, and %Z in the format to ensure the data is properly 
	interpreted as UTC/GMT
	'''
	return calendar.timegm(time.strptime(string,time_format))

def m2t(t):
	"""
		create a unix time from a matlab ordinal time
	"""
	dt = datetime.fromordinal(int(t))+timedelta(days=t%1) - timedelta(days=366) 
	# well, that's close...
	return calendar.timegm(dt.timetuple()) #woohoo?

def strz(n,z=2):
    '''
    convert a number to a string with the proper number of leading zeros
    '''
    return str(n).zfill(z)
    

def mean2d(dat,binsize):
	# this will compute a ceilometer style mean along the first axis -- WARNING - USES A FOR LOOP	
	# for every binsize number of rows, produce a single average
	"""
		the first index should be time, and the second height, we will average by taking chunks in time
		and averaging
		
		THIS MEANS THAT THERE IS NO TRANSPOSE OPERATIONS NEEDED FOR COMPUTATION
	"""
	out = np.zeros((int(dat.shape[0]/binsize),dat.shape[1])) #initialize
	chunk = dat[0:binsize]
	i=0 # index
	while True:
		try:
			out[i] = np.mean(chunk,axis=0) 
			i+=1
			#take a chunk of 'profiles' in 'time' ( ||| ||| ||| = 3 chunks)
			chunk = dat[i*binsize:(i+1)*binsize]
		except:
			break

	# we could convolve as well, but that is just not as nice! (and not much faster either)
	return out

def mean1d(dat,binsize):
	"""
	an equivalent method for single dimension averaging (such as getting equivalent times)
	"""
	out = np.zeros(int(dat.shape[0]/binsize))#one dimensional only!!
	chunk = dat[0:binsize]
	i=0 # index
	while True:
		try:
			out[i] = np.mean(chunk,axis=0)# axis does not have to be specified
			i+=1
			#take a chunk of 'profiles' in 'time' ( ||| ||| ||| = 3 chunks)
			chunk = dat[i*binsize:(i+1)*binsize]
		except:
			break
	return out
	
	
def runmean(dat,binsize):
	'''
	Deprecated.
	
	Create a running mean the same shape as dat.
	
	Parameters
	----------
	dat : numpy array
		Two dimensional gridded dataset, will be averaged in binsize running bins in
		the first dimension
	binsize : int
		Full width of the window used for averaging. (binsize/2 values on either end)
		
		
	'''
	#global thesisverbose
	weights = np.repeat(1.0,binsize)/binsize
	dat2 = np.zeros(dat[:,:-(binsize-1)].shape)
	for i in range(len(dat)):
		# average row by row, to maintain data shape, as convolve is 1 dimensional
	#	if thesisverbose:
		dat2[i] = np.convolve(dat[i],weights)[binsize-1:-(binsize-1)]
		#print 'row',i,dat2[i],weights

	return dat2


def stdev2d(dat,binsize):
	out = np.zeros((int(dat.shape[0]/binsize),dat.shape[1])) #initialize, if it is in the wrong order, that will be quickly apparent.
	chunk = dat[0:binsize]
	i=0 # index
	while True:
		try:
			out[i] = np.std(chunk,axis=0)
			i+=1
			chunk = dat[i*binsize:(i+1)*binsize]
		except:
			break
	return out	

def timebin(dat,time,dt):
	'''
	move data into time-oriented bins, returning the binned average of multi-dimensional data
	
	This is fairly slow.
	
	Parameters
	----------
	
	dat: numpy array
		the data to be averaged into bins, first dimension should correspond to time length
		
		etc...
	'''
	begin = np.min(time)
	end = np.max(time)
	length = np.floor((end-begin)/dt) + 1
	outT=np.zeros(length)
	outshape = [length]+list(dat.shape[1:])
	print outshape
	outD = np.zeros(outshape)
	binlow = begin
	i=-1
	while True:
		binhigh = binlow+dt
		i+=1
		outT[i]=binlow + dt/2
		'... do the processing'

		outD[i] = np.mean(dat[(time<binhigh)&(time>=binlow)],axis=1)
		binlow=binhigh
		if binhigh > end:
			break 
	return outD,outT
		
	
