'''
A package for methods specific to ceilometer analysis, such as cloud detection
and rain detection. 

Some of this is actually PCAPS specific, but, that will be dealt with later.
'''

def cloud_topped():
    '''
    Attempt to algorithmically identify when there is a CAP layer which is 
    topped by a condensed cloud
    '''
    pass

def precip():
    '''
    Simple algorithm to tell when there is precip/influences which will largely
    undermine any form of analysis
    '''
    pass

def virga():
    '''
    Attempt to algorithmically identify peropds where there is virga
    '''
    pass

def CAP():
    '''
    Attempt to identify CAP periods, and possibly strength from ceilometer
    data, 
    '''
    pass
