#!/usr/bin/env python

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def f(x):
    y = (x - 1.5)**2 + 0.5

    print("X = {}, Y = {}".format(x, y))

    return y

def test_run():
    Xguess = 2.0

    min_result = spo.minimize(f, Xguess, method='SLSQP', options={'disp':True})

    print("Minima found here:")
    print("X = {}, Y= {}".format(min_result.x, min_result.fun))

if __name__ == "__main__":
    test_run()


