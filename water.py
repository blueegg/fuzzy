#!/usr/bin/env python3

import numpy as np
import math
import matplotlib.pyplot as plt

Y = np.array([[1.0, 2.0, 4.0, 10, 65, 160],
              [2.5, 5.0, 25, 50, 200, 600],
              [30, 50, 300, 500, 2000, 6000],
              [0.3, 0.4, 2.0, 4.0, 10, 25],
              [10, 5.0, 1.5, 1.0, 0.4, 0.3]
              ])

target = Y.shape[0]
level = Y.shape[1]
print("targe = %d, level = %d" % (target, level))
print("Y:\n", Y)

S = np.empty_like(Y)
for i in range(target):
    for j in range(level):
        S[i, j] = (Y[i, j] - Y[i, 0]) / (Y[i, -1] - Y[i, 0])

print("S.T:\n", S.T)

XT = np.array([[0.88, 130, 410, 1.43, 2.98],
              [4.33, 21, 180, 3.38, 2.40],
              [4.91, 50, 969, 5.42, 1.46],
              [16.20, 26, 1020, 5.16, 1.16],
              [15.38, 87, 1540, 4.40, 0.65],
              [14.56, 140, 2270, 4.34, 0.27],
              [77.70, 135, 2140, 6.96, 0.36],
              [82.40, 332, 2660, 14.60, 0.49],
              [95.94, 136, 2230, 10.18, 0.37],
              [202.10, 708, 6790, 8.86, 0.31],
              [262.40, 500, 16050, 13.60, 0.15],
              [185.10, 670, 7200, 14.80, 0.26]
             ])

sample = XT.shape[0]
print("sample number = ", XT.shape[0])

X = XT.T
print("X:\n", X)

R = np.empty_like(X)

c = level - 1

for i in range(target):
    for j in range(sample):
        if i < 4:
            if X[i, j] > Y[i, c]:
                R[i, j] = 1
            elif X[i, j] < Y[i, 0]:
                R[i, j] = 0
            else:
                R[i, j] = (X[i, j] - Y[i, 0]) / (Y[i, c] - Y[i, 0])
        else:
             if X[i, j] < Y[i, c]:
                R[i, j] = 1
             elif X[i, j] > Y[i, 0]:
                R[i, j] = 0
             else:
                R[i, j] = (X[i, j] - Y[i, 0]) / (Y[i, c] - Y[i, 0])

print("R.T:\n", R.T)

lam = np.diag([0.233, 0.217, 0.189, 0.210, 0.151])

print("lambda:\n",lam)

A = lam.dot(R)

total = A.sum(axis= 0)

W = A / total

print("W.T:\n", W.T)

### p = 2, calculate POME
Z = np.zeros((level, sample))

for h in range(level):
    for j in range(sample):
        total = 0.0
        for i in range(target):
            total += math.pow(W[i, j] * (R[i, j] - S[i, h]), 2)
        Z[h, j] = math.sqrt(total)

#print("Z: \n", Z)

nita1 = -40.0

Z1 = np.exp(nita1 * Z)

#print("Z1 = ", Z1)

total = Z1.sum(axis=0)

#print("total = ", total)

U1 = Z1 / total

print("U1.T = \n", U1.T)

shannon_m = U1 * np.log(U1) * (-1.0)
shannon = shannon_m.sum(axis= 0)

print("U1 Shannon is:\n", shannon)

### p = 1, calculate POME
Z = np.zeros((level, sample))

for h in range(level):
    for j in range(sample):
        total = 0.0
        for i in range(target):
            total += abs(W[i, j] * (R[i, j] - S[i, h]))
        Z[h, j] = total

#print("Z: \n", Z)

nita2 = -23.0

Z2 = np.exp(nita2 * Z)

#print("Z2 = ", Z2)

total = Z2.sum(axis=0)

U2 = Z2 / total

print("U2.T = ", np.round(U2.T, 4))

shannon_m = U2 * np.log(U2) * (-1.0)
shannon = shannon_m.sum(axis=0)
print("U2 shannon is:\n", shannon)

