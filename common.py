# Returns a list of uncensored entries from the data list
def filterCensoredOnly(data):
    out = list()
    for entry in data:
        if entry[1] == "F":
            out.append(entry)
    return out


# Returns a list of uncensored entries from the data list
def filterUncensoredOnly(data):
    out = list()
    for entry in data:
        if entry[1] == "S":
            out.append(entry)
    return out


# Prints dat, each entry in a separate row
def printData(data):
    for entry in data:
        print(entry)
