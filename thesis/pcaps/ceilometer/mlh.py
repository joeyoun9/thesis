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

def threshold(data, threshold = -7.6, cloud=-5, returnfield=False, **kwargs):
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
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '010Threshold'
    z = data['height']
    t = data['time']
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
    return (depth,t)

def gradient(data, threshold=-.002, cloud=-5,limit=1500, binsize=300,
            multiple=False, returnfield=False, eval_distance=20, **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '110Gradient'
    #FIXME: this could be modified to detect multiple layers above a certain gradient level
    if not threshold and multiple:
        raise ValueError, 'You must specify a threshold value to get multiple layers'
    from thesis.tools import runmean
    ''' start by evaluating a .7 std dev threshold '''
    #std = stdev(.6,data,binsize=binsize)[0]
    z = data['height']
    bs,times = timemean(runmean(data['bs']**10,20),data['time'],binsize)
    'compute 200m vertical running mean on BS data'
    data = np.log(-1*np.gradient(bs,eval_distance)[1])
    data[np.isnan(data)]=0
    'and seek local maxima!'
    if returnfield:
        return (data,times)
    if not multiple:
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
    else:
        '''
        The multiple option on this method means that we search for all
        points where the gradient exceeds the threshold:
        
        There is one other rule, in order to be picked again, there MUST
        be a positive gradient value between the two.
        '''
        depth = np.zeros((len(data),4))
        for x in range(len(data)):
            hitcount = 0
            beenpositive=True
            for y in np.arange(len(z))[(z>=50)&(z<=limit)]:
                if data[x,y] <= threshold and beenpositive:
                    depth[x,hitcount]=z[y]
                    beenpositive=False
                    hitcount +=1
                if data[x,y] > 0:
                    beenpositive = True
                if hitcount == 4:
                    'only 4 heights can be saved.'
                    break
        return (depth,times)
            

def gradient2(data, threshold=-5e-5, cloud=-5, limit=1500,binsize=300, returnfield=False, **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '1102nd Gradient'
    #FIXME: this could be modified to detect multiple layers above a certain gradient level
    if not threshold:
        raise ValueError, 'You must specify a threshold value'
    from thesis.tools import runmean
    ''' start by evaluating a .7 std dev threshold '''
    #std = stdev(.6,data,binsize=binsize)[0]
    z = data['height']

    bs,times = timemean(runmean(data['bs'],20),data['time'],binsize)
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

def variance(data, threshold=0.1, binsize=300,returnfield=False, **kwargs):
    '''
    the evaluation of boundary layer height using the assumption that variance
    is highest at the top of the boundary layer
    '''
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '110Variance'
    if not threshold:
        raise ValueError, 'You must specify a threshold value'
    from thesis.tools import runmean
    height = data['height']
    data,time = timemean(runmean(data['bs'],10),data['time'],binsize/3) 
    'compute time mean (total bin / 3) data with 100 m running vertical mean'
    data,time = timestd(data,time,binsize)
    'Compute the temporal standard deviation over 3 blocks, as computed from earlier' 
    if returnfield:
        return (data,time)
    depth = np.zeros(len(time))
    'To find a deterministic value, determine where the value exceeds the threshold from the bottom'
    for x in range(len(data)):
        "for each bin, find the lowest point the value is the threshold"
        for y in range(len(data[x])):
            if data[x,y] >= threshold:
                'Quick QC check'
                if data[x,y] > 0.35:
                    'then we have a noise problem'
                    break
                depth[x] = height[y]
                break
    return depth,time

def noise_variance(data, threshold=0.4, binsize=300,returnfield=False, **kwargs):
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
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '110Noise Variance'
    if not threshold:
        raise ValueError, 'You must specify a threshold value'
    time = data['time']
    height = data['height']
    data,time = timestd(data['bs'],data['time'],binsize)
    # becomes too huge by expanding the logarithm
    if returnfield:
        return (data,time)
    depth = np.zeros(len(data))
    for x in range(len(data)):
        "for each bin, find the lowest point the value is the threshold"
        for y in range(len(data[x])):
            if data[x,y] >= threshold:
                depth[x] = height[y]
                break
            #if data[x,y] > cloud:
            #    depth[x]=np.nan
            #    break
        
    'and return a tuple'
    return (depth,time)

def idealized(data, binsize=300, returnfield=False, savebin=False, **kwargs):
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
    if data =='about':
        'Then something just wants an info string about the method, so spit it out'
        return '100Idealized Profile'
    
    from scipy import optimize,special
    bs = data['bs'][:,5:200]
    times = data['time']
    z = data['height'][5:200]
    bs,times = timemean(bs,times,binsize)
    if returnfield:
        return (bs,times)
    first_guesses,times = threshold({'bs':bs,'height':z,'time':times}) 
    'compute the low-level means from the 5th ob up to the guess height'
    guess_mean = lambda x:np.mean(bs[x][z<=first_guesses[x]])
    first_guess_mean = np.array(map(guess_mean,range(len(first_guesses))))
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
        
    print 'Returning Idealized Statistics: ',outH.shape,times.shape,outdH.shape
    return (outH,times,outdH)


    