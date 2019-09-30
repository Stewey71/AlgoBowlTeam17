def readInput(filename):
    """
    Reads from input file and outputs the universal set, and a list of tuples where
    first element of tuple is the subset and second element of tuple is the weight
    of subset
    
    :param filename: name of file to read in from
    """
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
    """
    Outputs from a setlist to an output file so random generation of outputFile
    works

    :param filename: The list of file to output to:
    :param setList: list of tuples where first element of tuple is subset
                    and second element of tuple is the weight of subset
    :param uniSetNum: Size of universal set
    """
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
