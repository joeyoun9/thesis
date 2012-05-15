"""
read ct12 messages
"""

import numpy as np


def read(ob):
	SCALING_FACTOR = 1.0e7
	#FIXME - also not grabbing clouds at this time...
	p = ob.split(unichr(002))
	code = p[0].strip()
	ob = p[1].strip()

	cld = []
	data = ob.split("\n")
	if len(data) is not 19:
		return False

	# the code line does not indicate anything, except message number [-2]
	# that changes what the very lasst line is, nothing more (7 has a last line [s/c])

	# get status information
	status = [data[0][0].replace('/','5')]+data[0][3:].replace('/','0').split()[:-1] # none of the actual binary status infromation
	status = status + [data[1][0:3].replace('/','9')] + data[1][7:-11].replace('/','9').split()
	status = np.array(status,dtype=np.float32)
	
	prof = data[2:17]#.strip().replace("\n",'').replace("\r","")
	values = np.zeros(250,dtype=np.float32)
	index = 0
	for l in prof:
		# the line is HHHD0D1D2D3D4...
		l=l.strip()
		#FIXME - check for high values!!
		for i in xrange(3,len(l),4):
			val = l[i:i+4]
			if val[0] == 'F' or val == '0000':
				values[index]= 1
			else:
				values[index] = int(val,16)
			index += 1
	values = values/SCALING_FACTOR # remove the scaling factor...
	out = {'height':np.arange(0,7500,30),'bs':np.log10(values),'status':status} # yes, 30 m resolution! how terrible!
	return out


