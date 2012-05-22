"""
	Methods and data for the PCAPS projects
"""

all = ['compress','tools']

from thesis.tools import s2t

def iop(num):
	# organize events, and return proper interpretable time tuples
	if num == 1:
		return (s2t('2010120112UTC','%Y%m%d%H%Z'),s2t('2010120702UTC','%Y%m%d%H%Z'))
	elif num == 2:
		return (s2t('2010120712UTC','%Y%m%d%H%Z'),s2t('2010121015UTC','%Y%m%d%H%Z'))
	elif num == 3:
		return (s2t('2010121212UTC','%Y%m%d%H%Z'),s2t('2010121421UTC','%Y%m%d%H%Z'))
	elif num == 4:
		return (s2t('2010122400UTC','%Y%m%d%H%Z'),s2t('2010122621UTC','%Y%m%d%H%Z'))
	elif num == 5:
		return (s2t('2011010100UTC','%Y%m%d%H%Z'),s2t('2011010912UTC','%Y%m%d%H%Z'))
	elif num == 6:
		return (s2t('2011011112UTC','%Y%m%d%H%Z'),s2t('2011011720UTC','%Y%m%d%H%Z'))
	elif num == 7:
		return (s2t('2011012012UTC','%Y%m%d%H%Z'),s2t('2011012206UTC','%Y%m%d%H%Z'))
	elif num == 8:
		return (s2t('2011012312UTC','%Y%m%d%H%Z'),s2t('2011012612UTC','%Y%m%d%H%Z'))
	elif num == 9:
		return (s2t('2011012612UTC','%Y%m%d%H%Z'),s2t('2011013106UTC','%Y%m%d%H%Z'))
	elif num == 10:
		return (s2t('2011020218UTC','%Y%m%d%H%Z'),s2t('2011020518UTC','%Y%m%d%H%Z'))
	
