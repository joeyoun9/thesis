"""
Tools for checking times and whatont
"""
import calendar,time
from datetime import timedelta,datetime
import numpy as np
import thesis # ensure thesisverbose is accessible

all = ['bundle','figure','map','metcalcs','pytables','sounding']

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
   
def mean2d(dat,dim,binsize):
	'''
	compute a chunk/bin style mean along the first axis, with dimension key of the same size
	'''
	# this will compute a ceilometer style mean along the first axis -- WARNING - USES A FOR LOOP	
	# for every binsize number of rows, produce a single average
	"""
		the first index should be time, and the second height, we will average by taking chunks in time
		and averaging
		
		THIS MEANS THAT THERE IS NO TRANSPOSE OPERATIONS NEEDED FOR COMPUTATION
	"""
	datO = np.zeros((int(dat.shape[0]/binsize),dat.shape[1])) #initialize
	dimO = 
	chunk = dat[0:binsize]
	dimx = dim[0:binsize]
	i=0 # index
	while True:
		try:
			datO[i] = np.mean(chunk,axis=0) 
			dimO[i] = np.mean(dimc)
			i+=1
			#take a chunk of 'profiles' in 'time' ( ||| ||| ||| = 3 chunks)
			chunk = dat[i*binsize:(i+1)*binsize]
			dimc = dat[i*binsize:(i+1)*binsize]
		except:
			break

	# we could convolve as well, but that is just not as nice! (and not much faster either)
	return datO,dimO

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
		
def runmean2d(dat,dim1,dim2,bin1,bin2):
    '''
    compute the running mean for a field with dimensions 1 and 2,
    and return the field, along with the new dimensions, in the original structure
    which woud be shape = (dim1.shape,dim2.shape)
    
    For time/height this ought to be written as dim1=height, dim2=time
    '''
    if not dat.shape == (dim1.shape[0],dim2.shape[0]):
        print 'Your dimensions are incorrect.'
    dat,dim1 = runmean(dat.T,dim1,bin1)
    dat,dim2 = runmean(dat.T,dim2,bin2)
    return dat,dim1,dim2        

def runmean(dat,dim,binsize):
    '''    
    Create a running mean the same shape as dat. Binsize must be even!!
    
    Parameters
    ----------
    dat : numpy array
        Two dimensional gridded dataset, will be averaged in binsize running bins in
        the first dimension
    binsize : int
        Full width of the window used for averaging. (binsize/2 values on either end)
        
    '''
    if not binsize%2 == 0:
        binsize +=1
    weights = np.repeat(1.0,binsize)/binsize
    dat_out = np.zeros(dat[:,:-(binsize-1)].shape)
    for i in range(len(dat)):
        ' average row by row, to maintain data shape, as convolve is 1 dimensional' 
        dat_out[i] = np.convolve(dat[i],weights)[binsize-1:1-(binsize)]
    'provide the user the time values, since there is an unfortunate shape change.'
    dim = dim[binsize/2:1-binsize/2]
    'this interpretation may not be completely valid...'
    return (dat_out,dim)


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

def timemean(dat,time,dt,verbose=False):
	'''
	move data into time-oriented bins, returning the binned average of multi-dimensional data
	
	
	Parameters
	----------
	
	dat: numpy array
		the data to be averaged into bins, first dimension should correspond to time length
		
		etc...
	'''
	if dt == 0:
		'do nothing, the function was just invariably wrapped into something'
		return dat,time
	begin = np.min(time)
	end = np.max(time)
	length = np.floor((end-begin)/dt) + 1
	outT=np.zeros(length)
	outshape = [length]+list(dat.shape[1:])
	if verbose:
		print outshape
	outD = np.zeros(outshape)
	binlow = begin
	i=-1
	while True:
		binhigh = binlow+dt
		i+=1
		outT[i]=binlow + dt/2
		'... do the processing'
		q = dat[(time<binhigh)&(time>=binlow)]
		if len(q) > 0:
			res = np.mean(q,axis=0)
		else:
			'WARNING This will not work for 2-d+ datasets!!! AHHH!!'
			res = np.nan
		outD[i] = res
		binlow=binhigh
		if binhigh > end:
			break 
	return outD,outT

def timebin(dat,time,dt,verbose=False):
	'''
	A replacemaent for the name timebin, to preserve intercompatibility.
	'''
	return timemean(dat,time,dt,verbose)

def timestd(dat,time,dt,verbose=False):
	'''
	Compute time-oriented standard deviations, instead of means for any particular bin.
	This allows computation of standard deviations on a time-binned basis.
	
	Parameters
	----------
	
	dat: numpy array
		the data to be averaged into bins, first dimension should correspond to time length
		
		etc...
	'''
	if dt == 0:
		'do nothing, the function was just invariably wrapped into something'
		return dat,time
	begin = np.min(time)
	end = np.max(time)
	length = np.floor((end-begin)/dt) + 1
	outT=np.zeros(length)
	outshape = [length]+list(dat.shape[1:])
	if verbose:
		print outshape
	outD = np.zeros(outshape)
	binlow = begin
	i=-1
	while True:
		binhigh = binlow+dt
		i+=1
		outT[i]=binlow + dt/2
		'... do the processing'
		q = dat[(time<binhigh)&(time>=binlow)]
		if len(q) > 0:
			res = np.std(q,axis=0)
		else:
			'WARNING This will not work for 2-d+ datasets!!! AHHH!!'
			res = np.nan
		outD[i] = res
		binlow=binhigh
		if binhigh > end:
			break 
	return outD,outT

def comp2time(*timetup):
    '''
    convert darn numbers to useful dates.
    ASSUMES THE GIVEN DATE IS IN UTC
    makes a tuple: yr,mn,day,hr,mn,sec, 0 0 0
    Can be made iterable. 
    '''
    while len(timetup) < 9:
        timetup = np.append(timetup,[0])
    return calendar.timegm(timetup)
     

	
		
	
