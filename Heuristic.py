import glob
import operator
import random
from math import exp


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
        outputTup.append((tempSet, tempWeight))
    uniSet = {i for i in range(1, uniSetNum + 1)}
    f.close()
    return uniSet, outputTup


def makeInputFile(filename, setList, uniSetNum):
    """
    Outputs from a setlist to an output file so random generation of makeInputFile
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
            if i == tup[-1]:
                f.write(str(i))
            else:
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
            if key is not None:
                try:
                    if key(elem) < key(val):
                        smallest.insert(i, elem)
                        smallest = smallest[:k]
                        break
                except (TypeError, AttributeError):
                    smallest.insert(i, elem)
                    smallest = smallest[:k]
                    break
            elif elem < val:
                smallest.insert(i, elem)
                smallest = smallest[:k]
                break
    return smallest


def k_weighted_random(list, k, key=None) -> list:
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

    reweighted = [round(key(x)) for x in list]
    maximum = max(reweighted)
    minimum = min(reweighted)
    # construct dictionary
    lookup = dict()
    val = minimum
    for data in list:
        curr_val = exp((maximum + 1) - round(key(data)))
        min_val = val
        val += curr_val
        lookup[(min_val, val)] = data

    k_weighted_random = []
    for i in range(k):
        random_val = random.uniform(minimum, val)
        for key, value in lookup.items():
            if key[0] <= random_val < key[1]:
                k_weighted_random.append(value)
    return k_weighted_random


class SpotlightSearch:
    class Path:
        def __init__(self, current_set, chosen_sets, cost, options):
            self.current_set = current_set
            self.chosen_sets = chosen_sets
            self.cost = cost
            self.options = options

        def add_to_current_set(self, addition: set):
            self.current_set |= addition
            self.current_set = set(self.current_set)

        def add_to_chosen_sets(self, addition: int):
            self.chosen_sets.append(addition)

        def add_to_cost(self, addition: int):
            self.cost += addition

        def remove_from_options(self, subset: set, weight: int):
            while self.options.count((subset, weight)) > 0:
                self.options.remove((subset, weight))

        def copy(self):
            return SpotlightSearch.Path(self.current_set.copy(), self.chosen_sets.copy(), self.cost,
                                        self.options.copy())

        def get_reweighted(self):
            return self.cost / len(self.current_set)

        def __repr__(self):
            f = open("output.txt", "a")
            f.write(str(self.cost) + "\n")
            for i in self.chosen_sets:
                if i == self.chosen_sets[-1]:
                    f.write(str(i))
                else:
                    f.write(str(i) + " ")
            f.write("\n")
            f.close()
            return f'Sets: {sorted(self.chosen_sets)}, Cost: {self.cost}'

    def __init__(self, universal_set, subsets, chosing_method, *args, **kwargs):
        self.paths = []
        self.universal_set = universal_set
        self.subsets = subsets
        self.subsets_master = dict([(f"{key[0]}{key[1]}", i + 1) for i, key in enumerate(subsets)])
        self.chosing_method = chosing_method
        self.chosing_method_args = args
        self.chosing_method_kwargs = kwargs

    def _set_to_int(self, sety_boi: set, weight: int):
        return self.subsets_master[f"{sety_boi}{weight}"]

    def solve(self):
        finished_sets = []
        # Seed solution with all options
        tempPaths = []
        for subset, cost in self.subsets:
            path = SpotlightSearch.Path(subset, [self._set_to_int(subset, cost)], cost, self.subsets.copy())
            path.remove_from_options(subset, cost)
            tempPaths.append(path)
        self.paths.extend(tempPaths)

        while not all([(len((self.universal_set - temp.current_set)) == 0) for temp in self.paths]):
            k_best_options = self.chosing_method(tempPaths, *self.chosing_method_args, **self.chosing_method_kwargs)
            self.paths.clear()
            self.paths.extend(k_best_options)
            tempPaths = []
            # Calculate weights for each path
            for path in self.paths:
                if len((self.universal_set - path.current_set)) != 0:
                    for subset, cost in path.options:
                        tempPath = path.copy()
                        tempPath.add_to_current_set(subset)
                        tempPath.add_to_chosen_sets(self._set_to_int(subset, cost))
                        tempPath.remove_from_options(subset, cost)
                        tempPath.add_to_cost(cost)
                        tempPaths.append(tempPath)
                else:
                    finished_sets.append(path)

        return finished_sets


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
        while subsets.count(best_option[:2]):
            subsets.remove(best_option[:2])
        chosen_sets.append(subset_master.get(f"{best_option[0]}{best_option[1]}"))
    return current_set, cost, sorted(chosen_sets)


if __name__ == "__main__":
    f = open("output.txt", "w")
    f.write("")
    f.close()
    for file in glob.glob('testInputs/*.txt'):
        print(file)
        x, y = readInput(file)
        hill_output = solve_hill_climbing(x.copy(), y.copy())[1:]
        print(f"Hill: Sets: {hill_output[1]}, Cost: {hill_output[0]}")
        # TODO: Implement spotlight search using annealing for choosing the k paths
        ss = SpotlightSearch(x.copy(), y.copy(), chosing_method=k_min, k=30,
                             key=operator.methodcaller('get_reweighted'))
        print(f"Spotlight: {k_min(ss.solve(), 1, key=operator.attrgetter('cost'))[0]}")
        ssr = SpotlightSearch(x.copy(), y.copy(), chosing_method=k_weighted_random, k=30,
                              key=operator.methodcaller('get_reweighted'))
        print(f"Random Spotlight: {k_min(ssr.solve(), 1, key=operator.attrgetter('cost'))[0]}")
        print("_______________________________________________________________")
