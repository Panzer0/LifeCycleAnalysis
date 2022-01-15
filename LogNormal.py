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
    data[0] = 1.4 * -2


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
    #adjustZero(invNorms)

    # Least square line
    m, b = np.polyfit(np.array(generateLogTimes(uncensoredData)),
                      np.array(invNorms), 1)

    print(f"m = {m}")
    print(f"b = {b}")
    print(f"Again: {invNorms}")
    plt.scatter(generateLogTimes(uncensoredData), invNorms)
    plt.plot(generateLogTimes(uncensoredData), invNorms)
    plt.plot(generateLogTimes(uncensoredData),
             m * np.array(generateLogTimes(uncensoredData)) + b)
    print(f"B ======= {b}, M ====== {m}")
    axes = plt.gca()
    axes.set_ylim([-3, -1])
    plt.xlabel("Elapsed time (days)")
    plt.ylabel("Probit(1-surv)")
    plt.show()

    return [generateLogTimes(uncensoredData),
            invNorms,
            generateLogTimes(uncensoredData),
            m * np.array(generateLogTimes(uncensoredData)) + b]


if __name__ == '__main__':
    execute("data.xlsx")
