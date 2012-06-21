'''
A package designed to enable analysis, collection, concentration and organization of data from
field projects I am using for my thesis.

Joe Young, June 2012

'''
all = ['compress','tools','pcaps']


thesisverbose=False
#FIXME - this will be reset every time it is re-imported

def verbose():
    '''
    A method on the package which modifies the internal variables to enable verbose actions.
    Conversely one could simply set the global variable 
        >>> thesisverbose=True
        
    Which is simply what this function does
    '''
    global thesisverbose
    thesisverbose=False
