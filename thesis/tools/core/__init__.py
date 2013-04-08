'''
A package for holding tools which are fundamental to the internal workings
of the package. These contents will likely be ported to Muto very quickly.
'''
__all__ = ['objects', 'pytables']

import os, sys
import importlib

def import_sources():
    '''
    This reads the environment for the computer used, and imports the sources
    provided there in python format to the srcs by appending that file to the
    system path, importing it and calling it srcs. 
    
    The imported file should have access to the thesis library, but all of it's objects
    will be in srcs, as per standar python imports. 
    '''
    if 'THESIS_SOURCES' in os.environ.keys():
        # Ok, grab the source file
        srcf = os.environ['THESIS_SOURCES']
        srcd = os.path.split(srcf)[0]
        sys.path.append(srcd)
        import_name = os.path.split(srcf)[1][:-3]

        srcs = __import__(import_name, globals(), locals())
        return srcs
    else:
        print 'No local sources environment found (THESIS_SOURCES)'
