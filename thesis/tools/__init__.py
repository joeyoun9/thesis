"""
Tools for checking times and whatont
"""
import calendar,time
from datetime import timedelta,datetime
import numpy as np

def s2t(string,time_format):
	return calendar.timegm(time.strptime(string,time_format))
	# better specify UTC if you want to make sure it makes the right choice!!!

def m2t(t):
	"""
		create a unix time from a matlab ordinal time
	"""
	print t
	dt = datetime.fromordinal(int(t))+timedelta(days=t%1) - timedelta(days=366) 
	# well, that's close...
	return calendar.timegm(dt.timetuple()) #woohoo?



def mean2d(dat,binsize):
	# this will compute a ceilometer style mean along the first axis -- WARNING - USES A FOR LOOP	
	# for every binsize number of rows, produce a single average
	"""
		the first index should be time, and the second height, we will average by taking chunks in time
		and averaging
	"""
	out = np.zeros((int(dat.shape[0]/binsize),dat.shape[1])) #initialize
	chunk = dat[0:binsize]
	i=0 # index
	while True:
		try:
			out[i] = np.mean(chunk,axis=0)
			i+=1
			chunk = dat[i*binsize:(i+1)*binsize]
		except:
			break

	# we could convolve as well, but that is just not as nice! (and not much faster either)
	return out

"""
#CONVOLUTION MEAN COMPUTATION
# use convolution to make a running mean!
w = 20.
weights = np.zeros(w)+1#np.repeat(0,w)/w
dat2 = np.zeros(dat[:,:-(w-1)].shape)
print dat2.shape,dat.shape
for i in range(len(dat)):
        # have to loop through rows to average, not too terrible
        print 'row',i
        dat2[i] = np.convolve(dat[i],weights)[w-1:-(w-1)]
"""


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
