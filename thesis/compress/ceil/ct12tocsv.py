#!/usr/bin/env python
"""
An all in one package for reading and producing two CSV files from CT12 data

DeWekker formatted timestamps.

This is coded to read whatever file is passed to it in the form of ./ct12tocsv.py [raw_file_path]
and will save raw_file_path.backscatter.csv and raw_file_path.status.csv 

"""


'1. Set some important parameters'
READ_CHUNK = 100000
'specify how many bytes to read at a single time, the larger the number, the faster, but the more memory required'
SAVE_POWER = True
'the backscatter data recorded should be power. set false to save DD'
PRINT_HEADER=True
'Should an informative header be inserted into the output CSV file?'



'2. import the python numerical/mathematical package numpy for fast efficient array structures'
import numpy as np
'also import the system package/namespace, which gives access to provided command line arguments'
import sys,calendar,time




'3. Create/Use the read function for translating any individual observation to understandable lists of data'
def read(ob,savepower=True):
	'split the data by line, and create a list called dls with each element being one line'
	dls = ob.split("\n")
	'initialize a blank simple list to hold the corrected lines array'
	dl = []
	'check if the received ob is long enough, if not, then skip, this ob is not formatted right...'
	if len(dls) < 15 or ":" in ob:
		return False
	'To catch all possibilities, fill the dl list with all the lines greater than 3 characters'
	for l in dls:
		if len(l.strip()) > 3:
			'the line appears to be long enough, so append it to our holder list,'
			dl.append(l) 
	'now dl has replaced dls as the data lines variable, so remove the old one'
	del dls	
	'Now read the status information lines, dl[0] and dl[1] for cloud info, gain, temp, etc'
	'''
	This is done by knowing the points in each line for each inidividual relevant piece of 
	status information. This can be found in the data message reading guide.
	'''
	cl = dl[0].strip()
	il = dl[1].strip()
	status = [cl[0:1],cl[4:9],cl[10:15],cl[16:21],cl[22:27]] + [x for x in cl[28:39]]
	status += [il[0:1],il[2:3],il[4:8],il[9:12],il[13:16],il[17:20],il[21:25],il[26:31],
	il[32:34],il[35:37],]
	'''
	Then run a quick process that turns this list back into a string, pipe (|) separated, then replace
	some of the overflow/ASOS codes ////, ** with 0's or 9's respectively.
	
	This also creates an efficient numpy array of the values, as a list of floating point numbers
	'''
	status = np.fromstring('|'.join(status).replace("/",'0').replace('*','9'),sep="|")
	'Create a numpy array to hold the backscattered power values, there are 250 range bins in a profile'
	values = np.zeros((250),dtype=np.float32)
	'Convert the 15 lines of data into one line, and replace spaces with 0s so the splitting works better'
	string = ob[len(dl[0]) + len(dl[1]) + 2:].replace(' ','0').replace("\n","").replace("\r","").strip()
	'create an index to keep track of which bin we are in'
	index = 0
	'''
	Loop through this backscatter string jumping every two characters. 
	Noting that every 42nd character is a height index, and therefore should be skipped.
	
	First, simply the DD value is saved, for computational efficiency. Once the profile is read
	the power is computed from the list of values in a more efficient manner (showing the power of numpy).
	'''
	for i in xrange(2,len(string[2:])+1,2):
		if i%42 == 0: continue
		'Translate the hexidecimal string to an integer using the hex int function int(x,16)'
		val = int(string[i:i+2],16)
		values[index] = val
		index +=1 
	'derive the gain value from the status lines before, and the manual, gain = 0 or 2, so let it pick as the index'
	gain = [250.,0,930.][int(status[-10])]
	if savepower:
		'now use the formula to make a vector calculation for power over the entire length'
		values = np.exp((values-1)/50)*0.188/gain

	'simply return the two arrays, since the outside function knows everything else'
	return values,status

def s2t(string,time_format):
	'''
	Convert a textual string time representation to a unix epoch time using the standard time format string
	provided. Identical to
	
		>>> calendar.timegm(time.strptime(string,time_format) 
		
	Parameters
	----------
	string: str
		a time stamp of whatever format, as long as it is information that can be interpreted by the 
		time.strptime() function
		
	
	
	Note
	----
	Specify UTC in the string, and %Z in the format to ensure the data is properly 
	interpreted as UTC/GMT
	'''
	return calendar.timegm(time.strptime(string,time_format))


'3. Now that the fuctions exist, all we have to do is read the file, find the obs, and save them'
'check for a file provided in the arguments'

if len(sys.argv)<2:
	raise ValueError('You must provide an argument.')
'grab the source file from the terminal arguments'
source = sys.argv[1]

print 'reading',source

'open the file for reading'
readhandle = open(source,'r')
'open the two output files for writing, meaning we OVERWRITE AND CLEAR these files.'
bshandle = open(source+'.backscatter.csv','w')
sthandle = open(source+'.status.csv','w')
'write headers, if we are supposed to'
if PRINT_HEADER:
	'backscatter hedaer is simply time and then heights in meters'
	bsh = 'time,'+','.join(map(str,range(0,3750,15)))
	sth = 'time,cld#,layer 1,bs range 1,layer 2,bs range 2, hardware alarm,'
	sth+='supply voltage alarm, laser power low, temperature alarm,solar shutter on,'
	sth+='blower on, heater on,cloud report unit, normalization, fast heater, gain,'
	sth+='laser pulse frequency,noise RMS,bs sum,internal, laser power, transmitter temp,'
	sth+='zero offset, internal, extinction coefficient'
	bshandle.write(bsh+'\n')
	sthandle.write(sth+'\n')

'define variables for control structures, these are non printing unichar characters'
B = unichr(002) 
C = unichr(003)
'begin a controlled infinite loop to read the file in chunks, the lazy way'
while True:
	'read a single chunk, and anvance the pointer that amount, and split by ob controller'
	data = readhandle.read(READ_CHUNK)
	'if nothing was returned, then the file is done, and we must break the infinite loop'
	if not data:
		break
	data = data.split(B)
	for ob in data:
		'grab the time by splitting by the second control, taking the end value, and stripping whitespace'
		tmstring = ob.split(C)[-1].strip()
		'now translate the time, and wrap in a try statement, to catch bad times = bad obs'
		try:
			tm = s2t(tmstring[:2]+tmstring[4:-4]+'UTC','%m/%d/%Y %H:%M:%S%Z')
			'Note, this will fail in 2100, assumes 012 == 2012 (only uses 2 digit year)'
		except:
			'the time was not in the right format, so it was probably garbage, next ob please.'
			continue
		'now grab just the observation text'
		try:
			out = read(ob.split(C)[0].strip(),SAVE_POWER)
		except:
			'again, failed to read, = bad ob'
			print 'ob read failed.'
			continue
		if not out:
			continue
		'if we made it to this point, the ob has been read successfully! So, now just save it'
		print 'ob:',time.ctime(tm)
		
		'Now we will write this to the file, using join and map to convert values to strings'
		bs = ','.join(map(str,out[0]))
		st = ','.join(map(str,out[1]))
		
		bshandle.write(str(tm)+','+bs+'\n')
		sthandle.write(str(tm)+','+st+'\n')
		
print 'reading complete.'
		
	

'and close everything'
readhandle.close()
bshandle.close()
sthandle.close()



