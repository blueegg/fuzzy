# Predicting Heavy and Extreme Losses in Real-Time for Portfolio Holders
# (c) 2015 QuantAtRisk.com, by Pawel Lachowicz
#
# heavy2.py

import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from pyvar import cpr

# ---1. Data Processing

# fetch and download daily adjusted-close price series for CAAS stock
#  and NASDAQ index using Yahoo! Finance public data provider
'''
caas = web.DataReader("CAAS", data_source='yahoo',
                   start='2005-05-13', end='2015-05-13')['Adj Close']
nasdaq = web.DataReader("^IXIC", data_source='yahoo',
                   start='2005-05-13', end='2015-05-13')['Adj Close']

CAAScp = np.array(caas.values)
NASDAQcp = np.array(nasdaq.values)

f = open("data2.dat","wb")
np.save(f,CAAScp)
np.save(f,NASDAQcp)
f.close()
'''

f = open("data2.dat","rb")
CAAScp = np.load(f)
NASDAQcp = np.load(f)
f.close()

# compute the return-series
retCAAS = CAAScp[1:]/CAAScp[:-1]-1
retNASDAQ = NASDAQcp[1:]/NASDAQcp[:-1]-1

# plotting (figure #1)
#  return-series for CAAS and NASDAQ index
#
plt.figure(num=1, figsize=(10, 6))
plt.subplot(211)
plt.grid(True)
plt.plot(retCAAS, '-r', label="CAAS")
plt.axis("tight")
plt.ylim([-0.25,0.5])
plt.legend(loc="upper right")
plt.ylabel("CAAS daily returns")
plt.subplot(212)
plt.grid(True)
plt.plot(retNASDAQ, '-', label="NASDAQ")
plt.legend(loc="upper right")
plt.axis("tight")
plt.ylim([-0.10,0.15])
plt.ylabel("NASDAQ daily returns")
plt.xlabel("Trading days 13/05/2005-13/05/2015")
#plt.show()

# ---2. Computations of Conditional Probabilities for Rare Events

# isolate return-series displaying negative returns solely
#  set 1 for time stamps corresponding to positive returns
nretCAAS = np.where(retCAAS < 0, retCAAS, 1)
nretNASDAQ = np.where(retNASDAQ < 0, retNASDAQ, 1)

# set threshold for rare events
thr = -0.065

# compute the sets of events
A = np.where(nretCAAS < 0, nretCAAS, 1)
A = np.where(A >= thr, A, 1)
B = np.where(nretCAAS < thr, retCAAS, 1)
R = np.where(nretNASDAQ < thr, retNASDAQ, 1)
nA = float(len(A[A != 1]))
nB = float(len(B[B != 1]))
n = float(len(nretCAAS[nretCAAS != 1]))  # n must equal to nA + nB
# (optional)
print(nA, nB, n == (nA + nB))  # check, if True then proceed further
print(len(A), len(B), len(R))
print

# compute the probabilities
pA = nA/n
pB = nB/n

# compute the conditional probabilities
pRA = np.sum(np.where(R+A < 0, 1, 0))/n
pRB = np.sum(np.where(R+B < 0, 1, 0))/n

pR = pRA*pA + pRB*pB

# display resultsh
print("Pr(A)\t = %5.5f%%" % (pA*100.))
print("Pr(B)\t = %5.5f%%" % (pB*100.))
print("Pr(R|A)\t = %5.5f%%" % (pRA*100.))
print("Pr(R|B)\t = %5.5f%%" % (pRB*100.))
print("Pr(R)\t = %5.5f%%" % (pR*100.))

if(pR>0):
    pBR = pRB*pB/pR
    print("\nPr(B|R)\t = %5.5f%%" % (pBR*100.))
else:
    print("\nPr(B|R) impossible to be determined. Pr(R)=0.")


from pyvar import cpr

prob = []
for t in range(2,len(retCAAS)-1):
    ret1 = retCAAS[0:t]
    ret2 = retNASDAQ[0:t]
    pBR, _ = cpr(ret1, ret2, thr=thr)
    prob.append(pBR)

# plotting (figure #2)
#   conditional probability for rare events given threshold
#
plt.figure(num=2, figsize=(10, 6))
plt.plot(np.array(prob)*100., 'r', label="CAAS")
plt.ylabel("Pr(B|R) [%]")
plt.axis('tight')
plt.title("L$_{thr}$ = %.2f%%" % (thr*100.))
plt.legend(loc="upper left")
plt.xlabel("Trading days 13/05/2005-13/05/2015")
plt.show()


# extras-----------------------

f = open("data3.dat","rb")
alphas = np.load(f)
f.close()

prob1 = []
prob2 = []
for t in range(2,len(retCAAS)-1):
    ret1 = retCAAS[0:t]
    ret2 = retNASDAQ[0:t]
    pBR, pR = cpr(ret1, ret2, thr=-0.065)
    prob1.append(pBR)
    prob2.append(pR)


# plotting (figure #3)
#   conditional probability for rare events given threshold
#
fig, ax1 = plt.subplots(num=2, figsize=(10, 6))
plt.plot(np.array(prob1)*100., 'r', label="Pr(B|R) at L=-6.5%")
plt.plot(np.array(prob2)*100., 'b', label="Pr(R) at L=-6.5%")
plt.plot(np.array(alphas*100.), 'k', label="Pr(L < -6.5%)")
plt.axis('tight')
plt.ylim([-0.5, 16])
plt.legend(loc="upper left")
plt.xlabel("Trading days 13/05/2005-13/05/2015")
plt.show()


