"""
Read sodar data - ASC Minisodar for now.
"""

from thesis.tools.pytables import *
from thesis.tools import s2t

import numpy as np

def read(files,save):
	"""
		give a list of files, they will be read, and then saved where specified
		
	"""
	# assumed 200m range, 20-200 m in 10 m gates
	# 4 lines of info
	# 18 lines data
	# 10 minutes each ( valid 5 minutes after time read)
	doc = h5(save)
	size = 19# again, with 20-200/10
	doc.create(height=size,wspd=size,wdir=size,w=size,sdw=size,iw=size,gspd=size,gdir=size,u=size,sdu=size,
		iu=size,snru=size,v=size,sdv=size,iv=size,snrv=size,snrw=size)
	for f in sorted(files):
		# files had best be a list
		print 'reading',f.split('/')[-1]
		fh = open(f)
		dat = fh.readlines()#ouch
		fh.close()
		# and now chunk through the obs
		i = 0
		while i < len(dat):
			fluff = dat[i:i+4]
			info = np.array([x.split() for x in dat[i+4:i+23]]).T # not the fastest...
			topbar = fluff[0].split()
			time = s2t(topbar[1]+topbar[2]+"UTC",'%m/%d/%Y%H:%M:%S%Z')
			if i == 0:
				# append height index information
				doc.append(time,persist=True,height=info[0],wspd=info[1],wdir=info[2],w=info[3],sdw=info[4],iw=info[5],
					gspd=info[6],gdir=info[7],u=info[8],sdu=info[9],iu=info[11],snru=info[12],
					v=info[13],sdv=info[14],iv=info[16],snrv=info[17],snrw=info[19])
			else:
				doc.append(time,persist=True,wspd=info[1],wdir=info[2],w=info[3],sdw=info[4],iw=info[5],
					gspd=info[6],gdir=info[7],u=info[8],sdu=info[9],iu=info[11],snru=info[12],
					v=info[13],sdv=info[14],iv=info[16],snrv=info[17],snrw=info[19])
				
			i+=23
	doc.close()
		
