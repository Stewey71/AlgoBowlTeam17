import glob

def readInput(filename):
    outputTup = []
    uniSet = {}
    f = open(filename, "r")
    uniSetNum = int(f.readline())
    setNums = f.readline()
    for line in f:
        tempSet = {int(j) for j in line.split()}
        tempWeight = int(f.readline())
        outputTup.append((tempSet, tempWeight))
    uniSet = {i for i in range(1, uniSetNum + 1)}
    f.close()
    return uniSet, outputTup


def readOutput(filename):
    x = open(filename, "r")
    outputSets = []
    weight = int(x.readline())
    outputSets = x.readline().split()
    return weight, outputSets


def determineCorrectness(unified, allSets, chosen, weightTotal):
    setOfChosen = set()
    sum = 0
    for i in chosen:
        i = int(i)-1
        value = allSets[i][0]
        for x in value:
            setOfChosen.add(x)
    if len(unified - setOfChosen) == 0:
        for i in chosen:
            i = int(i)-1
            value = allSets[i][1]
            sum+=value
        if sum == weightTotal:
            return "Success"
        else:
            return "Weight imbalance"
    else:
        return "Incorrect set coverage"


for i in sorted(glob.glob("testOutputs/*.txt")):
    uniSet, allSets = readInput("testInputs/" + i[12:17] + ".txt")
    totalWeight, chosenSets = readOutput(i)
    print(f"{i} : {determineCorrectness(uniSet, allSets, chosenSets, totalWeight)}")
