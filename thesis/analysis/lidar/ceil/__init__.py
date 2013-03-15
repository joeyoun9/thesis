'''
A package for methods specific to ceilometer analysis, such as cloud detection
and rain detection. 

Some of this is actually PCAPS specific, but, that will be dealt with later.
'''
import thesis.tools.core.objects.core_object as co
import numpy as np

class Filter(co):
    '''
    A class of methods for filtering times by specific events, which can be combined
    for specific criteria.
    
    All methods are designed for vertical lidar profiles, however they are also
    CL-31 ceilometer centric until further notice.
    
    All methods will return times and 
    '''
    def __init__(self, data):
        # initialize the class
        self.bs = data.bs
        self.time = data.time
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
        for p in xrange(self.len):
            if maxs[p] < -5:
                self.bs[i] = self.bs[p]
                self.time[i] = self.time[p]
                i += 1
            # if not, then continue
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
            if  means[p] < -5:
                self.bs[i] = self.bs[p]
                self.time[i] = self.time[p]
                i += 1
            # if not, then continue
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        return self

    def virga(self, exclude=True):
        '''
        Attempt to algorithmically identify peropds where there is virga
        
        Utilize backscatter thresholds and characteristic shape (strong, with
        greater than 200m of high returns below it, but ending above 200m above the surface
        
        
        '''
        i = 0
        maxs = np.amax(self.bs, axis=1)
        for p in xrange(self.len):
            if max(self.bs[p]) < -5:
                self.bs[i] = self.bs[p]
                self.time[i] = self.time[p]
                i += 1
            # if not, then continue
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        return self

    def CAP(self):
        '''
        Attempt to identify CAP periods, and possibly strength from ceilometer
        data,
        
        This could simply be based on a successfull detection of a layer with the 
        idealized profile method? -- too inefficient
        
        '''
        i = 0
        maxs = np.amax(self.bs, axis=1)
        for p in xrange(self.len):
            if max(self.bs[p]) < -5:
                self.bs[i] = self.bs[p]
                self.time[i] = self.time[p]
                i += 1
            # if not, then continue
        self.bs = self.bs[:i]
        self.time = self.time[:i]
        self.len = i
        return self





