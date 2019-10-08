import glob
import re

def readInput(filename):
    outputTup = []
    uniSet = {}
    f = open(filename, "r")
    uniSetNum = int(f.readline())
    setNums = f.readline()
    for i in range(int(setNums)):
        line = f.readline()
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


for file in sorted(glob.glob("outputs/*.txt")):
    m = re.search("group\d\d*",file)
    file_input = "input_" + m.group(0)
    uniSet, allSets = readInput("inputs/" + file_input + ".txt")
    totalWeight, chosenSets = readOutput(file)
    print(f"{file} : {determineCorrectness(uniSet, allSets, chosenSets, totalWeight)}")
