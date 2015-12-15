#! /usr/bin/env python3

import numpy as np

x0 = np.array([3.936, 4.575, 4.968, 5.063, 5.968, 5.507])

n = x0.shape[0]

x1 = np.empty_like(x0)

x1[0] = x0[0]
for i in range(x1.shape[0] - 1):
    x1[i + 1] = x1[i] + x0[i + 1]

print("x1:\n",x1)

B = np.ones((n-1, 2))
Y = x0[1:].T 

for i in range(n-1):
    B[i, 0] = -0.5 * (x1[i] + x1[i+1])

print("B:\n", B)
print("Y:\n",Y)

a = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)

print("a:\n", a)

