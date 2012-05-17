"""
Tools for checking times and whatont
"""
import calendar,time
from datetime import timedelta,datetime

def s2t(string,time_format):
	return calendar.timegm(time.strptime(string,time_format))
	# better specify UTC if you want to make sure it makes the right choice!!!

def matlabtime(t):
	"""
		create a unix time from a matlab ordinal time
	"""
	print t
	dt = datetime.fromordinal(int(t))+timedelta(days=t%1) - timedelta(days=366) 
	# well, that's close...
	return calendar.timegm(dt.timetuple()) #woohoo?
	
