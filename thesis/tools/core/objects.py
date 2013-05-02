'''
Created on Feb 18, 2013

@author: jyoung

A repository for data objects, similar to that to be developed for 
Muto.

This is not meant to be included in the bundle, it is an internal element.

'''
import copy
from numpy import savez, load
import logging as l
# #from pytables import h5
from numpy import array

class CoreObject(object):
    ''' 
    A simple object which possesses the ability to have its attributes
    manipulated with via the dictionary structure as well as the attribute
    structure.
    
    This is to ease backward compliance with library elements.
    
    Note that there is a catch for all situations here, and therefore this 
    is unlikely to fail. Hopefully this does not cause any undesired operation.
    '''
    def __init__(self, fname=None, dataset=None):
        # nothing to do here at this time
        self.time = array([])
        self.data = []  # really no use for this one...
        self.indices = []  # could be used, but usually isnt...
        if fname:
            # file can be a name or handle, just pass it to np.load. This should
            # be able to re-read anything created by the savez function! Yay!
            f = load(fname)
            for key, val in f.iteritems():
                self[key] = val
        if dataset:
            # then load the contents of this. It must be a dict
            for key, val in dataset.iteritems():
                self[key] = val.copy()
        # data is a list which must be appended to, showing the names of all data
        # values which will be saved. Savez will not do this
        return None

    def __getitem__(self, key):
        try:
            return object.__getattribute__(self, key)
        except:
            # in this case, the attribute does not exist - create it
            l.warning('Key "' + key + '" was not found')
            object.__setattr__(self, key, None)
            return None
    def __setitem__(self, key, value):
        object.__setattr__(self, key, value)
        return None
    def copy(self):
        '''
        Return a duplicate of this object. Deep copies are mandated because of
        the recursive object property within
        '''
        return copy.deepcopy(self)

    def savez(self, filename):
        '''
        Save the data arrays in this object 
        
        The file is structured such that the first item is a list of names, and
        the subsequent items are those specific values
        
        
        '''
        savez(filename, **self.__dict__)
        '''
    def hdf(self, filename):
        \'''
        Save this object as an HDF object using this project's HDF library
        to file filename
        \'''
        doc = h5(filename)
        variables = {}
        indices = {}
        try:
            keylen = self.time.shape[0]
        except:
            l.warning('To save as HDF, this must be a time-oriented dataset. CoreObject.time not found')
            return False
        # loop through elements, and save all data elements
        for key in self.data:
            variables[key] = self[key].shape
        for key in self.indices:
            indices[key] = self[key].shape
        doc.create(indices=indices, **variables)
        # Actually, forget it
    '''
    def __iter__(self):
        self._current = 0
        self._max = len(self.time)
        return self
    def next(self):
        if self._current >= self._max:
            raise StopIteration
        else:
            # create a new CoreObject, to return
            new = CoreObject()
            for key, value in self.__dict__.iteritems():
                try:
                    sz = value.shape[0]
                except:
                    continue
                if sz == self.time.shape[0]:
                    new[key] = value[self._current]
            self._current += 1
            return new




# for backwards compatibility.
core_object = CoreObject
