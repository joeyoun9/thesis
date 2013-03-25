'''
Created on Feb 18, 2013

@author: jyoung

A repository for data objects, similar to that to be developed for 
Muto.

This is not meant to be included in the bundle, it is an internal element.

'''
import copy
from numpy import savez
import logging as l

class CoreObject(object):
    ''' 
    A simple object which possesses the ability to have its attributes
    manipulated with via the dictionary structure as well as the attribute
    structure.
    
    This is to ease backward compliance with library elements.
    
    Note that there is a catch for all situations here, and therefore this 
    is unlikely to fail. Hopefully this does not cause any undesired operation.
    '''
    def __init__(self):
        # nothing to do here at this time
        pass

    def __getitem__(self, key):
        try:
            return object.__getattr__(self, key)
        except:
            # in this case, the attribute does not exist - create it
            l.warning('Key "' + key + '" was not found')
            object.__setattr__(self, key, None)
            return None
    def __setitem__(self, key, value):
        object.__setattr__(self, key, value)

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

# for backwards compatibility.
core_object = CoreObject
