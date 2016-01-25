#!/usr/bin/env python

# Predicting Heavy and Extreme Losses in Real-Time for Portfolio Holders (2)
# (c) 2015 Pawel Lachowicz, QuantAtRisk.com

import numpy as np
from scipy.stats import beta
import matplotlib.pyplot as plt
import pandas_datareader.data as web

''' 
# Fetching Yahoo! Finance for Facebook
data = web.DataReader("FB", data_source='yahoo',
                  start='2012-05-18', end='2015-12-04')['Adj Close']
cp = np.array(data.values)  # daily adj-close prices

f = open("fb_cp.dat", "wb")
np.save(f, cp)
f.close()
'''

#read in data from file
f = open("fb_cp.dat", "rb")
cp = np.load(f)
f.close()

ret = cp[1:] / cp[:-1] - 1    # compute daily returns
N = len(ret)

# Plotting IBM price- and return-series
plt.figure(num=2, figsize=(9, 6))
plt.subplot(2, 1, 1)
plt.plot(cp)
plt.axis("tight")
plt.ylabel("FB Adj Close [USD]")
plt.subplot(2, 1, 2)
plt.plot(ret, color=(.6, .6, .6))
plt.axis("tight")
plt.ylabel("Daily Returns")
plt.xlabel("Time Period [days]")
plt.show()

# provide a threshold
Lthr = -0.21

# how many events of L < -21% occured?
ne = np.sum(ret < Lthr)
# of what magnitude?
ev = ret[ret < Lthr]
# avgloss = np.mean(ev)  # if ev is non-empty array


# prior
alpha0 = beta0 = 1
# posterior
alpha1 = alpha0 + ne
beta1 = beta0 + N - ne
pr = alpha1 / (alpha1 + beta1)
cl1 = beta.ppf(0.05, alpha1, beta1)
cl2 = beta.ppf(0.95, alpha1, beta1)
ne252 = np.round(252 / (1 / cl2))

print("ne = %g" % ne)
print("alpha', beta' = %g, %g" % (alpha1, beta1))
print("Pr(L < %3g%%) = %5.2f%%\t[%5.2f%%, %5.2f%%]" % (Lthr * 100, pr * 100,
                                                       cl1 * 100, cl2 * 100))
print("E(ne) = %g" % ne252)

############################

returns = cp[1:] / cp[:-1] - 1
Lthr = -0.11

Pr = CL1 = CL2 = np.array([])
for i in range(2, len(returns)):
    # data window
    ret = returns[0:i]
    N = len(ret)
    ne = np.sum(ret < Lthr)
    # prior
    alpha0 = beta0 = 1
    # posterior
    alpha1 = alpha0 + ne
    beta1 = beta0 + N - ne
    pr = alpha1 / (alpha1 + beta1)
    cl1 = beta.ppf(0.05, alpha1, beta1)
    cl2 = beta.ppf(0.95, alpha1, beta1)
    #
    Pr = np.concatenate([Pr, np.array([pr * 100])])
    CL1 = np.concatenate([CL1, np.array([cl1 * 100])])
    CL2 = np.concatenate([CL2, np.array([cl2 * 100])])

plt.figure(num=1, figsize=(10, 5))
plt.plot(Pr, "k")
plt.plot(CL1, "r--")
plt.plot(CL2, "r--")
plt.axis("tight")
plt.ylim([0, 5])
plt.grid((True))
plt.show()

#######################################################
dL = 2
for k in range(-50, 0, dL):
    ev = ret[(ret >= k / 100) & (ret < (k / 100 + dL / 100))]
    avgloss = 0
    ne = np.sum((ret >= k / 100) & (ret < (k / 100 + dL / 100)))
    #
    # prior
    alpha0 = beta0 = 1
    # posterior
    alpha1 = alpha0 + ne
    beta1 = beta0 + N - ne
    pr = alpha1 / (alpha1 + beta1)
    cl1 = beta.ppf(0.05, alpha1, beta1)
    cl2 = beta.ppf(0.95, alpha1, beta1)
    if(len(ev) > 0):
        avgloss = np.mean(ev)
        print("Pr(%3g%% < L < %3g%%) =\t%5.2f%%\t[%5.2f%%, %5.2f%%]  ne = %4g"
              "  E(L) = %.2f%%" %
              (k, k + dL, pr * 100, cl1 * 100, cl2 * 100, ne, avgloss * 100))
    else:
        print("Pr(%3g%% < L < %3g%%) =\t%5.2f%%\t[%5.2f%%, %5.2f%%]  ne = "
              "%4g" % (k, k + dL, pr * 100, cl1 * 100, cl2 * 100, ne))
