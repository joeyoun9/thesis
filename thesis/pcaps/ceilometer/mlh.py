'''
A module to assist in the analysis of ceilometer boundary layers

methods posess an about keyword argument, which when passed, will return
a 3-character boolean string which indicates:
[0] is there time binning used
[1] is a threshold required?
[2] undefined

'''
import numpy as np
from thesis.tools import *

def threshold(data, threshold = -7.6, cloud=-5, returnfield=False, binsize=0,
               inTime=True, continuous=False, vertbin=20, **kwargs):
    '''
    for a formatted backsctter dataset, determine a timeseries of the lowest incidence
    of the specified backscatter value, regardless of mathematical base.
    
    Parameters
    ----------
    threshold: float, optional
        specify the cutoff value for the threshold to be determined from the bottom up
        
    data: numpy 2-d array
        the dataset from which the thresholds are determined 
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '010Threshold'
    if binsize == 0:
        'no binning or averaging or whatnot is to be done.'
        z = data['height']
        t = data['time']
        data = data['bs']
    else:
        data,t,z = _ComputeFieldMeans(data,binsize,inTime=inTime,continuous=continuous,vertbin=vertbin)
    if returnfield:
        return (data,z,t)
    depth = _ThresholdLT(data,z,threshold,range=1200)
    return (depth,t)

def gradient(data, window=20, cloud=-5,limit=1000, binsize=300, inTime=True,
             continuous=False, multiple=False, returnfield=False,
             eval_distance=20, vertbin=20, 
            **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    '''
    if data =='about':
        return '110Gradient'
    bs,times,z = _ComputeFieldMeans(data,binsize,inTime=inTime,
                                    continuous=continuous,vertbin=vertbin,
                                    power=True)
    field = np.gradient(bs,eval_distance)[1]
    field[field>=0.]=np.nan 
    'this line, though it is undone in 3 lines, is to protect log10'
    field = np.log10(-1*field)
    if returnfield:
        field[np.isnan(field)]=np.nanmin(field)
        return (field,times,z)
    
    '///////////////////  DETERMINISTIC SECTION  /////////////////////////////'
    if not multiple:
        depth = _MaxDepth(field,z,range=limit)
    else:
        '''
        Multiple levels should be returned, with the 
        '''
        depth = _LocalMaxDepths(field,z,window,4,range=limit)
    return (depth,times)

def gradient2(data, limit=1000, binsize=300, inTime=True, eval_dist=20,
              continuous=False,returnfield=False, vertbin=20, **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)

    Known as the inflection point method (IPM)
    
    note, if inTime is false, a time value is still required!!!
    '''
    if data =='about':
        return '1102nd Gradient'
    bs,times,z = _ComputeFieldMeans(data,binsize,inTime=inTime,
                                    continuous=continuous,vertbin=vertbin,
                                    power=True)
    'Compute the gradient of the gradient'
    'FIXME - do i want negative or positive gradients!?!!'
    data = np.gradient(np.gradient(bs,eval_dist)[1],eval_dist)[1]
    data[data>=0.] = np.NAN
    data = np.log10(-1*data)
    if returnfield:
        data[np.isnan(data)]=np.nanmin(data)
        return (data,times,z)
    'this should be detailed as the most negative second gradient'
    depth = _MaxDepth(data,z,range=limit)
    return (depth,times)

def variance(data, binsize=300, limit=1000, inTime=True, returnfield=False,
             continuous=False, power=False, vertbin=20, nbins=4, **kwargs):
    '''
    the evaluation of boundary layer height using the assumption that variance
    is highest at the top of the boundary layer
    
    If you do this one continuously, you're gonna have a bad time.
    '''
    if data =='about':
        return '110Variance'
    data,time,height = _ComputeFieldMeans(data,binsize/nbins,inTime=inTime,
                                          continuous=continuous,vertbin=vertbin,
                                          power=power)
    if inTime:
        data,time = timestd(data,time,nbins)
    else:
        data,time = stdev2d(data,time,nbins)

    if returnfield:
        return (data,time,height)
    depth = _MaxDepth(data,height,range=limit)
    return (depth,time)
    
def noise_variance(data, threshold=0.4, limit=1000, binsize=300, inTime=True, returnfield=False, **kwargs):
    '''
    use standard deviation calculations to determine the top of the layer
    under the theory that robust returns come from particle presence, and 
    noise is harder to filter where there is low return.
    
    Note, this method does not perform any averaging, and cannot be done continuously
    
    Parameters
    ----------
    value: float
        the stdev value to seek in the dataset, recommend around .5 to .7
    data: 3-D numpy array
        the type returned from a slice request on an hdf5, with keys for 
        'bs', 'time' and 'height'.
    binsize: int, optional
        the size of bins to create the calculations from, default to 20
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '110Noise Variance'
    if not threshold:
        raise ValueError, 'You must specify a threshold value'
    time = data['time']
    'bla bla not preserving namespace bla bla bla...'
    height = data['height']
    if inTime:
        data,time = timestd(data['bs'],time,binsize)
    else:
        data,time = stdev2d(data['bs'],time,binsize)
    if returnfield:
        return (data,time,height)
    depth = _ThresholdGT(data,height,threshold,range=limit)       
    'and return a tuple'
    return (depth,time)

def idealized(data, binsize=300, returnfield=False, inTime=True, savebin=False,

              continuous=False, vertbin=5, **kwargs):
    '''
    Use the idealized backscatter method to identify the top of the aerosol layer.
    
    This routine will use the -7.6 threshold method as a first guess, and will then minimize
    the defined function to determine the function coefficients 
    
    Parameters
    ----------
    
    data: list
        The produced output from the slice for ceilometer data for the time period analyzed
    binsize: int, optional
        the length in SECONDS for bins to be produced. Longer bins increase the chance of success
    returnfield: bool, optional
        return only the field analyzed, not very useful for this operation.
    inTime: bool, optional
        specify if the provided time dimension is actually epoch time stamps, or just bin numbers
    savebin: str, optional
        only save a demonstrative figure of a single bin. A possibly useful demonstration
        operation. 
   
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '100Idealized Profile'
    from scipy import optimize,special
    bs,times,z=_ComputeFieldMeans(data,binsize,inTime=inTime,continuous=continuous,vertbin=vertbin)
    'no, this method will not use power'
    if returnfield:
        return (bs,times,z)
    
    first_guesses,times = threshold({'bs':bs,'height':z,'time':times}) 
    'compute the low-level means from the 5th ob up to the guess height'
    guess_mean = lambda x:np.mean(bs[x][z<=first_guesses[x]])
    first_guess_mean = np.array(map(guess_mean,range(len(first_guesses))))
    'now, for each time bin, we will run the optimization'
    outH = np.zeros(len(times))
    outdH = np.zeros(len(times))
    for i in range(len(times)):
        '''
        make first guesses and fix the two variables
        '''
        b = bs[i] # the backscatter profile
        h = first_guesses[i] # first guess height (a very good guess)]
        dh = 100. # guess value of dh, based on observation
        'for now we are always assuming a 100m transition layer until told otherwise'
        p0 = [h,dh]
        if h == 0: continue
        bm = first_guess_mean[i] # approximation for boundary layer intensity, assumed valid
        bu = -8.2 #this is a gross approximation, and will lead to errors...
        'There are two coefficients, A1 and A2, and one is fixed for the fitting'
        a1 = (bm+bu)/2.
        a2 = (bm-bu)/2.
        fitfunc = lambda p, x: a1-a2*special.erf((x-p[0])/p[1])
        errfunc = lambda p, x, y: np.sum((fitfunc(p, x) - y)**2)
        #print errfunc(p0,height,b)
        p1 = optimize.fmin(errfunc, p0, args=(z,b))
        print p1
        outH[i] = p1[0]
        outdH[i] = p1[1]
    
        if savebin:
            'this is going to dump a plot and exit'
            plt.plot(fitfunc(p1,z),z)
            plt.plot(b,z)
            plt.xlabel('Bakscatter ($m^{-1}sr^{-1}$)')
            plt.ylabel('Height AGL (m)')
            plt.savefig(savebin)
            'in this case, this is the only operation engaged by the code.' 
            exit()
    return (outH,times,outdH)

'''
Additional future methods could be the wavelet method, the log gradient method, 
others...
'''

def _MaxDepth(data,z,range=1000):
    '''
    Internally compute the height of the maximum value of an array, with given inputs
    '''
    if range:
        data = data[:,range/10]
    return np.array(map(lambda x: z[x==np.nanmax(x)],data))

def _LocalMaxDepths(data,z,window,hits=4,range=False):
    '''
    Compute all local max's of a field up to hits number of hits or range
    '''
    if range:
        data = data[:,:range/10]
    dw = window/2
    '''
    I haven't found a nice way to simply map this one up yet.
    '''
    def __scanprof(x):
        'x is a single profile'
        hitcount = 0
        dict = np.zeros(hits)
        for y in range(len(x)):
            'don\'t make any assessments before we can look at a full window'
            if y < dw:
                continue
            'if the value is the maximum value in the window, then we are golden'
            if x[y] == np.nanmax(x[y-dw:y+dw]):
                x[hitcount]=z[y]
                hitcount+=1
            'Only record up to 4 values per time bin'
            if hitcount==hits:
                break
        return dict
    return np.array(map(__scanprof,data))

def _ThresholdLT(data,z,threshold,range=False):
    '''
    Find the lowest height where the value is less than the threshold
    IE in Threshold calcs.
    '''
    if range:
        data=data[:,:range/10]
    def th(x,z,t):
        try:
            return z[x<=t][0]
        except:
            return 0
        
    return np.array(map(lambda x: th(x,z,threshold),data))

def _ThresholdGT(data,z,threshold,range=False):
    '''
    The first height wheret he value is greater than the threshold,
    ie, the Variance method
    '''
    if range:
        data=data[:,:range/10]
    def th(x,z,t):
        try:
            return z[x>=t][0]
        except:
            return 0
        
    return np.array(map(lambda x: th(x,z,threshold),data))

def _ComputeFieldMeans(data,binsize,inTime=True,continuous=False,vertbin=20,
                       power=False):
    '''
    Computed the background data field given the variables from a given data variable
    (slice output is taken as the input) 
    '''
    if power:
        data['bs'] = 10**data['bs']
    if continuous:
        'continuous is not computed WRT time ever, so it is irrelevant'
        bs,times,z = runmean2d(data['bs'],data['time'],data['height'],binsize,vertbin)
        'compute means within binned values...'
    else:
        if vertbin:
            bs,z = runmean(data['bs'],data['height'],vertbin)
            '10*vertbin vertical running mean is given...'
        else:
            bs,z = data['bs'],data['height']
            
        if inTime:
            bs,times = timebin(bs,data['time'],binsize)
        else:
            bs,times = mean2d(bs,data['time'],binsize)
        'and a binsize temporal bin - NOTE that bin sizes should not be the same'
    return bs,times,z

    