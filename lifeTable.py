INTERVAL = 2000

def intervalPopulations(data):
    populations = list()
    entriesReamining = len(data)

    currentMin = 0
    currentMax = INTERVAL

    while True:
        if entriesReamining == 0:
            return populations
        populations.append(len([entry for entry in data if currentMin < entry[0] < currentMax]))
        entriesReamining -= populations[-1]

        currentMin+=1
        currentMax+=1





if __name__ == '__main__':
