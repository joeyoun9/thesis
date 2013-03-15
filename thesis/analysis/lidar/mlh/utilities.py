'''
Created on Feb 15, 2013

@author: jyoung

This is a module containing the methods which will assist in layer method
computation
'''
import numpy as np
from thesis.tools import *


def _MaxDepth(data, z, limit=1000):
    '''
    Internally compute the height of the maximum value of an array, with given inputs
    '''
    if limit:
        data = data[:, 7:limit / 10]
    else:
        data = data[:, 7:]
    def maxp(x):
        try:
            return z[x == np.nanmax(x)][0]
        except:
            return 0
    return np.array(map(maxp, data))

def _LocalMaxDepths(data, z, window, hits=4, limit=False, minmax=None):
    '''
    Compute all local max's of a field up to hits number of hits or range
    '''
    if limit:
        data = data[:, 7:limit / 10]
    else:
        data = data[:, 7:]
    dw = window / 2
    '''
    I haven't found a nice way to simply map this one up yet.
    '''
    def __scanprof(x):
        'x is a single profile'
        hitcount = 0
        dict = np.zeros(hits)
        for y in np.arange(len(x)):
            'don\'t make any assessments before we can look at a full window'
            if y < dw:
                continue
            'if the value is the maximum value in the window, then we are golden'
            mx = np.nanmax(x[y - dw:y + dw])
            if mx > minmax and x[y] == mx:
                dict[hitcount] = z[y]
                hitcount += 1
            'Only record up to 4 values per time bin'
            if hitcount == hits:
                break
        return dict
    return np.array(map(__scanprof, data))

def _ThresholdLT(data, z, threshold, limit=False):
    '''
    Find the lowest height where the value is less than the threshold
    IE in Threshold calcs.
    '''
    if limit:
        data = data[:, 7:limit / 10]
    else:
        data = data[:, 7:]
    def th(x, z, t):
        try:
            return z[x <= t][0]
        except:
            return 0

    return np.array(map(lambda x: th(x, z, threshold), data))

def _ThresholdGT(data, z, threshold, limit=False):
    '''
    The first height wheret he value is greater than the threshold,
    ie, the Variance method
    '''
    if limit:
        data = data[:, 7:limit / 10]
    else:
        data = data[:, 7:]
    def th(x, z, t):
        try:
            return z[x >= t][0]
        except:
            return 0

    return np.array(map(lambda x: th(x, z, threshold), data))

def _ComputeFieldMeans(data, binsize, inTime=True, continuous=False, vertbin=20,
                       power=False):
    '''
    Computed the background data field given the variables from a given data variable
    (slice output is taken as the input) 
    '''
    if power:
        data['bs'] = 10 ** data['bs']
    if continuous:
        'continuous is not computed WRT time ever, so it is irrelevant'
        # FIXME - this should be redone as a c
        field, times, z = runmean2d(data['bs'], binsize, vertbin), data['time'], data['height']
        'compute means within binned values...'
    else:
        if vertbin:
            field, z = runmean(data['bs'], vertbin, ax=1), data['height']
            '10*vertbin vertical running mean is given...'
        else:
            field, z = data['bs'], data['height']


        if inTime:
            field, times = timebin(field, data['time'], binsize)
        else:
            'mean2d is meant to be much faster than timebin'
            field, times = mean2d(field, data['time'], binsize)
    del data
    return field, times, z
