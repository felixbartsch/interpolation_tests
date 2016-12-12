import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt


def corr_no_interpolation(y1,y2, window_interest):
    corr = np.absolute(np.correlate(y1[0,:], y2[0,:], "full"))
    delay = np.argmax(corr)
    return corr, delay


def corr_pre_interpolation(y1,y2, window_interest):
    x1 = np.linspace(0,len(y1[0,:]),len(y1[0,:]))
    f1 = interpolate.interp1d(x1, y1)
    x1_interpolated = np.linspace(0,len(y1[0,:]),len(y1[0,:]) * 10)
    y1 = f1(x1_interpolated)
    x2 = np.linspace(0,len(y2[0,:]),len(y2[0,:]))
    f2 = interpolate.interp1d(x2, y2)
    x2_interpolated = np.linspace(0,len(y2[0,:]),len(y2[0,:]) * 10)
    y2 = f2(x2_interpolated)
    corr, delay = corr_no_interpolation(y1,y2, window_interest)
    #window_interp = np.arange(delay-window_interest*10,delay+window_interest*10)
    return corr, float(delay)/10
    
    
def corr_spline_interpolation(y1,y2, window_interest):
    corr, delay = corr_no_interpolation(y1,y2, window_interest)
    if window_interest%2!=0:
        window_interp = np.arange(delay-(window_interest-1)/2,delay+(window_interest-1)/2)
        xnew = np.arange(delay-((window_interest-1)/2),delay+(window_interest-1)/2, 0.0001)
    else:
        window_interp = np.arange(delay-(window_interest)/2,delay+(window_interest)/2-1)
        xnew = np.arange(delay-((window_interest)/2),delay+(window_interest)/2-1, 0.0001)
    tck = interpolate.splrep(window_interp, corr[window_interp], s=0, k=4)
    dspl = interpolate.splder(tck)
    corr = interpolate.splev(xnew, tck, der=0)
    delay_spl = interpolate.sproot(dspl, mest = 20)
    delay = delay_spl[np.argmax(interpolate.splev(delay_spl, tck, der=0))]
    return corr, delay
'''    
def corr_sinc_interpolation(y1,y2, window_interest):
    corr, delay = corr_no_interpolation(y1,y2, window_interest)
    window_interp = np.arange(delay-window_interest,delay+window_interest)
    return corr, delay
'''