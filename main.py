import pandas as pandas
from statistics import NormalDist


def survivalFunction(data, i):
    if i == 0:
        return 1
    return survivalFunction(data, i - 1) * data[i+1][2] / (data[i+1][2] + 1)


def appendIndices(data):
    for i, entry in enumerate(data):
        entry.append(i + 1)


def inverseNormal(data, i):
    print(survivalFunction(data, i + 1))
    return NormalDist().inv_cdf(1 - survivalFunction(data, i + 1))


def printData(data):
    for entry in data:
        print(entry)


if __name__ == '__main__':
    pureData = pandas.read_excel('data.xlsx', header=1, skiprows=1)
    preparedData = [[x[2], x[1]] for x in pureData.values]
    preparedData.sort(reverse=True)
    appendIndices(preparedData)
    preparedData.reverse()

    #for i in range(preparedData[0][2]):
        #print("for i = ", i, " ", survivalFunction(preparedData, i))


    for i in range(preparedData[0][2]):
        print("for i =", i + 1, "time =", preparedData[i][0], inverseNormal(preparedData, i))


