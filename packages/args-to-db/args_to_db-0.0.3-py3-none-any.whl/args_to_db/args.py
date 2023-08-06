import itertools

def all_combinations_of_array(array):
    combinations = []
    for element_count in range(len(array) + 1):
        combinations += [list(tupl) for tupl in itertools.combinations(array, element_count)]
    return combinations


def all_combinations(*possible_args):
    if len(possible_args) == 1:
        array = possible_args[0]
    else:
        array = possible_args
    
    return all_combinations_of_array(array)
