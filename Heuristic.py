import operator


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


def reweight_subsets(comparison_set: set, subsets: list):
    """
    Calculates the weights for a subset as the weight/number of new elements
    to try and maximize the number of new elements for the cost
    :param comparison_set: the set we are trying to grow
    :param subsets: the sets that can be unioned with the comparison set with their weights (set, weight)
    :return: [(the subset, their og weight, their new weight), ...]
    """
    weighted_subsets = []
    for subset, weight in subsets:
        new_weight = weight / (len(subset - comparison_set) + 1)
        weighted_subsets.append((subset, weight, new_weight))
    return weighted_subsets


def k_min(list, k, key=None) -> list:
    """
    Returns a list of size min(len(list),k) of the smallest elements
    O(kn)
    :param list: the list to get the k smallest
    :param key: what to compare on
    :return: the k smallest, smallest to largest
    """
    if len(list) <= k:
        if key is not None:
            return sorted(list, key=key)
        return sorted(list)
    smallest = [1e9 for _ in range(k)]
    for elem in list:
        for i, val in enumerate(smallest):
            try:
                if key(elem) < key(val):
                    smallest.insert(i, elem)
                    smallest = smallest[:k]
                    break
            except TypeError:
                smallest.insert(i, elem)
                smallest = smallest[:k]
                break
    return smallest


# TODO: Implement Spotlight search
# TODO: Implement spotlight search using annealing for choosing the k paths

def solve_hill_climbing(universal_set: set, subsets: list):
    """
    Iteratively choses the set with the lowest cost per new element until the set
    spans the universal set
    :param universal_set: the set to spane
    :param subsets: the sets that can be unioned to create the universal set and their weights [(set, weight), ...]
    :return: (the covered set, the total cost, the chosen sets [based on location in subsets])
    """

    current_set = set()
    cost = 0
    # key: the set and weight as a string
    # value: location in subsets
    subset_master = dict([(f"{key[0]}{key[1]}", i + 1) for i, key in enumerate(subsets)])
    chosen_sets = []
    while universal_set != current_set and subsets:
        # Calculate new weights
        reweighted_subsets = reweight_subsets(current_set, subsets)
        # Grab the smallest weight
        best_option = min(reweighted_subsets, key=operator.itemgetter(2))
        # Update costs, current set, chosen set, and subsets
        cost += best_option[1]
        current_set |= best_option[0]
        subsets.remove(best_option[:2])
        chosen_sets.append(subset_master.get(f"{best_option[0]}{best_option[1]}"))
    return current_set, cost, sorted(chosen_sets)


if __name__ == "__main__":
    x, y = readInput("testInputs/test1.txt")
    print(solve_hill_climbing(x.copy(), y.copy())[1:])
    print(solve_spotlight_search(x.copy(), y.copy()))
