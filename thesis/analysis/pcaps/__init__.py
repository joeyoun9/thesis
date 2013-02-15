'''
The pcaps directory provides access to temporal objects pf specificed events. 

'''
all = ['summarize']

from thesis.tools import s2t

def iop(num, buffer=False):
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
    out = [
        (s2t('2010 12 01 12 UTC', '%Y %m %d %H %Z'), s2t('2011 02 18 00 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 01 12 UTC', '%Y %m %d %H %Z'), s2t('2010 12 07 02 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 07 12 UTC', '%Y %m %d %H %Z'), s2t('2010 12 10 15 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 12 12 UTC', '%Y %m %d %H %Z'), s2t('2010 12 14 21 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 24 00 UTC', '%Y %m %d %H %Z'), s2t('2010 12 26 21 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 01 00 UTC', '%Y %m %d %H %Z'), s2t('2011 01 09 12 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 11 12 UTC', '%Y %m %d %H %Z'), s2t('2011 01 17 20 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 20 12 UTC', '%Y %m %d %H %Z'), s2t('2011 01 22 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 23 12 UTC', '%Y %m %d %H %Z'), s2t('2011 01 26 12 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 26 12 UTC', '%Y %m %d %H %Z'), s2t('2011 01 31 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 02 02 18 UTC', '%Y %m %d %H %Z'), s2t('2011 02 05 18 UTC', '%Y %m %d %H %Z')),
        ]
    if not buffer:
        return out[num]
    else:
        out = list(out[num])
        out[0] = out[0] - 86400 * buffer
        out[1] = out[1] + 86400 * buffer
        return out

# make a simple dict available for other events
events = {
    'pcaps':iop(0),
    'target1':(s2t('201012040000UTC', '%Y%m%d%H%M%Z'), s2t('201012051200UTC', '%Y%m%d%H%M%Z')),
    'target2':(s2t('201101050430UTC', '%Y%m%d%H%M%Z'), s2t('201101050800UTC', '%Y%m%d%H%M%Z')),  # WAVES!!!
    'target3':(s2t('201012020000UTC', '%Y%m%d%H%M%Z'), s2t('201012041200UTC', '%Y%m%d%H%M%Z')),  # wave breakup
}

aerosol_periods = [
        (s2t('2010 12 01 15 UTC', '%Y %m %d %H %Z'), s2t('2010 12 03 02 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 03 12 UTC', '%Y %m %d %H %Z'), s2t('2010 12 05 02 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 05 07 UTC', '%Y %m %d %H %Z'), s2t('2010 12 05 21 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 07 12 UTC', '%Y %m %d %H %Z'), s2t('2010 12 08 09 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 08 18 UTC', '%Y %m %d %H %Z'), s2t('2010 12 09 08 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 09 14 UTC', '%Y %m %d %H %Z'), s2t('2010 12 10 00 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 13 22 UTC', '%Y %m %d %H %Z'), s2t('2010 12 14 20 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 25 17 UTC', '%Y %m %d %H %Z'), s2t('2010 12 26 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 26 14 UTC', '%Y %m %d %H %Z'), s2t('2010 12 26 17 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 02 01 UTC', '%Y %m %d %H %Z'), s2t('2011 01 04 00 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 04 20 UTC', '%Y %m %d %H %Z'), s2t('2011 01 07 01 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 07 18 UTC', '%Y %m %d %H %Z'), s2t('2011 01 08 02 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 08 18 UTC', '%Y %m %d %H %Z'), s2t('2011 01 09 00 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 12 01 UTC', '%Y %m %d %H %Z'), s2t('2011 01 14 00 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 14 18 UTC', '%Y %m %d %H %Z'), s2t('2011 01 15 10 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 15 19 UTC', '%Y %m %d %H %Z'), s2t('2011 01 16 10 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 20 16 UTC', '%Y %m %d %H %Z'), s2t('2011 01 21 01 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 21 08 UTC', '%Y %m %d %H %Z'), s2t('2011 01 22 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 23 15 UTC', '%Y %m %d %H %Z'), s2t('2011 01 23 23 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 24 14 UTC', '%Y %m %d %H %Z'), s2t('2011 01 25 07 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 26 03 UTC', '%Y %m %d %H %Z'), s2t('2011 01 26 05 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 26 22 UTC', '%Y %m %d %H %Z'), s2t('2011 01 28 02 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 28 17 UTC', '%Y %m %d %H %Z'), s2t('2011 01 29 01 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 29 17 UTC', '%Y %m %d %H %Z'), s2t('2011 01 30 01 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 02 03 14 UTC', '%Y %m %d %H %Z'), s2t('2011 02 05 03 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 02 05 06 UTC', '%Y %m %d %H %Z'), s2t('2011 02 05 17 UTC', '%Y %m %d %H %Z')),
        ]
virga_periods = [
        (s2t('2010 12 03 06 UTC', '%Y %m %d %H %Z'), s2t('2010 12 03 10 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 05 02 UTC', '%Y %m %d %H %Z'), s2t('2010 12 05 07 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 09 09 UTC', '%Y %m %d %H %Z'), s2t('2010 12 09 12 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 10 00 UTC', '%Y %m %d %H %Z'), s2t('2010 12 10 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 04 00 UTC', '%Y %m %d %H %Z'), s2t('2011 01 04 20 UTC', '%Y %m %d %H %Z')),
        # This is the most interesting virga event
        (s2t('2011 01 08 22 UTC', '%Y %m %d %H %Z'), s2t('2011 01 09 06 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 14 00 UTC', '%Y %m %d %H %Z'), s2t('2011 01 14 17 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 15 11 UTC', '%Y %m %d %H %Z'), s2t('2011 01 15 17 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 20 13 UTC', '%Y %m %d %H %Z'), s2t('2011 01 20 16 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 25 08 UTC', '%Y %m %d %H %Z'), s2t('2011 01 26 02 UTC', '%Y %m %d %H %Z')),
        ]
'''
Light aerosol periods constitute times during IOP events where the aerosol concentration better
resembled a convectively mixing atmosphere.
'''
light_aerosol_periods = [
        (s2t('2010 12 08 09 UTC', '%Y %m %d %H %Z'), s2t('2010 12 08 17 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 10 07 UTC', '%Y %m %d %H %Z'), s2t('2010 12 10 13 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 12 14 UTC', '%Y %m %d %H %Z'), s2t('2010 12 13 22 UTC', '%Y %m %d %H %Z')),
        (s2t('2010 12 26 06 UTC', '%Y %m %d %H %Z'), s2t('2010 12 26 14 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 01 02 UTC', '%Y %m %d %H %Z'), s2t('2011 01 01 22 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 11 10 UTC', '%Y %m %d %H %Z'), s2t('2011 01 12 00 UTC', '%Y %m %d %H %Z')),
        # sarted before IOP Began
        (s2t('2011 01 21 01 UTC', '%Y %m %d %H %Z'), s2t('2011 01 21 07 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 01 23 12 UTC', '%Y %m %d %H %Z'), s2t('2011 01 24 13 UTC', '%Y %m %d %H %Z')),
        (s2t('2011 02 02 21 UTC', '%Y %m %d %H %Z'), s2t('2011 02 03 15 UTC', '%Y %m %d %H %Z')),
        ]
