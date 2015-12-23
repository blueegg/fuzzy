import numpy as np

def findvar(ret, alpha=0.05, nbins=100):
    # Function computes an empirical Value-at-Risk (VaR) for return-series
    #   (ret) defined as NumPy 1D array, given alpha
    # (c) 2015 QuantAtRisk.com, by Pawel Lachowicz
    #
    # compute a normalised histogram (\int H(x)dx = 1)
    #  nbins: number of bins used (recommended nbins>50)
    hist, bins = np.histogram(ret, bins=nbins, density=True)
    wd = np.diff(bins)
    # cumulative sum from -inf to +inf
    cumsum = np.cumsum(hist * wd)
    # find an area of H(x) for computing VaR
    crit = cumsum[cumsum <= alpha]
    n = len(crit)
    # (1-alpha)VaR
    VaR = bins[n]
    # supplementary data of the bar plot
    bardata = hist, n, wd
    return VaR, bardata

def findalpha(ret, thr=1, nbins=100):
    # Function computes the probablity P(X<thr)=alpha given threshold
    #   level (thr) and return-series (NumPy 1D array). X denotes the
    #   returns as a rv and nbins is number of bins used for histogram
    # (c) 2015 QuantAtRisk.com, by Pawel Lachowicz
    #
    # compute normalised histogram (\int H(x)dx=1)
    hist, bins = np.histogram(ret, bins=nbins, density=True)
    # compute a default histogram
    hist1, bins1 = np.histogram(ret, bins=nbins, density=False)
    wd = np.diff(bins1)
    x = np.where(bins1 < thr)
    y = np.where(hist1 != 0)
    z = list(set(x[0]).intersection(set(y[0])))
    crit = np.cumsum(hist[z]*wd[z])
    # find alpha
    try:
        alpha = crit[-1]
    except Exception as e:
        alpha = 0
    # count number of events falling into (-inft, thr] intervals
    nevents = np.sum(hist1[z])
    return alpha, nevents

def cpr(ret1, ret2, thr=0.05):
    # Function computes the conditional probabilities for rare events
    # (c) 2015 QuantAtRisk.com, by Pawel Lachowicz
    #
    nret1 = np.where(ret1 < 0, ret1, 1)
    nret2 = np.where(ret2 < 0, ret2, 1)
    #
    # compute the sets of events
    A = np.where(nret1 < 0, nret1, 1)
    A = np.where(A >= thr, A, 1)
    B = np.where(nret1 < thr, ret1, 1)
    R = np.where(nret2 < thr, ret2, 1)
    nA = float(len(A[A != 1]))
    nB = float(len(B[B != 1]))
    n = float(len(nret1[nret1 != 1]))  # n must equal to nA + nB
    # (optional)
    #print(nA, nB, n == (nA + nB))  # check, if True then proceed further
    #print(len(A), len(B), len(R))
    #
    # compute the probabilities
    pA = nA/n
    pB = nB/n
    #
    # compute the conditional probabilities
    pRA = np.sum(np.where(R+A < 0, 1, 0))/n
    pRB = np.sum(np.where(R+B < 0, 1, 0))/n
    #
    pR = pRA*pA + pRB*pB
    #
    if(pR>0):
        pBR = pRB*pB/pR
    else:
        # Pr(B|R) impossible to be determined. Pr(R)=0.
        pBR = 0 # should be np.nan, zero for plotting only
    #
    prob = pBR, pR
    return prob