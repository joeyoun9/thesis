'''
The pcaps directory provides access to temporal objects pf specificed events. 

'''
__all__ = [
           'iop',
           'shade_iops',
           'cap_times',
           'pm_times',
           'shade_caps',
           'pcaps_timeticks',
           'events',
           'aerosol_periods',
           'virga_periods',
           'light_aerosol_periods',
           ]

from thesis.tools import s2t
import logging as l
from thesis.tools.core.objects import CoreObject
from thesis.tools.bundle import srcs, runmean
import time
from datetime import datetime
import numpy as np
import cleanfig as cf

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
    if num == 'all':
        return out[1:]
    if not buffer:
        return out[num]
    else:
        out = list(out[num])
        out[0] = out[0] - 86400 * buffer
        out[1] = out[1] + 86400 * buffer
        return out



def shade_iops(color='#FFCC00', plt=None, ax=None, text=True, alpha=.3, zorder=0):
    '''
    for a plot where time is the x axis, add shaded bars where IOPs are occuring.
    This is meant to be used with xlim and ylim defined, it will not make those decisions
    '''
    if not plt and not ax:
        l.warning('IOP shading not done, no plt or ax specified')
        return False
    if plt:
        ax = plt.gca()
    # add a plot showing IOPs
    i = 0
    lims = ax.get_ylim()

    for d in iop('all'):
        i += 1
        ax.fill([d[0], d[0], d[1], d[1]], [lims[0], lims[1], lims[1], lims[0]],
                 color, alpha=alpha, ec=color, zorder=zorder)
        if text:
            pad = (lims[1] - lims[0]) * .015
            ax.text(sum(d) / 2., lims[1] - pad, str(i), ha='center', va='top')
    return True

def cap_times(threshold=4.04):
    '''
    Where deficit.deficit > 4.04 for more than 3 soundings, go (+- 6 hours)
    '''
    deficit = CoreObject(srcs.pcaps.proc.heatdeficit).slice(iop(0))

    # identify all points below the threshold
    points = deficit.deficit <= threshold
    points[0] = True  # this corrects if the series starts above the threshold
    keys = np.arange(len(points))[points]
    # compute the gradient of these keys
    kd = np.diff(keys)
    # whatever values of keys correspond to points where kd >= 3, are golden!
    startkeys = keys[kd >= 3]
    kds = kd[kd >= 3]  # we will want this to print the end keys
    for skey in startkeys:
        # loop throught starting time keys
        ekey = keys[keys > skey][0]
        yield [deficit.time[skey] - 3600 * 6., deficit.time[ekey] + 3600 * 6.]
        # yeilding a list so I can modify it later

def pm_times(threshold=20, smooth=24):
    '''
    Where PM10 > 20, return these times
    '''
    pm = CoreObject(srcs.pcaps.daq.pm10co).slice(iop(0))

    # identify all points below the threshold
    points = runmean(pm.pm10, smooth) < threshold
    points[0] = True  # this corrects if the series starts above the threshold
    keys = np.arange(len(points))[points]
    # compute the gradient of these keys
    kd = np.diff(keys)
    # whatever values of keys correspond to points where kd >= 3, are golden!
    startkeys = keys[kd >= 3]
    kds = kd[kd >= 3]  # we will want this to print the end keys
    for skey in startkeys:
        # loop throught starting time keys
        ekey = keys[keys > skey][0]
        yield [pm.time[skey], pm.time[ekey]]
        # yeilding a list so I can modify it later

def shade_caps(threshold=4.04, color='#FFCC00', ec='#FFCC00', plt=None, ax=None, text=True, alpha=.3, zorder=0):
    '''
    for a plot where time is the x axis, add shaded bars where IOPs are occuring.
    This is meant to be used with xlim and ylim defined, it will not make those decisions
    '''
    if not plt and not ax:
        l.warning('IOP shading not done, no plt or ax specified')
        return False
    if plt:
        ax = plt.gca()
    # add a plot showing IOPs
    i = 0
    lims = ax.get_ylim()
    buff = 6 * 3600  # for now
    for d in cap_times(threshold):
        i += 1
        d[0] = d[0] + buff
        d[1] = d[1] - buff
        ax.fill([d[0], d[0], d[1], d[1]], [lims[0], lims[1], lims[1], lims[0]],
                 color, alpha=alpha, ec=color, zorder=zorder)
        if text:
            pad = (lims[1] - lims[0]) * .015
            ax.text(sum(d) / 2., lims[1] - pad, str(i), ha='center', va='top')
    return True

def pcaps_timeticks(plt, notext=False):
    '''
    this will print properly formatted timeticks for the entire PCAPS period
    on a figure about the long length of a page. 
    
    s2t assumes utc...
    '''
    locations = [
                 s2t(2010120112),
                 s2t(2010121512),
                 s2t(2010123112),
                 s2t(2011011512),
                 # s2t(2011020112),
                 s2t(2011020712)]
    labels = [''] * 5
    i = 0
    if not notext:
        for loc in locations:
            labels[i] = datetime.fromtimestamp(loc).strftime("%d %b %Y")

            i += 1
        # label the axis
        plt.xlabel('Date')
    ax = plt.gca()
    ax.set_xticks(locations)
    ax.set_xticklabels(labels)
    # minor ticks, one per day!
    minorT = []
    i = locations[0]
    while i <= locations[-1]:
        minorT += [i]
        i += 86400
    ax.set_xticks(minorT, minor=True)

# make a simple dict available for other events
events = {
    'pcaps':(s2t(2010120112), s2t(2011020712)),
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
