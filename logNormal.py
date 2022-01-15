import math

import pandas as pandas
from statistics import NormalDist

from matplotlib import pyplot as plt

from common import filterCensoredOnly, printData, importData


def survivalFunction(data, i):
    if i == 0:
        return 1
    return survivalFunction(data, i - 1) * data[i + 1][2] / (data[i + 1][2] + 1)


def appendIndices(data):
    for i, entry in enumerate(data):
        entry.append(i + 1)


def inverseNormal(data, i):
    #print(survivalFunction(data, i + 1))
    return NormalDist().inv_cdf(1 - survivalFunction(data, i + 1))

def generateLogTimes(data):
    out = list()
    for entry in data:
        out.append(math.log(entry[0]))

if __name__ == '__main__':
    data = importData("data.xlsx")
    data.sort(reverse=True)
    appendIndices(data)
    data.reverse()

    uncensoredData = filterCensoredOnly(data)

    #for i in range(data[0][2]):
    #    print("for i = ", i, " ", survivalFunction(data, i))


    invNorms = list()
    print(len(data))
    for i in range(len(data)):
        print(f"for i = {i + 1}, time = {data[i][0]} "
              f"InvNormal = {inverseNormal(data, i)}")
        invNorms.append(inverseNormal(data, i))

    print("Test")

    plt.plot(generateLogTimes(data), invNorms)
    plt.show()

