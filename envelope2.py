#!/usr/bin/env python

import numpy as np
from matplotlib import pyplot as plt

NSAMPLE = 19


def S(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
           (p1[1] - p3[1]) * (p2[0] - p3[0])


def extend_line(start, end):
    if start[0] != 2202:
        y1 = (2202 - start[0]) * (end[1] - start[1]) / \
            (end[0] - start[0]) + start[1]
    else:
        y1 = start[1]

    if end[0] != 97203:
        y2 = (97203 - start[0]) * (end[1] - start[1]) / \
            (end[0] - start[0]) + start[1]
    else:
        y2 = end[1]

    return np.array([[2202, y1], [97203, y2]])


def Decrease(x_data, y_data):
    #    x_data = np.arange(0, NSAMPLE)
    #    r_data = np.float32(np.random.normal(size=(NSAMPLE, )))
    #    y_data = np.float32(x_data * (-0.5) + r_data * 3)

    samples = np.vstack((x_data, y_data)).T
    lines = []
    for i in range(NSAMPLE - 1):        # start
        for j in range(i + 1, NSAMPLE):  # end
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

    lines.sort(key=lambda width: width[1] - width[0], reverse=True)
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


def Increase():
    x_data = np.arange(0, NSAMPLE)
    r_data = np.float32(np.random.normal(size=(NSAMPLE, )))
    y_data = np.float32(x_data * (0.5) + r_data * 3)

    samples = np.vstack((x_data, y_data)).T
    lines = []
    start = end = 0
    for i in range(NSAMPLE - 1):        # start
        for j in range(i + 1, NSAMPLE):  # end
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

    lines.sort(key=lambda width: width[1] - width[0], reverse=True)
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


def do_extend_line(start_p, end_p, desired_x_list):
    desired_y_list = []
    for x in desired_x_list:
        y = (end_p[1] - start_p[1]) * (x - start_p[0]) / \
            (end_p[0] - start_p[0]) + start_p[1]
        desired_y_list.append(y)
    return desired_y_list


def do_increase(x_list, y_list):
    n = len(x_list)
    assert(len(y_list) == n)
    lines = []
    for i in range(n - 1):        # start
        for j in range(i + 1, n):  # end
            if y_list[i] < y_list[j]:
                find = True
                for k in range(n):
                    if k == i or k == j:
                        continue

                    jus = S((x_list[i], y_list[i]), (x_list[j],y_list[j]), 
                            (x_list[k], y_list[k]))
                    if jus < 0:
                        find = False
                        break
                if find:
                    lines.append([i, j])
    lines.sort(key=lambda width: width[1] - width[0], reverse=True)
    lines = lines[:3]
    return lines


def do_decrease(x_list, y_list):
    n = len(x_list)
    assert(len(y_list) == n)
    lines = []
    for i in range(n - 1):        # start
        for j in range(i + 1, n):  # end
            if y_list[i] > y_list[j]:
                find = True
                for k in range(n):
                    if k == i or k == j:
                        continue

                    jus = S((x_list[i], y_list[i]), (x_list[j],
                                                     y_list[j]), (x_list[k], y_list[k]))
                    if jus > 0:
                        find = False
                        break
                if find:
                    lines.append([i, j])

    lines.sort(key=lambda width: width[1] - width[0], reverse=True)
    lines = lines[:3]
    return lines


if __name__ == '__main__':
    x = [2202, 5401, 16152, 20879, 23490, 28181, 37008, 37836, 43201,
         48838, 54172, 59948, 64802, 74812, 78007, 81313, 87115, 91860, 97203]

    y = [21228.156740911567, 21118.33318493456, 21089.292237236776,
         21305.411343572978, 21320.807468577146, 21446.48485677886,
         21556.473875982552, 21563.90016261253, 21440.655329000092,
         21106.293235281777, 20973.501538883214, 20844.407759515514,
         20892.173448490787, 20714.783324275268, 20924.89277920091,
         20754.544505947757, 20751.055931857285, 20614.198645452187,
         20443.4155462559]

    print(len(x), len(y))

    Decrease(np.array(x), np.array(y))
#    for i in range(10):
#        Decrease()

#    for i in range(10):
#        Increase()
