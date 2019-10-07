import random

#from Heuristic import makeInputFile


def set_creator(universal_set):
    """
    Subsects a universal sets into sets of sizes: size/2, size/4, ... 2
    From highest index to lowest index

    :param universal_set: The list of subsets
    """
    curr_set_size = len(universal_set)
    sets = []
    while curr_set_size >= 1:
        sets.append(universal_set[curr_set_size // 2:curr_set_size + 1])
        curr_set_size //= 2
    return sets

# Parameters
size = 500
big_subset_weight = 1000

# create output file
output = open("createdInput.txt", "w")

# build the universal set
universal_set = [i+1 for i in range(size)]
subsets = []

# create sets
subsets.extend(set_creator(universal_set))
subsets.extend(set_creator(subsets[0]))

# Add in random numbers to random sets
# Set the weights randomly
# such that the sum of all the small sets is > the weight of the big subset
# but the small subsets do have individual weights << than the big subset
subsets_and_weights = [(subsets[0], big_subset_weight)]
minimum_weight = big_subset_weight//(len(subsets)-1)*2
#maximum_weight_ratio = big_subset_weight/len(subsets[0])
#if(maximum_weight < minimum_weight):
#    raise ValueError(f"The range for subset weights is invalid: minimum weight {minimum_weight} > maximum weight {maximum_weight}")
# set weights
# TODO: make sure that the sum(small subset weights > big_subset_weight)
for subset in subsets[1:]:
    maximum_weight_ratio = big_subset_weight / len(subsets[0])
    curr_min = minimum_weight
    while minimum_weight > int(maximum_weight_ratio * len(subset)):
        maximum_weight_ratio *= 1.1
    weight = random.randint(curr_min, int(maximum_weight_ratio * len(subset)))
    subsets_and_weights.append((subset, weight))

# Add duplicates of sets and weights with higher values
originalSets = len(subsets_and_weights)
number_of_duplicates = random.randint(2, 500 - originalSets) # starting at 2 since we add an empty set later
for i in range(number_of_duplicates):
    rand_index = random.randrange(1, originalSets-1) # ensure we do not copy an already copied set which would make our min weight too large
    minimum_weight = subsets_and_weights[rand_index][1]
    maximum_weight_ratio = 1.3
    curr_min = minimum_weight
    curr_max = int(maximum_weight_ratio * minimum_weight)
    while curr_min > curr_max:
        maximum_weight_ratio *= 1.1
        curr_max = int(maximum_weight_ratio * minimum_weight)
    duplicate_weight = random.randint(curr_min, curr_max)
    subsets_and_weights.append((subsets_and_weights[rand_index][0], duplicate_weight))

# Add the empty set
emptySubset = []
emptyWeight = random.randint(curr_min, curr_max)
subsets_and_weights.append((emptySubset, emptyWeight))

if len(subsets_and_weights) > 500:
    raise ValueError("Too many subsets: ".format(len(subsets_and_weights)))

# save the input
output.write(str(size) + "\n")
output.write(str(len(subsets_and_weights)) + "\n")
i = 0
while i < len(subsets_and_weights):
    output.write(str(subsets_and_weights[i][0]) + "\n")
    output.write(str(subsets_and_weights[i][1]) + "\n")
    i+=1