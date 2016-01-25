#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt

NSAMPLE = 20

def S(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
           (p1[1] - p3[1]) * (p2[0] - p3[0])

def extend_line(start, end):
    if start[0] != 0:
        y1 = (0 - start[0]) * (end[1] - start[1]) / (end[0] - start[0]) + start[1]
    else:
        y1 = start[1]

    if end[0] != 19:
        y2 = (19 - start[0]) * (end[1] - start[1]) / (end[0] - start[0]) + start[1]
    else:
        y2 = end[1]

    return np.array([[0, y1], [19, y2]])

def Decrease():
    x_data = np.arange(0, NSAMPLE)
    r_data = np.float32(np.random.normal(size=(NSAMPLE, )))
    y_data = np.float32(x_data * (-0.5) + r_data * 3)

    samples = np.vstack((x_data, y_data)).T
    lines = []
    for i in range(NSAMPLE - 1):        # start
        for j in range(i + 1, NSAMPLE): # end
            if samples[i][1] > samples[j][1]:
                find = True
                for k in range(NSAMPLE):
                    if k == i or k == j:
                        continue

                    jus = S(samples[i], samples[j], samples[k])
                    print("i = %d, j = %d, k = %d, s = %f" % (i, j, k, jus))
                    if jus > 0:
                        find = False
                        break
                if find:
                    lines.append([i, j])

    lines.sort(key=lambda width:width[1] - width[0], reverse=True)
    lines=lines[:3]
    print(lines)
    envelopes = []
    for line in lines:
        envelope = extend_line(samples[line[0]], samples[line[1]])
        envelopes.append(envelope)

#    envelope = samples[np.array([start, end])]
#    print(envelope)
#    envelope = extend_line(samples[start], samples[end])

    plot_out = plt.plot(samples.T[0], samples.T[1])
    for idx, envelope in enumerate(envelopes):
        labels = "Trend %d(%d, %d)" % (idx + 1, lines[idx][0], lines[idx][1])
        plot_out = plt.plot(envelope.T[0], envelope.T[1], label=labels)
    plt.legend()
    plt.show()

def Increase():
    x_data = np.arange(0, NSAMPLE)
    r_data = np.float32(np.random.normal(size=(NSAMPLE, )))
    y_data = np.float32(x_data * (0.5) + r_data * 3)

    samples = np.vstack((x_data, y_data)).T
    lines = []
    start = end = 0
    for i in range(NSAMPLE - 1):        # start
        for j in range(i + 1, NSAMPLE): # end
            if samples[i][1] < samples[j][1]:
                find = True
                for k in range(NSAMPLE):
                    if k == i or k == j:
                        continue

                    jus = S(samples[i], samples[j], samples[k])
                    print("i = %d, j = %d, k = %d, s = %f" % (i, j, k, jus))
                    if jus < 0:
                        find = False
                        break
                if find:
                    lines.append([i, j])

    lines.sort(key=lambda width:width[1] - width[0], reverse=True)
    lines = lines[:3]
    print(lines)
    envelopes = []
    for line in lines:
        envelope = extend_line(samples[line[0]], samples[line[1]])
        envelopes.append(envelope)

#    envelope = samples[np.array([start, end])]
#    print(envelope)
#    envelope = extend_line(samples[start], samples[end])

    plot_out = plt.plot(samples.T[0], samples.T[1])
    for idx, envelope in enumerate(envelopes):
        labels = "Trend %d(%d, %d)" % (idx + 1, lines[idx][0], lines[idx][1])
        plot_out = plt.plot(envelope.T[0], envelope.T[1], label=labels)
    plt.legend()
    plt.show()

for i in range(10):
    Decrease()

for i in range(10):
    Increase()

