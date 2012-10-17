"""
	Methods and data for the PCAPS projects
"""

all = ['ceilometer','summarize']

from thesis.tools import s2t

def iop(num,buffer=False):
	'''
	Select an IOP timetuple for the project defined iops. Available option to 
	buffer this tuple by buffer [days] on either end
	
	Parameters
	----------
	num:int
		reference to the IOP number from PCAPS
	buffer: float, optional
		length in days to extend the tuple.
	'''
	# organize events, and return proper interpretable time tuples
	if num == 0:
		out= (s2t('2010120112UTC','%Y%m%d%H%Z'),s2t('2011021800UTC','%Y%m%d%H%Z'))
	elif num == 1:
		out= (s2t('2010120112UTC','%Y%m%d%H%Z'),s2t('2010120702UTC','%Y%m%d%H%Z'))
	elif num == 2:
		out= (s2t('2010120712UTC','%Y%m%d%H%Z'),s2t('2010121015UTC','%Y%m%d%H%Z'))
	elif num == 3:
		out= (s2t('2010121212UTC','%Y%m%d%H%Z'),s2t('2010121421UTC','%Y%m%d%H%Z'))
	elif num == 4:
		out= (s2t('2010122400UTC','%Y%m%d%H%Z'),s2t('2010122621UTC','%Y%m%d%H%Z'))
	elif num == 5:
		out= (s2t('2011010100UTC','%Y%m%d%H%Z'),s2t('2011010912UTC','%Y%m%d%H%Z'))
	elif num == 6:
		out= (s2t('2011011112UTC','%Y%m%d%H%Z'),s2t('2011011720UTC','%Y%m%d%H%Z'))
	elif num == 7:
		out= (s2t('2011012012UTC','%Y%m%d%H%Z'),s2t('2011012206UTC','%Y%m%d%H%Z'))
	elif num == 8:
		out= (s2t('2011012312UTC','%Y%m%d%H%Z'),s2t('2011012612UTC','%Y%m%d%H%Z'))
	elif num == 9:
		out= (s2t('2011012612UTC','%Y%m%d%H%Z'),s2t('2011013106UTC','%Y%m%d%H%Z'))
	elif num == 10:
		out= (s2t('2011020218UTC','%Y%m%d%H%Z'),s2t('2011020518UTC','%Y%m%d%H%Z'))
	if not buffer:
		return out
	else:
		out = list(out)
		out[0] = out[0] - 86400*buffer
		out[1]=out[1] + 86400*buffer
		return out

# make a simple dict available for other events
events = {
	'pcaps':(s2t('2010120100UTC','%Y%m%d%H%Z'),s2t('2012021800UTC','%Y%m%d%H%Z')),
	'target1':(s2t('201012040000UTC','%Y%m%d%H%M%Z'),s2t('201012051200UTC','%Y%m%d%H%M%Z')),
	
	

}	
