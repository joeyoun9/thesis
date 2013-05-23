'''
Joe Young August 2012
'''
import numpy as np
import math
import cleanfig as cf


# default conversions dictionary, seconds per whole unit of whatever we are talking about, user modifyable if re-passed to the function
default_time_conversions = {
    'tc' : 1000,
    'tf' : 800,
    'rh' : 900,
}

def skew (temp, pres, rate=.005):
    # return temp + (1000-pres)*.05
    dz = 5740.*np.log(1000 / pres)
    return temp + rate * dz

def skewz (temp, z, rate=.005):
    return temp + rate * z

def c2t (t, v, var, conversions=default_time_conversions, z=False, offset=False, colorbar_degrees=10, skew_distance=15):
    '''
    Convert a profile of temperatures in celcius   
    
    Parameters
    ----------
    t: int
        the time of the sounding
    v: list
        the values of the profile, either T,TD or RH (not recommended)
    var: str
        the type of the provided variable, as a valid key of conversions
    conversions: dict, optional
        Tell how many seconds correspond to one unit change for various variables
    z: list, optional
        elevation information
    offset: float/list, optional
        provide a baseline value so that both temp/dewp lines are not right on top of eachother.
        Example
        -------
        >>> temp = c2t(t,tempdata,var)
        >>> dewpoint = c2t(t,dewpointdata,var,offset=tempdata)
    Other parameters deprecated.
    
    
    '''
    if not z.any():
        skewz = lambda x, y: x  # create skewz as a meaningless function
        z = [0 for x in range(len(v))]  # create a dummy Z
    else:
        skewz = lambda x, y: x + .005 * y

    if offset:
        # the offset will be an amount in the unit of v, and shows how much we should adjust time
        # OR offset can be a list, in which case, the offset value will be the distance between the point[0] on that list
        if type(offset) == list:
            offset = v[0] - offset[0]
        t += offset * conversions[var]
    prof = []
    v0 = skewz(v[0], z[0])  # the first temperature = the first time, t
    for k, val in enumerate(v):
        dt = (skewz(val, z[k]) - v0) * conversions[var]  # now we know the dt to be used
        prof.append(t + dt)

    # provide a colorbar dataset!

    # and create skew lines!!
    # # colorbar is simply colorbar_degrees away from the core axis
    # prof is now a profile of times valued to the values specified
    return prof

# prof_height is a function which will take a profile, and will return the point above and/or below a certian elevation
def prof_height (v, z, length=99999., bottom=0.):
    # self is the request obj, v is the variable profile, and z are the corresponding heights AMSL
    prof = []
    prof_z = []
    prof_zreal = []
    for k, v in enumerate(v):
        if z[k] - bottom < length and z[k] >= bottom:
            prof.append(v)
            prof_z.append(z[k] - bottom)
            prof_zreal.append(z[k])
    return prof, prof_z, prof_zreal

def rh2td(t, rh, kc):
    # use the more accurate approximation
    # TEMP IN K
    if kc == "k":
        td = 17.271 * t / (237.7 + t) + np.log(rh / 100)
    else:
        td = t - (100. - rh) / 5.
    return td

def sounding_dewpoint(t, rh):
    # calculates and returns kelvin dew point temperature
    # for given temperature [k] and rh [%]
    # philosophy: rh = e/es. now, e depends on the temperature, as does es
    # basically, at hella cold temperatures, L = something else
    # FIXME replace math objects with np objects
    R = 286.9
    P0 = 6.112
    T0 = 273.15
    L = 2260000 if t > 274 else 2260000  # + 334000
    if t < 271:
        e = (rh / 100) * (6.112 * math.exp((L / R) * ((1 / T0) - (1 / t))))
        td = (T0 ** -1 - (R / L) * math.log(e / P0)) ** -1
    else:
        e = (rh / 100) * (6.112 * math.exp((L / R) * ((1 / T0) - (1 / t))))
        # td = (  T0**-1 - (R / L) * math.log(e / P0) )**-1
        td = (243.5 * math.log(e / 6.112)) / (17.67 - math.log(e / 6.112)) + 273.15

    # td can be found by rearranging the clausius-clapeyron equation
    return td

def e_calc(t, rh):
    pass
    # this will use an iterative method of solving for e (vapor pressure)
    # at the given temperature basically the same as the dewpoint, but using
    # iterative forms of the clasius-clapeyron equation... eventually!


def c2f(t):
    return 1.8 * t + 32

def f2c(t):
    return (t - 32) / 1.8


def moist_adiabat (tmp, pres, kc):
    # this is a wallace and hobbs approximation:
    if kc == "k":
        t = tmp
    else:
        t = tmp + 273.15
    lv = 2500000.
    cp = 1004.
    td = dry_adiabat(t, pres, 'k')
    te = td * np.exp(lv * ws(t, pres) / cp * t)
    print t, pres, es(t), ws(t, pres), lv * ws(t, pres) / cp * t
    return te




def dry_adiabat (temp, pres, kc):
    # temp in K!!
    if kc == "k":
        t = temp
    else:
        t = temp + 273.15
    tda = t * (np.power(pres / 1000., 2. / 7.))
    return tda




def virt (t, RH, p):
    # sadly this has to be calculated from td, because i have no real good way of calculating td from RH
    tv = t / (1 - ((RH * es(t)) / (100 * p)) * (1 - 0.622))
    return tv

def e(t):
    '''
        saturation compute vapor pressure using a multidimensional t, and the emperical calc.
    '''
    A = 2.53e11  # pa
    B = 5420  # K

    return A * np.exp(-B / t)  #T IN K!!!

def theta(t, p):
    't in K, p in hPa, returns in K'
    return t * (1000 / p) ** (.286)


def thetae(t, p):
    't in K, p in hPa, returns K'
    ev = e(t)
    rc = 0.622 * ev / (p * 100 - ev)
    l = 2.5e6
    cp = 1004
    return theta(t, p) * np.exp((l * rc) / (cp * t))

def _z(p):
    '''
     Compute z as a function of p (NOT T) in hPa
     
     This uses an absolute reference temperature of 0C
     to compute an absolute reference Z for any pressure. This is needed
     for plotting background values on soundings, which require a direct and
     persistent conversion between P and Z. This should not be used elsewhere.
    '''
    return (287. / 9.81) * 273.15 * np.log(1000 / p)

def plot_skewt(plt, t, td, p, skew=.006):
    """
    Create the contours for a skew-T plot, and plot them
    """
    "initialize the contouring background variables, not too inefficient"
    ts = np.arange(-100, 200, 1.5)  # temps (200)
    ps = np.arange(1100, 0, -1)  # pressures[1100]
    dp = np.zeros((1100, 200))
    "Compute initial value matrices"
    pss = (dp.T + ps).T  # full gridded pressure information
    tss = dp + ts  # get temperature on the pressure grid
    zss = _z(pss)
    "Compute special variables"
    thet = theta(tss + 273.15, pss) - 273.15  # ((tss+273.15)*(1000/pss)**(.286)) - 273.15
    thte = thetae(tss + 273.15, pss) - 273.15  # (theta+273.15)*np.exp((l*rc)/(cp*(tss+273.15))) - 273.15
    "Compute theta e contouring levels to align with indexes"
    televels = []
    for tr in range(-100, 100, 5):
        'tr is the temperature at 1000mb, so calculate @e there to determine plotting level'
        val = thetae(tr + 273.15, 1000) - 273.15
        televels.append(val)
    "Perform skewing of the computed arrays"
    thet = thet - skew * zss
    thte = thte - skew * zss
    tss = tss - skew * zss

    t = t + skew * (287. / 9.81) * 273.15 * np.log(1000 / p)
    td = td + skew * (287. / 9.81) * 273.15 * np.log(1000 / p)

    # write the function using the 0c calculation for height, and then skew the data!!

    cs = plt.contour(ts, ps, tss, levels=range(-100, 100, 5), colors='b', linewidths=0.5, linestyles='solid')
    csp = plt.contour(ts, ps, pss, levels=range(1000, 100, -100), colors='k', linewidths=0.5, linestyles='solid')
    te = plt.contour(ts, ps, thte, levels=televels, colors='g', linewidths=0.5, linestyles='solid')
    cst = plt.contour(ts, ps, thet, levels=range(-100, 100, 5), colors='r', linewidths=0.5, linestyles='solid')

    # plt.clabel(te,fontsize=5,inline=True)
    ax = plt.gca()
    ax.set_yscale('log')
    plt.plot(td, p, 'g', linewidth=2)
    plt.plot(t, p, 'r', linewidth=2)
    plt.ylim(p[0], p[-1])

    plt.yticks(range(1000, 100, 10), range(1000, 100, 10))

    "adjust the tempreature ticks to account for the 'lifted' surface in the sounding"
    cf.customTick(ax, 'x', np.arange(-100, 100, 10) + skew * z(p[0]), range(-100, 100, 10),)
    # plt.ylim(1000,10)
    plt.xlim(min(td) - 1, max(t) + 6)
    # plt.xlim(-50,110)
    "and that should do it."
