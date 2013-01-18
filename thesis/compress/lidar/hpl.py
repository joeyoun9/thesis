"""
	Read in halophotonics data files from their doppler scanning lidar
	
"""
from thesis.tools.bundle import *
from thesis.tools import s2t
import numpy as np

def h5_compress_stares(files, save, maxdim=312):
    """
        Read the files and return a gridded data object
        bin_size is the distance in minutes of the bins
    """
    doc = h5(save)
    doc.create(indices={'height':maxdim},bs=maxdim,snr=maxdim,doppler=maxdim,dz=1)
    
    for fd in files:

        fname = fd.split('/')[-1]
        logging.info('reading',fname)
        # file format expected: Stare_20_20110617_18.hpl
        'we are only looking for the date. The hour is given elsewhere'
        otime = s2t(fname[-15:-7]+"UTC","%Y%m%d%Z")
        f = open(fd)
        'Files are ~6MB, so we can just read them in, as array of lines.'
        lines = f.readlines()
        f.close()
        gates = int(lines[2].split()[-1])
        if gates > maxdim: continue #skip those guys
        dz    = float(lines[3].split()[-1])
        i=17
        while i < len(lines):
            try:
                time = float(lines[i].split()[0])*3600 + otime
                data = np.array([np.fromstring(lines[x],sep=' ',dtype=np.float32) for x in range(i+1,i+gates+1)])
                data.resize((maxdim,4))
                i+=gates+1
                doc.append(time,bs=data[:,3],snr=data[:,2],doppler=data[:,1],dz=[dz],persist=True)
            except (KeyboardInterrupt,SystemExit):
                doc.close()
                exit()
            except:
                logging.debug('Encountered an error, with data shape:',data.shape)
                'a file never recovers from this'
                break
    doc.close()
    
#FIXME - need to add support for all the other scans. Preferably into one file
def h5_compress(files, save, maxdim=312):
    """
        Read the files and return a gridded data object
        bin_size is the distance in minutes of the bins
    """
    doc = h5(save)
    doc.create(indices={'range':maxdim},bs=maxdim,snr=maxdim,doppler=maxdim,dz=1)
    
    for fd in files:

        fname = fd.split('/')[-1]
        print 'reading',fname
        # file format expected: Stare_20_20110617_18.hpl
        'we are only looking for the date. The hour is given elsewhere'
        otime = s2t(fname[-15:-7]+"UTC","%Y%m%d%Z")
        f = open(fd)
        'Files are ~6MB, so we can just read them in, as array of lines.'
        lines = f.readlines()
        f.close()
        gates = int(lines[2].split()[-1])
        if gates > maxdim: continue #skip those guys
        dz    = float(lines[3].split()[-1])
        i=17
        while i < len(lines):
            try:
                time = float(lines[i].split()[0])*3600 + otime
                data = np.array([np.fromstring(lines[x],sep=' ',dtype=np.float32) for x in range(i+1,i+gates+1)])
                data.resize((maxdim,4))
                i+=gates+1
                doc.append(time,bs=data[:,3],snr=data[:,2],doppler=data[:,1],dz=[dz],persist=True)
            except (KeyboardInterrupt,SystemExit):
                doc.close()
                exit()
            except:
                print data.shape
                'a file never recovers from this'
                break
    doc.close()

		
		
