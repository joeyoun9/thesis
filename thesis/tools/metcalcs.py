import numpy as np

__all__ = ['ws', 'es']


def ws (t, pres):
    'Compute saturation mixing ratio at any temperature and pressure of Earth air'
    pres = pres * 100.  # expect entry of hPa - convert to pa because that is the unit es returns
    return 0.622 * (es(t) / (pres - es(t)))

def es (t):
    '''
    Calculate saturation vapor pressure for any temperature in dry air (earth).
    
    Parameters
    ----------
    t: float
        temperature in KELVIN.
    '''
    es0 = 6.11  # Pa
    t0 = 273.15
    l = 2500000.  # J/whatever kg m^2 blah
    rv = 461.5
    return es0 * np.exp((l / rv) * ((1. / t0) - (1. / t)))
