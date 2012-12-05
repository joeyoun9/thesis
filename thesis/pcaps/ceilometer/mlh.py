'''
A module to assist in the analysis of ceilometer boundary layers
'''
import numpy as np
from thesis.tools import *

def threshold(data, threshold = -7.6, cloud=-5, returnfield=False):
    '''
    for a formatted backsctter dataset, determine a timeseries of the lowest incidence
    of the specified backscatter value, regardless of mathematical base.
    
    Parameters
    ----------
    threshold: float, optional
        specify the cutoff value for the threshold to be determined from the bottom up
        
    data: numpy 2-d array
        the dataset from which the thresholds are determined
        
    cloud: float, optional
        a value specifying the maximum value to be interpreted as a cloud. Values are not 
        computed above clouds, as they are somewhat meaningless.
        
    '''
    z = data['height']
    data = data['bs']
    'time is not a factor for this analysis'
    if returnfield:
        raise ValueError,'There is no computed field for the threshold analysis'
    depth = np.zeros(len(data))
    for x in range(len(data)):
        "for each bin, find the lowest point the value is the threshold"
        for y in range(len(data[x])):
            if data[x,y] <= threshold:
                depth[x] = z[y]
                break
            if data[x,y] > cloud:
                depth[x]=np.nan
                break
            
            # and plot
    return depth

def gradient(data, threshold=False, cloud=-5,limit=1500,binsize=300, returnfield=False):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    
    '''
    #FIXME: this could be modified to detect multiple layers above a certain gradient level
    from thesis.tools import runmean
    ''' start by evaluating a .7 std dev threshold '''
    #std = stdev(.6,data,binsize=binsize)[0]
    z = data['height']
    bs,times = timebin(runmean(data['bs'],20),data['time'],binsize)
    'compute 200m vertical running mean on BS data'
    data = np.gradient(bs,20)[1]
    if returnfield:
        return (data,times)
    depth = np.zeros(len(data))
    for x in range(len(data)):
        "each time bin."
        max_grad = 0 #"we seek the minimum gradient..."
        mh = 0 #"the height of the current winner"
        for y in np.arange(len(z))[(z>50)&(z<=limit)]:
            "loop through heights, but only for keys less than 1500m"
            if data[x,y] < max_grad:
                mh = z[y]
                max_grad = data[x,y]
            #if height[y]>=std[x]:
            #    break
        depth[x]=mh
    return (depth,times)

def gradient2(data, threshold=False, cloud=-5, limit=1500,binsize=300, returnfield=False):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    
    '''
    #FIXME: this could be modified to detect multiple layers above a certain gradient level
    from thesis.tools import runmean
    ''' start by evaluating a .7 std dev threshold '''
    #std = stdev(.6,data,binsize=binsize)[0]
    height = data['height']

    bs,times = timebin(runmean(data['bs'],20),data['time'],binsize)
    'compute 200m vertical running mean on BS data'
    'Compute the gradient of the gradient'
    data = np.gradient(np.gradient(bs,20)[1],20)[1]
    
    if returnfield:
        return (data,times)
    depth = np.zeros(len(data))
    for x in range(len(data)):
        "each time bin."
        max_grad = 0 #"we seek the minimum gradient..."
        mh = 0 #"the height of the current winner"
        for y in np.arange(len(z))[(z>50)&(z<=limit)]:
            "loop through heights, but only for keys less than 1500m"
            if data[x,y] < max_grad:
                mh = z[y]
                max_grad = data[x,y]
            #if height[y]>=std[x]:
            #    break
        depth[x]=mh
    return (depth,times)


def variance(data, threshold, binsize=20,returnfield=False):
    '''
    the evaluation of boundary layer height using the assumption that variance
    is highest at the top of the boundary layer
    '''
    from thesis.tools import runmean
    height = data['height']
    time = mean1d(data['time'],binsize)
    data = runmean(data['bs'],10) #100 m running vertical mean
    data = np.stdev(mean2d(data,binsize),20)[0]
    if returnfield:
        return data,time
    else:
        raise ValueError, 'Sorry, there is no deterministic output for the variance analysis currently'
    'for now all this routine returns is the actual plot of data...'

def noise_variance(data, threshold, binsize=20,returnfield=False):
    '''
    use standard deviation calculations to determine the top of the layer
    under the theory that robust returns come from particle presence, and 
    noise is harder to filter where there is low return.
    
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
    time = data['time']
    height = data['height']
    data = stdev2d(data['bs'],binsize) # becomes too huge by expanding the logarithm
    time = mean1d(time,binsize) 
    depth = [0 for x in range(len(data))]
    for x in range(len(data)):
        "for each bin, find the lowest point the value is the threshold"
        for y in range(len(data[x])):
            if data[x,y] >= threshold:
                depth[x] = height[y]
                break
            #if data[x,y] > cloud:
            #    depth[x]=np.nan
            #    break
        
    # and return a tuple
    return (depth,time)


def idealized(data, binsize=300, returnfield=False, savebin=False):
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
    savebin: str, optional
        only save a demonstrative figure of a single bin. A possibly useful demonstration
        operation. 
   
    '''
    from scipy import optimize,special
    bs = data['bs'][:,5:200]
    times = data['time']
    z = data['height'][5:200]
    bs,times = timebin(bs,times,binsize)
    if returnfield:
        return (bs,times)
    first_guesses = threshold({'bs':bs,'height':z}) # gotta fake it this time
    'compute the low-level means from the 5th ob up to the guess height'
    first_guess_mean = np.array(map(lambda x:np.mean(bs[x][z[5:]<=first_guesses[x]]),range(len(first_guesses))))
    'now, for each time bin, we will run the optimization'
    outH = np.zeros(len(times))
    outdH = np.zeros(len(times))
    print 'looping'
    for i in range(len(times)):
        '''
        make first guesses and fix the two variables
        '''
        b = bs[i] # the backscatter profile
        h = first_guesses[i] # first guess height (a very good guess)]
        dh = 50.
        'for now we are always assuming a 200m transition layer until told othewise'
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
        
        
    return (outH,outdH,times)


    