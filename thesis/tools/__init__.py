"""
Tools for checking times and whatont
"""
import calendar,time

def s2t(string,time_format):
	return calendar.timegm(time.strptime(string,time_format))
	# better specify UTC if you want to make sure it makes the right choice!!!

