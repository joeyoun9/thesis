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
from utilities import *
import logging as l

def threshold(data, threshold= -7.6, cloud= -5, returnfield=False, binsize=0,
               inTime=True, continuous=False, vertbin=5, **kwargs):
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
    if data == 'about':
        'Then something just wants an info string about the method, so spit it out'
        return '010Threshold'
    if binsize == 0:
        'no binning or averaging or whatnot is to be done.'
        z = data['height']
        t = data['time']
        data = data['bs']
    else:
        data, t, z = _ComputeFieldMeans(data, binsize, inTime=inTime, continuous=continuous, vertbin=vertbin)
    if returnfield:
        return (data, t, z)
    depth = _ThresholdLT(data, z, threshold, limit=1200)
    del data
    return (depth, t)

def gradient(data, window=20, cloud= -5, limit=1500, binsize=300, inTime=True,
             continuous=False, multiple=False, returnfield=False,
             eval_distance=20, vertbin=5, minmax= -9.7,
            **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    '''
    if data == 'about':
        return '110Gradient'
    bs, times, z = _ComputeFieldMeans(data, binsize, inTime=inTime,
                                    continuous=continuous, vertbin=vertbin,
                                    power=True)
    del data
    'Compute the vertical gradient!'
    field = np.gradient(bs, eval_distance)[1]
    field[field >= 0.] = np.nan
    'this line, though it is undone in 3 lines, is to protect log10'
    field = np.log10(-1 * field)
    if returnfield:
        field[np.isnan(field)] = np.nanmin(field)
        return (field, times, z)
    'get rid of field data which is beyond the limit of what gets computed'
    field = field[:, z <= limit]
    z = z[z <= limit]
    tops = np.zeros(len(field))
    bottoms = np.zeros(len(field))

    '///////////////////  DETERMINISTIC SECTION  /////////////////////////////'
    if not multiple:
        'FIXME - this should pick the max depth within the largest contiguous'
        'first loop through and identify the largest contiguous non-zero aera'
        i = 0
        field[:, 0] = np.nan
        depth = np.zeros(len(field))
        for prof in np.isnan(field):
            'we get a list of true/false'
            keys = np.arange(len(prof))[prof]
            '=[0,1,2,5,6]'
            'compute the diff of this field'
            kd = np.diff(keys)
            '=[1,1,3,1]'
            startkey = keys[kd == max(kd)][0]
            '=2'
            'the endkey is the next item in keys after startkeys'
            endkey = keys[keys > startkey][0]
            tops[i] = z[endkey]
            bottoms[i] = z[startkey]
            if startkey + 1 == endkey:
                'then there really is no data... weird'
                i += 1
                continue

            zs = z[startkey + 1:endkey]
            fd = field[i, startkey + 1:endkey]
            'pick the LAST match, rather than the first'
            depth[i] = zs[fd == np.nanmax(fd)][-1]

            i += 1
    else:
        '''
        Multiple levels should be returned, with the 
        '''
        depth = _LocalMaxDepths(field, z, window, 4, limit=limit, minmax=minmax)
    del field
    return (depth, times, tops, bottoms)

def ipm(data, limit=1000, binsize=300, inTime=True, eval_dist=20,
              continuous=False, returnfield=False, vertbin=5, **kwargs):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)

    Known as the inflection point method (IPM)
    
    note, if inTime is false, a time value is still required!!!
    '''
    if data == 'about':
        return '110Inflection Point Method'
    bs, times, z = _ComputeFieldMeans(data, binsize, inTime=inTime,
                                    continuous=continuous, vertbin=vertbin,
                                    power=True)
    'Compute the gradient of the gradient'
    'FIXME - do i want negative or positive gradients!?!!'
    field = np.gradient(np.gradient(bs, eval_dist)[1], eval_dist)[1]
    field[field >= 0.] = np.NAN
    field = np.log10(-1 * field)
    if returnfield:
        field[np.isnan(field)] = np.nanmin(field)
        return (field, times, z)
    field = field[:, 20:]
    z = z[20:]
    # We need to compute the max above 200m.
    depth = _MaxDepth(field, z, limit=limit)
    return (depth, times)


def variance(data, binsize=300, limit=1000, inTime=True, returnfield=False,
             continuous=False, power=False, vertbin=5, nbins=20, **kwargs):
    '''
    Compute boundary layer/aerosol layer depth by evaluating temporal variance
    under the assumption that sufficient smoothing will result in oscillations
    of boundary layer top being apparent.
    '''
    if data == 'about':
        return '110Variance'
    data, time, height = _ComputeFieldMeans(data, binsize, inTime=inTime,
                                          continuous=continuous, vertbin=vertbin,
                                          power=power)
    # Now, to preserve shape, I am going to do a running calculation of STDev
    i = 0
    length = len(data)
    '''
    newdata = np.zeros(data.shape)
    while i < length:
        'I am assuming that int/int = int'
        i0 = i - nbins / 2
        i1 = i + nbins / 2
        if i < nbins / 2:
            i0 = 0
        if i > ln - nbins / 2:
            i1 = ln

        clump = data[i0:i1]
        newdata[i] = np.std(clump, axis=0)**2
        i += 1
    '''
    data = runstd(data, nbins) ** 2

    if returnfield:
        return (data, time, height)
    depth = _MaxDepth(data, height, limit=limit)
    return (depth, time)

def noise_variance(data, threshold=0.4, limit=1000, binsize=300, inTime=True,
                   returnfield=False, **kwargs):
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
    if data == 'about':
        'Then something just wants an info string about the method, so spit it out'
        return '110Noise Variance'
    if not threshold:
        raise ValueError, 'You must specify a threshold value'
    time = data['time']
    'bla bla not preserving namespace bla bla bla...'
    height = data['height']
    if inTime:
        data, time = timestd(data['bs'], time, binsize) ** 2
    else:
        data, time = stdev2d(data['bs'], time, binsize) ** 2
    if returnfield:
        return (data, time, height)
    depth = _ThresholdGT(data, height, threshold, limit=limit)
    'and return a tuple'
    return (depth, time)

def idealized(data, binsize=300, returnfield=False, inTime=True, savebin=False,
              continuous=False, guessmean=False, guessheight=False, vertbin=5,
              limit=1000, background= -8.2, threshold= -7.6, **kwargs):
    '''
    Use the idealized backscatter method to identify the top of the aerosol layer.
    
    This routine will use the -7.6 threshold method as a first guess, and will 
    then minimize the defined function to determine the function coefficients 
    
    Parameters
    ----------
    
    data: list
        The produced output from the slice for ceilometer data for the time 
        period analyzed
    binsize: int, optional
        the length in SECONDS for bins to be produced. Longer bins increase 
        the chance of success
    returnfield: bool, optional
        return only the field analyzed, not very useful for this operation.
    inTime: bool, optional
        specify if the provided time dimension is actually epoch time stamps, 
        or just bin numbers
    savebin: str, optional
        only save a demonstrative figure of a single bin. A possibly useful 
        demonstration operation. 
    background: float, optional
        set the background (low value) approximation. The current value is -8.2,
        which is sufficient for Vaisala CL31 ceilometer backscatter in (m*sr)^-1
        units.
   
    '''
    if data == 'about':
        'Then something just wants an info string about the method, so spit it out'
        return '100Idealized Profile'
    from scipy import optimize, special
    bs, times, z = _ComputeFieldMeans(data, binsize, inTime=inTime, continuous=continuous, vertbin=vertbin)
    bs, z = bs[:, :limit / 10], z[:limit / 10]
    'no, this method will not use power'
    if returnfield:
        return (bs, times, z)
    if guessmean and guessheight:
        'A fixed guess mean has been assigned'
        first_guesses = [guessheight for x in times]
        first_guess_mean = [guessmean for x in times]
    else:
        print 'Applying threshold theory'
        first_guesses = _ThresholdLT(bs, z, threshold)
        'compute the low-level means from the 5th ob up to the guess height'
        guess_mean_func = lambda x:np.mean(bs[x][z <= first_guesses[x]])
        first_guess_mean = map(guess_mean_func, range(len(first_guesses)))

    'now, for each time bin, we will run the optimization'
    outH = np.zeros(len(times))
    outdH = np.zeros(len(times))
    for i in range(len(times)):
        '''
        make first guesses and fix the two variables
        '''
        b = bs[i]  # the backscatter profile
        h = first_guesses[i]  # first guess height (a very good guess)]
        dh = 100.  # guess value of dh, based on observation
        'for now we are always assuming a 100m transition layer until told otherwise'
        p0 = [h, dh]
        if h == 0: continue
        bm = first_guess_mean[i]  # approximation for boundary layer intensity, assumed valid
        bu = background  # this is a gross approximation, and will lead to errors...
        'There are two coefficients, A1 and A2, and one is fixed for the fitting'
        a1 = (bm + bu) / 2.
        a2 = (bm - bu) / 2.
        fitfunc = lambda p, z: a1 - a2 * special.erf((z - p[0]) / p[1])
        errfunc = lambda p, z, bs: np.sum((fitfunc(p, z) - bs) ** 2)
        # print errfunc(p0,height,b)
        p1 = optimize.fmin(errfunc, p0, args=(z, b))
        print p1
        outH[i] = p1[0]
        outdH[i] = p1[1]

        if savebin:
            'this code can just save an example bin plot.'
            import matplotlib.pyplot as plt
            plt.plot(fitfunc(p1, z), z)
            plt.plot(b, z)
            plt.xlabel('Bakscatter ($m^{-1}sr^{-1}$)')
            plt.ylabel('Height AGL (m)')
            plt.savefig(savebin)
            'in this case, this is the only operation engaged by the code.'
            return True
    'this can solve to some bizzaro solutions, so we need to filter realistic values'
    outH[(outH > limit) | (outH < 0)] = 0
    outdH[(outdH > limit) | (outdH < -limit)] = 0
    return (outH, times, outdH, first_guess_mean)

def idealized_multiple(data, binsize=300, returnfield=False, inTime=True, savebin=False,
              continuous=False, guessmean=False, guessheight=False, vertbin=5,
              limit=1000, background= -8.2, threshold= -7.6, **kwargs):
    '''
    Use the idealized backscatter method to identify the top of the aerosol layer.
    
    This routine will use the -7.6 threshold method as a first guess, and will 
    then minimize the defined function to determine the function coefficients 
    
    This is from the method proposed by Eresmaa et al 2012
    
    Parameters
    ----------
    
    data: list
        The produced output from the slice for ceilometer data for the time 
        period analyzed
    binsize: int, optional
        the length in SECONDS for bins to be produced. Longer bins increase 
        the chance of success
    returnfield: bool, optional
        return only the field analyzed, not very useful for this operation.
    inTime: bool, optional
        specify if the provided time dimension is actually epoch time stamps, 
        or just bin numbers
    savebin: str, optional
        only save a demonstrative figure of a single bin. A possibly useful 
        demonstration operation. 
    background: float, optional
        set the background (low value) approximation. The current value is -8.2,
        which is sufficient for Vaisala CL31 ceilometer backscatter in (m*sr)^-1
        units.
   
    '''
    l.warning("The mutli-layer idealized profile method has not been implemented")
    exit()
    if data == 'about':
        'Then something just wants an info string about the method, so spit it out'
        return '100Idealized Profile'
    from scipy import optimize, special
    bs, times, z = _ComputeFieldMeans(data, binsize, inTime=inTime, continuous=continuous, vertbin=vertbin)
    bs, z = bs[:, :limit / 10], z[:limit / 10]
    'no, this method will not use power'
    if returnfield:
        return (bs, times, z)
    if guessmean and guessheight:
        'A fixed guess mean has been assigned'
        first_guesses = [guessheight for x in times]
        first_guess_mean = [guessmean for x in times]
    else:
        print 'Applying threshold theory'
        first_guesses = _ThresholdLT(bs, z, threshold)
        'compute the low-level means from the 5th ob up to the guess height'
        guess_mean_func = lambda x:np.mean(bs[x][z <= first_guesses[x]])
        first_guess_mean = map(guess_mean_func, range(len(first_guesses)))

    'now, for each time bin, we will run the optimization'
    outH = np.zeros(len(times))
    outdH = np.zeros(len(times))
    for i in range(len(times)):
        '''
        make first guesses and fix the two variables
        '''
        b = bs[i]  # the backscatter profile
        h = first_guesses[i]  # first guess height (a very good guess)]
        dh = 100.  # guess value of dh, based on observation
        'for now we are always assuming a 100m transition layer until told otherwise'
        p0 = [h, dh]
        if h == 0: continue
        bm = first_guess_mean[i]  # approximation for boundary layer intensity, assumed valid
        bu = background  # this is a gross approximation, and will lead to errors...
        'There are two coefficients, A1 and A2, and one is fixed for the fitting'
        a1 = (bm + bu) / 2.
        a2 = (bm - bu) / 2.
        fitfunc = lambda p, z: a1 - a2 * special.erf((z - p[0]) / p[1])
        errfunc = lambda p, z, bs: np.sum((fitfunc(p, z) - bs) ** 2)
        # print errfunc(p0,height,b)
        p1 = optimize.fmin(errfunc, p0, args=(z, b))
        print p1
        outH[i] = p1[0]
        outdH[i] = p1[1]

        if savebin:
            'this code can just save an example bin plot.'
            import matplotlib.pyplot as plt
            plt.plot(fitfunc(p1, z), z)
            plt.plot(b, z)
            plt.xlabel('Bakscatter ($m^{-1}sr^{-1}$)')
            plt.ylabel('Height AGL (m)')
            plt.savefig(savebin)
            'in this case, this is the only operation engaged by the code.'
            return True
    'this can solve to some bizzaro solutions, so we need to filter realistic values'
    outH[(outH > limit) | (outH < 0)] = 0
    outdH[(outdH > limit) | (outdH < -limit)] = 0
    return (outH, times, outdH, first_guess_mean)

'''
Additional future methods could be the wavelet method, the log gradient method, 
others...
'''
