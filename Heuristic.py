import glob
import operator
import random
import re
from math import exp


def formatOutput(cost, chosen_sets,f):
    f.write(str(cost) + "\n")
    for i in chosen_sets:
        if i == chosen_sets[-1]:
            f.write(str(i))
        else:
            f.write(str(i) + " ")
    f.write("\n")


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
        if line == "\n":
            tempWeight = int(f.readline())
            continue
        tempSet = {int(j) for j in line.split()}
        tempWeight = int(f.readline())
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


class LocalBeamSearch:
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
            return LocalBeamSearch.Path(self.current_set.copy(), self.chosen_sets.copy(), self.cost,
                                        self.options.copy())

        def get_reweighted(self):
            return self.cost / len(self.current_set)

        def __repr__(self):
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
            path = LocalBeamSearch.Path(subset, [self._set_to_int(subset, cost)], cost, self.subsets.copy())
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


class SimulatedAnnealing:
    class SubsetBins:
        def __init__(self, all_subsets, lookup_table, active_subsets=()):
            self.all_subsets = all_subsets
            self.lookup_table = lookup_table
            for t_set in active_subsets:
                self.all_subsets[t_set - 1] = True

        def covers(self, universal_set):
            current_set = []
            for j in [i + 1 for i, val in enumerate(self.all_subsets) if val]:
                current_set.extend(self.lookup_table[j][0])
            current_set = set(current_set)
            return len(universal_set - current_set) == 0

        def cost(self) -> int:
            """
            finds the cost of the bin
            :return: sum of the weights for the active subsets of the bin
            """
            cost = 0
            for j in [i + 1 for i, val in enumerate(self.all_subsets) if val]:
                cost += self.lookup_table[j][1]
            return cost

        def get_sets(self):
            return [j for j in [i + 1 for i, val in enumerate(self.all_subsets) if val]]

        def copy(self):
            copy = SimulatedAnnealing.SubsetBins(self.all_subsets.copy(), self.lookup_table)
            return copy

        def __repr__(self):
            return f"Sets: {self.active_sets}, Cost: {self.cost()}"

    def __init__(self, universal_set, subsets):
        self.universal_set = universal_set
        self.subsets = subsets
        self.subsets_master = dict([(f"{key[0]}{key[1]}", i + 1) for i, key in enumerate(self.subsets)])
        self.subsets_master_reverse = dict([(i + 1, key) for i, key in enumerate(self.subsets)])
        self.current_sets = []

    def acceptance_probability(self, old_cost, new_cost, temperature) -> float:
        """
        finds the probability that the new solution is chosen
        :param old_cost:
        :param new_cost:
        :param temperature:
        :return:
        """
        return exp((old_cost - new_cost) / temperature)

    def neighbor(self, bin):
        # swap every value in active to inactive
        # test if the bin has coverage
        neighbor = None
        number_of_possibilities = 0
        # For the sets swap a set from active to inactive or reverse, check for coverage
        # if covering use reservoir selection to decide if we we are using that bin
        # pop the modifications to the bin
        for i in range(len(bin.all_subsets)):
            original_state = bin.all_subsets[i]
            bin.all_subsets[i] = not original_state
            if not original_state:
                number_of_possibilities += 1
                if random.randrange(0, number_of_possibilities) <= 1:
                    neighbor = bin.copy()
            elif bin.covers(self.universal_set):
                number_of_possibilities += 1
                if random.randrange(0, number_of_possibilities) <= 1:
                    neighbor = bin.copy()
            bin.all_subsets[i] = original_state
        return neighbor

    def solve(self, initial_temperature, end_temperature, rate, seed=None, per_temp=100):
        if seed is None:
            seed = [i + 1 for i, _ in enumerate(self.subsets)]
        bin = SimulatedAnnealing.SubsetBins(all_subsets=[False for i in self.subsets], active_subsets=seed,
                                            lookup_table=self.subsets_master_reverse)
        best_solve = bin
        old_cost = bin.cost()
        temperature = initial_temperature
        while temperature >= end_temperature:
            for i in range(0, per_temp):
                new_bin = self.neighbor(bin)
                new_cost = new_bin.cost()
                try:
                    ap = self.acceptance_probability(old_cost, new_cost, temperature)
                except OverflowError:
                    ap = 10
                if ap > random.random():
                    bin = new_bin
                    old_cost = new_cost
                    if old_cost < best_solve.cost():
                        best_solve = bin
            temperature *= rate

        # Get rid of any sets that are not required
        for index, i in enumerate(best_solve.all_subsets):
            if i:
                best_solve.all_subsets[index] = False
                if not best_solve.covers(self.universal_set):
                    best_solve.all_subsets[index] = True

        result = best_solve.get_sets()
        return result, best_solve.cost()

    def _set_to_int(self, sety_boi, weight=None):
        if weight is not None:
            return self.subsets_master[f"{sety_boi}{weight}"]
        return self.subsets_master[f"{sety_boi[0]}{sety_boi[1]}"]


if __name__ == "__main__":
    for file in sorted(glob.glob('testInputs/*.txt')):
        print(file)
        x, y = readInput(file)

        number_1_result = []
        number_1_cost = 10000000

        hill_output = solve_hill_climbing(x.copy(), y.copy())[1:]
        print(f"Hill: Sets: {hill_output[1]}, Cost: {hill_output[0]}")
        if hill_output[0] < number_1_cost:
            number_1_result = hill_output[1]
            number_1_cost = hill_output[0]

        ss = LocalBeamSearch(x.copy(), y.copy(), chosing_method=k_min, k=30,
                             key=operator.methodcaller('get_reweighted'))

        result = k_min(ss.solve(), 1, key=operator.attrgetter('cost'))[0]
        print(f"Local Beam: {result}")
        if result.cost < number_1_cost:
            number_1_result = result.chosen_sets
            number_1_cost = result.cost

        ssr = LocalBeamSearch(x.copy(), y.copy(), chosing_method=k_weighted_random, k=30,
                              key=operator.methodcaller('get_reweighted'))
        result = k_min(ssr.solve(), 1, key=operator.attrgetter('cost'))[0]
        print(f"Random Local Beam: {result}")
        if result.cost < number_1_cost:
            number_1_result = result.chosen_sets
            number_1_cost = result.cost

        sa = SimulatedAnnealing(x.copy(), y.copy())
        sar = sa.solve(10, 0.0001, 0.9)
        print(f"Simulated Annealing: Sets: {sar[0]}, Cost: {sar[1]}")
        if sar[1] < number_1_cost:
            number_1_cost = sar[1]
            number_1_result = sar[0]

        sa = SimulatedAnnealing(x.copy(), y.copy())
        sar = sa.solve(10, 0.001, 0.9, seed=hill_output[1])
        print(f"Simulated Annealing seeded: Sets: {sar[0]}, Cost: {sar[1]}")
        if sar[1] < number_1_cost:
            number_1_cost = sar[1]
            number_1_result = sar[0]
        m = re.search("group\d\d*",file)
        file = m.group(0)
        f = open(f'Outputs/{file}', 'w')
        formatOutput(number_1_cost, number_1_result, f)
        f.close()
        print(f"\nBest Result: Sets: {number_1_result}, Cost: {number_1_cost}")
        print("_______________________________________________________________")
