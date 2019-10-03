def readInput(filename):
    outputTup = []
    uniSet = {}
    f = open(filename, "r")
    uniSetNum = int(f.readline())
    setNums = f.readline()
    for line in f:
        tempSet = {int(j) for j in line.split()}
        tempWeight = int(f.readline());
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
    if setOfChosen == unified:
        for i in chosen:
            i = int(i)-1
            value = allSets[i][1]
            sum+=value
        if sum == weightTotal:
            print("success")
        else:
            print("weight imbalance")
    else:
        print("incorrect set coverage")


uniSet, allSets = readInput("input.txt")
totalWeight, chosenSets = readOutput("output.txt")
determineCorrectness(uniSet, allSets, chosenSets, totalWeight)



