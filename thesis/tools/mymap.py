"""
	UTM Digital Elevation Model working tools, for determining points, blending datasets, and making grids
"""

from math import *
import numpy as np

def ll2utm(lat, lon, zone=False):
	"""
		convert a lat lon in decimal to cartesina UTM in meters
	"""
	if not zone:
		zone = find_zone(lon)

	# CALCULATION USES RADIANS AND KILOMTERS
	# the N0 value is hemisphere specific, so figure that out, ace
	if lat >= 0:
		N0 = 0
	else:
		N0 = 10000 #(km)
	lat = radians(lat)
	lon = radians(lon)
	E0  = 500 #km
	k0 = 0.9996
	a = 6378.137 #km earth radius
	e = 0.0818192 # earth eccentricity - NOT TO BE CONFUSED WITH 2.982... e, 
	_A = A(lat,lon,zone,e)
	_T = T(lat,e)
	_C = C(lat,e)
	_s = s(lat,e)
	_v = v(lat,e)
	
	x = E0 + k0*a*_v*(_A+(1 - _T + _C)*(pow(_A,3)/6) + (5 - 18*_T + _T*_T)*(pow(_A,5)/120))
	y = N0 + k0*a*(_s+_v*tan(lat)*(_A*_A/2 + (5 - _T + 9*_C + 4*_C*_C)*pow(_A,4)/24 + (61 - 58*_T + _T*_T)*pow(_A,6)/720))
	return x*1000,y*1000
	

# defining several functions needed

def v(lat,ec):
	return 1/sqrt(1-pow(ec,2)*pow(sin(lat),2))
def A(lat,lon,zone,ec):
	lon0 = radians(zone * 6 - 180 - 3)
	#print degrees(lon),degrees(lon0) # just confuses me when it prints
	return (lon - lon0)* cos(lat)
def s(lat,ec):
	a = (1 - pow(ec,2)/4 - 3 * pow(ec,4)/64 - 5 * pow(ec,6)/256) * lat
	b = (3*pow(ec,2)/8 + 3 * pow(ec,4)/32 + 45*pow(ec,6)/1024)*sin(2*lat)
	c = (15*pow(ec,4)/256 + 45*pow(ec,6)/1024) * sin(4*lat)
	d = 35*pow(ec,6)*sin(6*lat) / 3072
	return a - b + c - d
def T(lat,ec):
	return pow(tan(lat),2)
def C(lat,ec):
	return pow(ec,2)*pow(cos(lat),2) / (1- pow(ec,2))

def find_zone(lon):
	"""
		a SEMI functional UTM zone finding tool (does not account for things like where Norway pulls a fast one)
	"""
	# number of zones is 60, atarting at 01 with -180 to 60 at <= 180 WARNING - MORE COMPLEX IN NORTHERN EUROPE!!
	v = lon+180 # now we are calculating from 0 - 360
	for z in range(1,61):
		if v <= z*(360/60):
			zone = z
			break
	print "Identified as zone",zone
	return zone

def gridsub(x1,y1,d1,x2,y2,d2):
	"""
		replace values on grid 1 with values from grid 2 where they line up and are not nan
		
	"""
	#FIXME try this with numpy - where the indices are the same?
	
	# start by determining where they overlap, by seeing where the x begins and ends in both
	# then loop through those areas, and check and replace if found
	hrange = [x2[0],x2[-1]]
	vrange = [y2[-1],y2[0]]
	# DETERMINE THE CORRESPONDING COORDINATES FOR EACH GRID TO EACH GRID
	# find x start for d1 and d2
	# REQUIRES A PERFECT GRID IN BOTH!!!
	x1s = -1
	x2s = False
	for x in range(len(x1)):
		if x1[x] == hrange[0]:
			x1s = x
			x2s = 0 # presumably this means the start is here
			break
	if x1s < 0:
		# well, then it appears that x1s is off the edge of the map, so, find the corresponding
		print " initial x dimension is off the map"
		for x in range(len(x2)):
			if x2[x] == x1[0]: # if it equals the lowest value of x1:
				x1s = 0
				x2s = x
	if x1s < 0:
		print "Um, d2 is not located within d1, sorry"
		return d1 # fail nice
	
	# now the same for y
	y1s = -1
	y2s = False
	for x in range(len(y1)):
		if y1[x] == vrange[1]:
			y1s = x
			y2s = 0 # presumably this means the start is here
			break
	if y1s < 0:
		# well, then it appears that x1s is off the edge of the map, so, find the corresponding
		print " initial y dimension is off the map"
		for x in range(len(y2)):
			if y2[x] == y1[-1]: # if it equals the lowest value of y1:
				y1s = 0
				y2s = x
	if y1s < 0:
		print "Um, d2 is not located within d1, sorry"
		return d1 #fail nice

	# well, now we know where to start, so let's go!
	print "starting points: ",x1s,y1s,x2s,y2s
	y2k = y2s
	for y in range(y1s,len(y1)):
		x2k = x2s
		y2k += 1
		# but we still have to check for termination
		if y2k >= len(y2):
			# then we are beyond the end, break (below the lowest value)
			break
		for x in range(x1s, len(x1)):
			# x and y should now be the values of d1 to replace
			x2k += 1
			if x2k >= len(x2):
				break
			if not np.isnan(d2[y2k,x2k]):
				# woohoo, a value! - set the initial value to this
				d1[y,x] = d2[y2k,x2k]
	return d1

def salt_lake_map():
	'''
	Creates and returns a map object which is tuned to a good map
	of the Salt Lake Valley. Takes no inputs
	'''
	from mpl_toolkits.basemap import  Basemap
	'Yes, yes, that is against the rules... '
	m=Basemap(width=45000,height=40000,resolution='l',
                projection='eqdc',lat_1=40.4,lat_2=40.8,
                lat_0=40.6,lon_0=-111.95) 
	return m
	

def lincross(x0,y0,x1,y1,x,y,d):
	"""
		return a linear cross section of heights between the two points,
		two lists are returned, the values, and the points along the longer axis
	
		start is a tuple (x,y) of the starting point, and end is the same for the end
		d is the gridded dataset for the elevations 
	"""
	out = []

	# first determine the nearest actual coordinates with rounding
	x0 = findkey(x0,x)
	y0 = findkey(y0,y)
	x1 = findkey(x1,x)
	y1 = findkey(y1,y)
	# now calculate the distance traveled in each direction, to get both the equation for the slope
	# and so i can know which is the traversing direction, and which is the searching direction
	dx = x1 - x0
	dy = y1 - y0
	print x0,x1,y0,y1
	#FIXME - if dx or dy are 0, then we may have a problem? 
	if dx > dy:
		# direction = x
		slim = [x0,x1]
		search = x
		traverse = y
		mult = dy/dx #dy/dx
		add = y0 
		func = _dvalx
	else:
		# direction = y
		slim = [y0,y1]
		search = y
		traverse = x
		mult = dx/dy #dx/dy
		add = x0
		func = _dvaly
	# define the equation to find the instantaneous value along the traversing direction

	# loop, calculate, and round to get the nearest point in the traversing direction
	ds = -1 # for calculating the point
	for s in range(len(search)):
		if s < slim[0] or s > slim[1]:
			continue
		# now we are within the limit
		ds += 1
		t = int(round(add + mult * ds)) # finding the nearest point by rounding
		out.append(func(t,s,d))
		
	return out
	

# these two functions are simply for internal use
# a function needed to be named
def _dvalx(v1,v2,d):
	return d[v1,v2]
def _dvaly(v1,v2,d):
	return d[v2,v1]

def findkey(v,l):
	# a simple function to find the key, however this also finds the closest key
	inc = True
	if (l[0] > l[1]):
		inc = False
	for k in range(len(l)):
		kv = l[k]
		if kv == v:
			# well great! then we just return l
			return k
		# but, it is never that simple
		# check directionality, if descending, use
		if kv > v and inc:
			# then determine which is closer, kv, or l[k-1]
			if k == 0: 
				return 0
			else:
				# now calculate the difference between
				if v - kv > v - l[k-1]:
					return k-1
				else:
					return k
		elif kv < v and not inc:
			# then determine which is closer, kv, or l[k-1]
			if k == 0: 
				return 0
			else:
				# now calculate the difference between
				if v - kv > v - l[k-1]:
					return k-1
				else:
					return k

