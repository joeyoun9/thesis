'''
Created on Feb 18, 2013

@author: jyoung

A repository for data objects, similar to that to be developed for 
Muto.


'''

class go():
    ''' 
    A simple object which posesses the ability to have its attributes
    manipulated with via the dictionary structure as well as the attribute
    structure.
    
    This is to ease backward compliance with library elements.
    
    Note that there is a catch for all situations here, and therefore this 
    is unlikely to fail. Hopefully this does not cause any undesired operation.
    '''
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except:
            # in this case, the attribute does not exist - create it
            self.__dict__[key] = None
    def __setitem__(self, key, value):
        self.__dict__[key] = value


