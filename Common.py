import pandas

# Imports data from the data.xlsx file
def importData(filename):
    pureData = pandas.read_excel(filename, header=1, skiprows=1)
    return [[x[2], x[1]] for x in pureData.values]




# Returns a list of uncensored entries from the data list
def filterCensoredOnly(data):
    out = list()
    for entry in data:
        if entry[1] == "S":
            out.append(entry)
    return out


# Returns a list of uncensored entries from the data list
def filterUncensoredOnly(data):
    out = list()
    for entry in data:
        if entry[1] == "F":
            out.append(entry)
    return out

def getTimeList(data):
    out = list()
    for entry in data:
        list.append()


# Prints dat, each entry in a separate row
def printData(data):
    for entry in data:
        print(entry)
