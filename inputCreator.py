import random

def set_creator(universal_set:list)-> list:
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
size = 999
big_subset_weight = 3*size//4


# build the universal set
universal_set = [i+1 for i in range(size)]
subsets = []

# create sets
subsets.extend(set_creator(universal_set))
subsets.extend(set_creator(subsets[0]))
print(subsets)

# Set the weights randomly
# such that the sum of all the small sets is > the weight of the big subset
# but the small subsets do have individual weights << than the big subset
subsets_and_weights = [(subsets[0], big_subset_weight)]
minimum_weight = big_subset_weight//(len(subsets)-1)
maximum_weight = big_subset_weight//2
if(maximum_weight < minimum_weight):
    raise ValueError(f"The range for sbset weights is invalid: minimum weight {minimum_weight} > maximum weight {maximum_weight}")
# set weights
for subset in subsets[1:]:
    weight = random.randint(minimum_weight, maximum_weight)
    subsets_and_weights.append((subset, weight))


# Add duplicates of sets and weights with higher values
number_of_duplicates = random.randint(1, 500 - len(subsets_and_weights))
for i in range(number_of_duplicates):
    rand_index = random.randrange(1, len(subsets_and_weights)-1)
    minimum_weight = subsets_and_weights[rand_index][1]
    duplicate_weight = random.randint(minimum_weight, maximum_weight)
    subsets_and_weights.append((subsets_and_weights[rand_index][0], duplicate_weight))

if len(subsets_and_weights)> 500 :
    raise ValueError(f"Too many subsets: {len(subsets_and_weights)}")
print(subsets_and_weights)


