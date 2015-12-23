#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

a = 80
b = 60

theta = np.arange(0, np.pi / 2, 0.01)

for n in np.arange(2, 10, 1):
    x = a * np.power(np.cos(theta), 2 / n)
    y = b * np.power(np.sin(theta), 2 / n)
    plt.plot(x, y)

plt.show()

