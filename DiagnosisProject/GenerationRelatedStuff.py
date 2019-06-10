# Imports
from LinearCombinationComponent import LinearCombinationComponent
from random import randint
from Graph import  Graph
import re

# Constants
MULTIPLIER_BOUND = 2    # multipliers in components will be in [-MULTIPLIER_BOUND, MULTIPLIER_BOUND]
B_BOUND = 5     # b in components will be in [-B_BOUND, B_BOUND]

DICT_HASH = {}

# Gets number of components to create, number of inputs each component has (single option) and a flag for debug printing
def generate_random_components(number_of_components=3, number_of_inputs_in_component=2, log_messages=False):
    ret = []

    for index in range(number_of_components):
        new_multipliers = [randint(-MULTIPLIER_BOUND, MULTIPLIER_BOUND) for _ in range(number_of_inputs_in_component)]
        new_comp = LinearCombinationComponent(multipliers=new_multipliers, b=randint(-B_BOUND, B_BOUND))

        if log_messages:
            print("Generated new component: {}".format(new_comp.to_string()))

        ret.append(new_comp)

    return ret


# Generates a file with subsystems' normal and buggy observations... (for Avishay)
def generate_instance_file(graph_path, num_reg_observations, num_buggy_observations, num_defect, out_path):
    graph = Graph(csv_path=graph_path)

    reg_obs = graph.generate_samples(num_reg_observations)
    buggy_obs, ids = graph.generate_buggy_samples(num_buggy_observations, number_of_bugs=num_defect)

    graph.export_to_file(reg_obs, buggy_obs, ids, path=out_path)


# c = generate_random_components()
# new_c = c[2].to_string()
# c[0].update_from_string(new_c)
# print(c[0].to_string())
#generate_instance_file("C:\\Users\\אבישי\\Downloads\\DiagnosisProject\\DiagnosisProject\\example_graph.csv", 5, 5, 2, "out_example_2")

def generate_hash():
    file = open("C:\\Users\\אבישי\\Downloads\\DiagnosisProject\\DiagnosisProject\\example_graph_output.txt", "r")
    lines = []
    for line in file :
        lines.append(line[:-1])
    subsystems = lines[lines.index('Subsystems:') : lines.index('')][1:]
    observations = lines[lines.index('NormalObservations:') : lines.index('TotalBuggyObservations:')][1: -1]
    bug_obs = lines[lines.index('BuggyObservations:') : lines.index('BuggyIds')][1: -1]
    for x in range(1, 10):
        DICT_HASH["hash{0}".format(x)] = {}

def update_hash_tabels():
    file = open("C:\\Users\\אבישי\\Downloads\\DiagnosisProject\\DiagnosisProject\\example_graph_output.txt", "r")
    lines = []
    for line in file :
        lines.append(line[:-1])
    observations = lines[lines.index('NormalObservations:') : lines.index('TotalBuggyObservations:')][1: -1]
    for obs in observations:
        b = re.split("[\[\],]" , obs)
        index = b[1][1]
        in_1= [i for i, n in enumerate(b) if n == ' '][1]
        in_2= [i for i, n in enumerate(b) if n == ''][2]
        inputs = b[in_1+1 : in_2]
        outs = b[-2]
        str_in = ', '.join(inputs)
        DICT_HASH["hash{0}".format(int(index))][str_in] = outs

def check_observation():
    file = open("C:\\Users\\אבישי\\Downloads\\DiagnosisProject\\DiagnosisProject\\example_graph_output.txt", "r")
    lines = []
    for line in file:
        lines.append(line[:-1])
    bug_obs = lines[lines.index('BuggyObservations:'): lines.index('BuggyIds')][1: -1]
    for obs in bug_obs:
        b = re.split("[\[\],]", obs)
        index = b[1][1]
        in_1= [i for i, n in enumerate(b) if n == ' '][1]
        in_2= [i for i, n in enumerate(b) if n == ''][2]
        inputs = b[in_1+1 : in_2]
        outs = b[-2]
        str_in = ', '.join(inputs)
        if str_in in DICT_HASH["hash{0}".format(int(index))]and DICT_HASH["hash{0}".format(int(index))][str_in] != outs:
            print("bad component: {0}".format(index))


generate_hash()
update_hash_tabels()
check_observation()