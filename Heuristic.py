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
    f.close()
    return uniSet, outputTup

def outputFile(filename, setList, uniSetNum):
    f = open(filename, "w")
    f.write(str(uniSetNum) + "\n")
    f.close()
    f = open(filename, "a")
    f.write(str(len(setList)) + "\n")
    for tup in setList:
        for i in tup[0]:
            f.write(str(i) + " ")
        f.write("\n")    
        f.write(str(tup[1]) + "\n")
    f.close()


x,y = readInput("input.txt")
outputFile("output.txt",y,len(x))
