# Imports
from LinearCombinationComponent import LinearCombinationComponent
from random import randint

# Constants
MULTIPLIER_BOUND = 3    # multipliers in components will be in [-MULTIPLIER_BOUND, MULTIPLIER_BOUND]
B_BOUND = 5     # b in components will be in [-B_BOUND, B_BOUND]


# Gets number of components to create, number of inputs each component has (single option) and a flag for debug printing
def generate_random_components(number_of_components=3, number_of_inputs_in_component=1, log_messages=True):
    ret = []

    for index in range(number_of_components):
        new_multipliers = [randint(-MULTIPLIER_BOUND, MULTIPLIER_BOUND) for _ in range(number_of_inputs_in_component)]
        new_comp = LinearCombinationComponent(multipliers=new_multipliers, b=randint(-B_BOUND, B_BOUND))

        if log_messages:
            print("Generated new component: {}".format(new_comp.to_string()))

        ret.append(new_comp)

    return ret


