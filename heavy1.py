# Predicting Heavy and Extreme Losses in Real-Time for Portfolio Holders
# (c) 2015 QuantAtRisk.com, by Pawel Lachowicz
#
# heavy1.py

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import pandas.io.data as web
import numpy as np
from pyvar import findvar, findalpha

# ---1. Data Processing

# fetch and download daily adjusted-close price series for CAAS
#  and AAPL stocks using Yahoo! Finance public data provider
'''
caas = web.DataReader("CAAS", data_source='yahoo',
                      start='2005-05-13', end='2015-05-13')['Adj Close']
aapl = web.DataReader("AAPL", data_source='yahoo',
                      start='2005-05-13', end='2015-05-13')['Adj Close']

CAAScp = np.array(caas.values)
AAPLcp = np.array(aapl.values)

f = open("data1.dat","wb")
np.save(f, CAAScp)
np.save(f, AAPLcp)
f.close()
'''
# read in the data from a file
f = open("data1.dat","rb")
CAAScp = np.load(f)
AAPLcp = np.load(f)
f.close()

# compute return-series
retCAAS = CAAScp[1:]/CAAScp[:-1]-1
retAAPL = AAPLcp[1:]/AAPLcp[:-1]-1

# plotting (figure #1)
#  adjusted-close price-series
fig, ax1 = plt.subplots(figsize=(10, 6))
plt.xlabel("Trading days 13/05/2005-13/05/2015")
plt.plot(CAAScp, '-r', label="CAAS")
plt.axis("tight")
plt.legend(loc=(0.02, 0.8))
plt.ylabel("CAAS Adj Close Price (US$)")
ax2 = ax1.twinx()
plt.plot(AAPLcp, '-', label="AAPL")
plt.legend(loc=(0.02, 0.9))
plt.axis("tight")
plt.ylabel("AAPL Adj Close Price (US$)")

# plotting (figure #2)
#  daily return-series
plt.figure(num=2, figsize=(10, 6))
plt.subplot(211)
plt.grid(True)
plt.plot(retCAAS, '-r', label="CAAS")
plt.axis("tight")
plt.ylim([-0.25,0.5])
plt.legend(loc="upper right")
plt.ylabel("CAAS daily returns")
plt.subplot(212)
plt.grid(True)
plt.plot(retAAPL, '-', label="AAPL")
plt.legend(loc="upper right")
plt.axis("tight")
plt.ylim([-0.25,0.5])
plt.ylabel("AAPL daily returns")
plt.xlabel("Trading days 13/05/2005-13/05/2015")


# ---2. Compuation of VaR given alpha

alpha = 0.01

VaR_CAAS, bardata1 = findvar(retCAAS, alpha=alpha, nbins=200)
VaR_AAPL, bardata2 = findvar(retAAPL, alpha=alpha, nbins=100)

cl = 100.*(1-alpha)

print("%g%% VaR (CAAS) = %.2f%%" % (cl, VaR_CAAS*100.))
print("%g%% VaR (AAPL) = %.2f%%\n" % (cl, VaR_AAPL*100.))

# plotting (figure #3)
#  histograms of daily returns; H(x)
#
plt.figure(num=3, figsize=(10, 6))
c = (.7,.7,.7)  # grey color (RGB)
#
# CAAS
ax = plt.subplot(211)
hist1, bins1 = np.histogram(retCAAS, bins=200, density=False)
widths = np.diff(bins1)
b = plt.bar(bins1[:-1], hist1, widths, color=c, edgecolor="k", label="CAAS")
plt.legend(loc=(0.02, 0.8))
#
# mark in red all histogram values where int_{-infty}^{VaR} H(x)dx = alpha
hn, nb, _ = bardata1
for i in range(nb):
    b[i].set_color('r')
    b[i].set_edgecolor('k')
plt.text(-0.225, 30, "VaR$_{%.0f}$ (CAAS) = %.2f%%" % (cl, VaR_CAAS*100.))
plt.xlim([-0.25, 0])
plt.ylim([0, 50])
#
# AAPL
ax2 = plt.subplot(212)
hist2, bins2 = np.histogram(retAAPL, bins=100, density=False)
widths = np.diff(bins2)
b = plt.bar(bins2[:-1], hist2, widths, color=c, edgecolor="k", label="AAPL")
plt.legend(loc=(0.02, 0.8))
#
# mark in red all histogram bars where int_{-infty}^{VaR} H(x)dx = alpha
hn, nb, wd = bardata2
for i in range(nb):
    b[i].set_color('r')
    b[i].set_edgecolor('k')
plt.text(-0.225, 30, "VaR$_{%.0f}$ (AAPL) = %.2f%%" % (cl, VaR_AAPL*100.))
plt.xlim([-0.25, 0])
plt.ylim([0, 50])
plt.xlabel("Stock Returns (left tail only)")
#plt.show()


# ---3. Computation of alpha, given the threshold for rare events

thr = -0.10

alpha1, ne1 = findalpha(retCAAS, thr=thr, nbins=200)
alpha2, ne2 = findalpha(retAAPL, thr=thr, nbins=200)

print("CAAS:")
print("  Pr( L < %.2f%% ) = %.2f%%" % (thr*100., alpha1*100.))
print("  %g historical event(s)" % ne1)
print("AAPL:")
print("  Pr( L < %.2f%% ) = %.2f%%" % (thr*100., alpha2*100.))
print("  %g historical event(s)" % ne2)


# ---4. Mapping alphas for Rare Events

alphas = []
nevents = []
for t in range(1,len(retCAAS)-1):
    data = retCAAS[0:t]
    alpha, ne = findalpha(data, thr=thr, nbins=500)
    alphas.append(alpha)
    nevents.append(ne)

alphas2 = []
nevents2 = []
for t in range(1,len(retAAPL)-1):
    data = retAAPL[0:t]
    alpha, ne = findalpha(data, thr=thr, nbins=500)
    alphas2.append(alpha)
    nevents2.append(ne)

plt.close("all")


# plotting (figure #4)
#   running probability for rare events
#
plt.figure(num=4, figsize=(10, 6))
ax1 = plt.subplot(211)
plt.plot(np.array(alphas)*100., 'r')
plt.plot(np.array(alphas2)*100.)
plt.ylabel("Pr( L < %.2f%% ) [%%]" % (thr*100.))
plt.axis('tight')
ax2 = plt.subplot(212)
plt.plot(np.array(nevents), 'r', label="CAAS")
plt.plot(np.array(nevents2), label="AAPL")
plt.ylabel("# of Events with L < %.2f%%" % (thr*100.))
plt.axis('tight')
plt.legend(loc="upper left")
plt.xlabel("Trading days 13/05/2005-13/05/2015")
plt.show()


# ---5. Extra plot

alphas = []
for t in range(1,len(retCAAS)-1):
    data = retCAAS[0:t]
    alpha, _ = findalpha(data, thr=-0.065, nbins=500)
    alphas.append(alpha)

f = open("data3.dat","wb")
np.save(f,np.array(alphas))
f.close()

plt.close("all")


# plotting (figure #5)
#   running probability for rare events
#
plt.figure(num=5, figsize=(10, 6))
plt.plot(np.array(alphas)*100., 'r')
plt.ylabel("Pr( L < %.2f%% ) [%%]" % (thr*100.))
plt.axis('tight')
plt.legend(loc="upper left")
plt.xlabel("Trading days 13/05/2005-13/05/2015")
plt.show()
