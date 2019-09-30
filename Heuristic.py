def readInput(filename):
    outputTup = []
    uniSet = {}
    f = open(filename, "r")
    uniSetNum = int(f.readline())
    setNums = f.readline()
    for line in f:
        tempSet = {int(j) for j in line.split()}
        tempWeight = int(f.readline());
        outputTup.append((tempSet,tempWeight))
    uniSet = {i for i in range(1,uniSetNum+1)}
    return uniSet, outputTup
print(readInput("input.txt"))
