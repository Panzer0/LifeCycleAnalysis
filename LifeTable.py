import pandas
import matplotlib.pyplot as plt

from Common import filterUncensoredOnly, filterCensoredOnly, importData
from LogNormal import appendIndices

INTERVAL = 2000


def intervalPopulations(data):
    populations = list()
    entriesRemaining = len(data)

    currentMin = 0
    currentMax = INTERVAL

    while True:
        if entriesRemaining == 0:
            return populations
        populations.append(len([entry for entry in data if
                                currentMin < entry[0] < currentMax]))
        entriesRemaining -= populations[-1]

        currentMin += INTERVAL
        currentMax += INTERVAL


def intervalEntering(intervals, size):
    out = list()
    survivors = size
    for interval in intervals:
        out.append(survivors)
        survivors -= interval
    return out


def generateMidpoints(intervalPopulations):
    out = list()
    midpoint = INTERVAL / 2
    for i in range(len(intervalPopulations)):
        out.append(midpoint)
        midpoint += INTERVAL
    return out

def generateStartpoints(intervalPopulations):
    out = list()
    startpoint = 0
    for i in range(len(intervalPopulations)):
        out.append(startpoint)
        startpoint += INTERVAL
    return out


def survival(data, i):
    pureIntervals = intervalPopulations(data)
    n = intervalEntering(pureIntervals, len(data))[i]
    d = intervalPopulations(filterUncensoredOnly(data))[i]
    w = intervalPopulations(filterCensoredOnly(data))[i]

    if i == 0:
        return 1
    return survival(data, i - 1) * (1 - d / (n - w / 2))


def hazard(data, midpoint):
    if midpoint == INTERVAL / 2:
        return 0

    i = int((midpoint - INTERVAL / 2) / INTERVAL)
    pureIntervals = intervalPopulations(data)
    n = intervalEntering(pureIntervals, len(data))[i]
    d = intervalPopulations(filterUncensoredOnly(data))[i]
    w = intervalPopulations(filterCensoredOnly(data))[i]

    return survival(data, i) * d / ((n - 0.5 * w) * INTERVAL)


if __name__ == '__main__':
    # Input data handling
    data = importData("data.xlsx")
    print(data)

    # Survival function handling
    survivals = list()
    for i in range(8):
        survivals.append(survival(data, i))
        print(f"For {i}: {survival(data, i)}")


    # Hazard function handling
    midpoints = generateMidpoints(intervalPopulations(data))
    hazards = list()
    for midpoint in midpoints:
        hazards.append(hazard(data, midpoint))
        print(f"For {midpoint} hazard = {hazard(data, midpoint)}")


    # Plots
    startpoints = generateStartpoints(intervalPopulations(data))
    print(startpoints)
    plt.plot(midpoints, survivals)
    axes = plt.gca()
    axes.set_ylim([0, 1.10])
    axes.set_xlim([0, 20000])
    #plt.plot(midpoints, hazards)
    plt.show()
