'''
A package for methods specific to ceilometer analysis, such as cloud detection
and rain detection. 

Some of this is actually PCAPS specific, but, that will be dealt with later.
'''
from thesis.tools.core.objects import core_object as co
import numpy as np
from thesis.tools import *
import logging as l

class Filter(co):
    '''
    A class of methods for filtering times by specific events, which can be combined
    for specific criteria.
    
    All methods are designed for vertical lidar profiles, however they are also
    CL-31 ceilometer centric until further notice.
    
    All methods operate on the class and return itself, so it can be run as 
    Filter.cloud().virga().mean2d(30) Though the .virga in this instance would be redundant
    '''
    def __init__(self, data, copy=True):
        '''
        Initialize the filter object. By default data elements are duplicated 
        to allow multuple procedures to engage. This may not be desired for memory reasons
        
        Set copy=False if copying is not desired
        '''
        # initialize the class
        if type(data) == str:
            # if data is a string, then it is a filename we should initialize from
            f = np.load(data)
            self.bs = f['bs']
            self.time = f['time']
            self.height = f['height']
        else:
            if copy:
                self.bs = data['bs'].copy()
                self.time = data['time'].copy()
            else:
                self.bs = data['bs']
                self.time = data['time']
            if 'height' in dir(data):
                if copy:
                    self.height = data['height'].copy()
                else:
                    self.height = data['height']
            else:
                self.height = np.arange(self.bs.shape[1]) * 10
                # CL31 centric height default
        self.len = self.time.shape[0]
        # now hopefully filters can be applied to any dataset quickly and efficiently.

    def cloud(self, exclude=True):
        '''
        Attempt to algorithmically identify when there is a CAP layer which is 
        topped by a condensed cloud
        
        loop through bs, and time, and remove all times and profiles which meet 
        the defined criteria
        
        I will implement a shift-replace mechanism
        
        '''
        i = 0
        maxs = np.amax(self.bs, axis=1)
        self.cloudheights=np.zeros(self.time.shape)
        for p in xrange(self.len):
            if exclude:
                if maxs[p] < -5.3:
                    self.bs[i] = self.bs[p]
                    self.time[i] = self.time[p]
                    i += 1
            else:
                # this data is being included, to the exclusion of all others
                if maxs[p] > -5.3:
                    self.bs[i] = self.bs[p]
                    self.time[i] = self.time[p]
                    self.cloudheights=self.height[self.bs[p]==maxs[p]][0]
                    i += 1
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        return self

    def precip(self, exclude=True):
        '''
        Determine if precipitation is reaching the ground in a lidar profile
        
        Exclusion has not been implemented currently. we are not implementing
        rain beneficial analyses at this time. 
        
        '''
        i = 0
        # the mean of 50 - 150m backscatter should be > -5?
        means = np.mean(self.bs[:, 5:15], axis=1)
        for p in xrange(self.len):
            if exclude:
                if  means[p] < -5.5:
                    self.bs[i] = self.bs[p]
                    self.time[i] = self.time[p]
                    i += 1
            else:
                if  means[p] >= -5.5:
                    self.bs[i] = self.bs[p]
                    self.time[i] = self.time[p]
                    i += 1
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        return self

    def virga(self, exclude=True,details=False):
        '''
        Virga: greater than 100m of rain-like extinction without being present at the surface
        
        if details are requested, then it should return a dit of the limits of the virga...
        '''
        i = 0
        if details:
            ret = np.zeros(self.time.shape[0],2)
        for p in xrange(self.len):
            if max(self.bs[p,3:7]) < -5. and max(self.bs[p]) > -5.:
                
                # determine vertial extent
                heights = self.height[self.bs[p]>-5.5]
                if len(heights)<10:
                    continue
                if heights[-2]-heights[1]<150:
                    continue
                self.bs[i] = self.bs[p]
                self.time[i] = self.time[p]
                i += 1
                if details:
                    ret[i] =[heights[1],heights[-2]] # 
                
            # if not, then continue
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        if details:
            self.virgaheights = ret[:i] # good luck using this..
        return self

    def CAP(self, exclude=False, threshold= -7.6):
        '''
        CAP in this research is defined as simply exceeding a threshold before going below it
        
        Note that exclude is used in the same fashion as elsewhere, hence being default false.
        
        '''
        keyarray = np.arange(self.bs.shape[1] - 7)
        highs = (self.bs[:, 7:] > threshold)
        lows = (self.bs[:, 7:] < threshold)
        # if there is a CAP the value of 'high' should first occur lower than 'low'
        c = 0
        for i in xrange(self.len):
            start_high = keyarray[highs[i]]
            if len(start_high) < 1:
                continue
            start_high = start_high[0]
            start_low = keyarray[lows[i]][0]
            if not exclude and start_high < start_low:
                self.bs[c] = self.bs[i]
                self.time[c] = self.time[i]
                c += 1
            elif exclude and start_high > start_low:
                self.bs[c] = self.bs[i]
                self.time[c] = self.time[i]
                c += 1
        self.bs = self.bs[:c]
        self.time = self.time[:c]
        self.len = c
        return self

    def mlh_method(self, method, **kwargs):
        '''
        run any mlh method, provided as method, with keyword arguments kwargs on the data contained
        The contained data is not modified.
        '''

        return method(self, **kwargs)

    def smooth(self, binsize, inTime=True, continuous=False, vertbin=5,
                       power=False):
        '''
        Compute the temporal mean of the backscatter field, adjust time and bs values accordingly
        
        This can be done continuously, but if so, inTime must be turned off
        '''
        if power:
            self.bs = 10 ** self.bs
        if continuous:
            'continuous is not computed WRT time ever, so it is irrelevant'
            # FIXME - this should be redone as a c
            self.bs = runmean2d(self.bs, binsize, vertbin)
            # height and time information is not changed with running means
        else:
            # this is to be done chunk wise. Vertical smoothing is done automatically and continuously
            if vertbin:
                self.bs = runmean(self.bs, vertbin, ax=1)
            if inTime:
                self.bs, self.time = timebin(self.bs, self.time, binsize)
            else:
                # 'mean2d is meant to be much faster than timebin'
                self.bs, self.time = mean2d(self.bs, self.time, binsize)
        return self
    def slice(self,tt):
        '''
        Replicates the slice mechanism of the CoreObject, but returns a Filter object. 
        
        Prefereably not dangerously recursively...
        '''
        return Filter(co(duplicate=self).slice(tt))

    def mask(self, threshold= -7.6, maskvalue= -8.):
        '''
        Hide all the values above the first point where the threshold is exceeded(low)
        '''
        def dropat(bs, t=threshold, lm=maskvalue):
            k = np.arange(len(bs))[bs <= t]
            try:
                bs[k[0]:] = lm
            except:
                l.info('Failed to mask')
            return bs

        self.bs = np.array(map(dropat, self.bs))
        return self







