'''
A module to assist in the analysis of ceilometer boundary layers
'''
import numpy as np
from thesis.tools import *
def threshold_depth(threshold, data, height, cloud=-5):
    '''
    for a formatted backsctter dataset, determine a timeseries of the lowest incidence
    of the specified backscatter value, regardless of mathematical base.
    
    Parameters
    ----------
    threshold: float
        specify the cutoff value for the threshold to be determined from the bottom up
        
    data: numpy 2-d array
        the dataset from which the thresholds are determined
        
    height: list,numpy array
        a list of height indices which should also be the same length as the second dimension
        as the backscatter dataset.
        
    cloud: float, optional
        a value specifying the maximum value to be interpreted as a cloud. Values are not 
        computed above clouds, as they are somewhat meaningless.
        
    '''
    depth = [0 for x in range(len(data))]
    for x in range(len(data)):
        "for each bin, find the lowest point the value is the threshold"
        for y in range(len(data[x])):
            if data[x,y] <= threshold:
                depth[x] = height[y]
                break
            if data[x,y] > cloud:
                depth[x]=np.nan
                break
            
            # and plot
    return depth



def gradient(data,cloud=-5,limit=1500,binsize=20):
    '''
    determine mixed layer/aerosol depth by determinng the maximum decrease 
    (this is not the second gradient method)
    
    lowest 1500 m only
    '''
    height = data['height']
    time = mean1d(data['time'],binsize)
    data = np.gradient(mean2d(data['bs'],binsize))[0]
    depth = [0 for x in range(len(data))]
    for x in range(len(data)):
        "each time bin."
        max_grad = 0 #"we seek the minimum gradient..."
        mh = 0 #"the height of the current winner"
        for y in np.arange(len(height))[height<=limit]:
            "loop through heights, but only for keys less than 1500m"
            if data[x,y] < max_grad:
                mh = height[y]
        depth[x]=mh
    return (depth,time)

def stdev(threshold,data,binsize=20):
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
    