import math

import pandas as pandas
import numpy as np
from statistics import NormalDist

from matplotlib import pyplot as plt

from Common import importData, \
    filterUncensoredOnly


def survivalFunction(data, i):
    print(f"Got {i}")
    if i == 0:
        return 1
    # print(f"i = {i}")
    # print(f"data[i+1] = {data[i][2]}")
    return survivalFunction(data, i - 1) * data[i][2] / (data[i][2] + 1)


def appendIndices(data):
    for i, entry in enumerate(data):
        entry.append(i + 1)


def inverseNormal(data, i):
    if i == 0:
        return 0
    # print(survivalFunction(data, i + 1))
    return NormalDist().inv_cdf(1 - survivalFunction(data, i))


def adjustZero(data):
    for i in range(len(data)-1):

        data[i] = data[i + 1]
    data[-1] = -1.07




def generateLogTimes(data):
    out = list()
    for entry in data:
        out.append(math.log(entry[0]))
    return out


def execute(filename):
    data = importData(filename)
    data.sort(reverse=True)
    appendIndices(data)
    data.reverse()

    uncensoredData = filterUncensoredOnly(data)
    print(data)
    print(uncensoredData)

    survivals = list()

    for i in range(len(uncensoredData)):
        survivals.append(
            survivalFunction(uncensoredData, len(uncensoredData) - i - 1))
        # print("for i = ", i, " ", survivalFunction(data, len(uncensoredData)-i-1))
        # print(f"for i = {i}, rank = {data[i][2]}  S = {survivalFunction(data, len(data) - i - 1)}")

    print(survivals)
    print(len(survivals))

    invNorms = list()

    for i in range(len(uncensoredData)):
        print(f"for i = {i + 1}, time = {uncensoredData[i][0]} "
              f"InvNormal = {inverseNormal(uncensoredData, i)}")
        invNorms.append(inverseNormal(uncensoredData, i))

    # print(f"logTimes: {generateLogTimes(data)}")
    print(f"invNorms: {invNorms}")
    adjustZero(invNorms)

    uncensoredLogTimes = generateLogTimes(uncensoredData)

    invNorms = invNorms[:-3 or None]
    uncensoredLogTimes = uncensoredLogTimes[:-3 or None]

    # Least square line
    a, b = np.polyfit(np.array(uncensoredLogTimes),
                      np.array(invNorms), 1)

    print(f"m = {a}")
    print(f"b = {b}")
    print(f"Again: {invNorms}")
    plt.scatter(uncensoredLogTimes, invNorms)
    plt.plot(uncensoredLogTimes, invNorms)
    plt.plot(uncensoredLogTimes, a * np.array(uncensoredLogTimes) + b)
    print(f"B ======= {b}, M ====== {a}")

    axes = plt.gca()
    axes.set_ylim([-3, -1])
    plt.xlabel("Elapsed time (days)")
    plt.ylabel("Probit(1-surv)")
    plt.show()

    return [a, b]


if __name__ == '__main__':
    execute("data.xlsx")
