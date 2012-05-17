"""
Read  a ct12k observation - this is almost a copy of the ceil2ff function doing the same thing.
"""

import numpy as np

def read(ob):
	dls = ob.split("\n") # data lines
	dl = []
	if len(dls) < 15 or ":" in ob:
		return False

	# purify the ob so that i dont have to care about formatting
	for l in dls:
		if len(l.strip()) > 3:
			# then i guess there is content
			dl.append(l) #NOT STRIP!!
	# ok, let's hope that is good
	del dls	

	# hold extra header information
	cld = 'CT12'+dl[1].strip()+dl[2].strip()
	text = "" # holds the strings
	
	cl = dl[0].strip()
	status = [
	cl[0:1],
	cl[4:9],
	cl[10:15],
	cl[16:21],
	cl[22:27]
	] + [x for x in cl[28:39]]
	il = dl[1].strip()
	status += [
	il[0:1],
	il[2:3],
	il[4:8],
	il[9:12],
	il[13:16],
	il[17:20],
	il[21:25],
	il[26:31],
	il[32:34],
	il[35:37],
	]
	# this could be slow, but whatever
	status = np.fromstring('|'.join(status).replace("/",'0').replace('*','9'),sep="|")
	values = np.zeros((250),dtype=np.float32) # 250 is a permitted size at this time, and is exact.

	# the first values are heights of the beginning of the row...
	string = ob[len(dl[0]) + len(dl[1]) + 2:].replace(' ','0').replace("\n","").replace("\r","").strip() #faster?
	index = 0
	for i in xrange(2,len(string[2:])+1,2):
		if i%42 == 0: continue # height indices
		val = (int(string[i:i+2],16)-1)/50. # compute the SS value...
		values[index] = val
		index +=1 

	out = {'height':np.arange(0,3750,15),'bs':np.exp(values),'status':status} # 15 m vertical resolution is the only reportable form!

	del values,il,cl,status,dl

	return out


