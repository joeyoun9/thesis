'''
Created on Feb 18, 2013

@author: jyoung

A repository for data objects, similar to that to be developed for 
Muto.

This is not meant to be included in the bundle, it is an internal element.

'''
import copy

class CoreObject():
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
            return self.__dict__[key]
        except:
            # in this case, the attribute does not exist - create it
            self.__dict__[key] = None
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def copy(self):
        '''
        Return a duplicate of this object. Deep copies are mandated because of
        the recursive object property within
        '''
        return copy.deepcopy(self)

# for backwards compatibility.


core_object = CoreObject
