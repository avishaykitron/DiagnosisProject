# Imports
from LinearCombinationComponent import LinearCombinationComponent
from random import randint
from Graph import  Graph
import csv

import re

# Constants
MULTIPLIER_BOUND = 2    # multipliers in components will be in [-MULTIPLIER_BOUND, MULTIPLIER_BOUND]
B_BOUND = 5     # b in components will be in [-B_BOUND, B_BOUND]

DICT_HASH = {}
PATH = "C:\\Users\\אבישי\\Downloads\\DiagnosisProject\\DiagnosisProject\\example_graph_2_output.txt"
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

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

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


def getKeysByValue(dictOfElements, valueToFind):
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            return item[0]
    return 0


def generate_hash():
    file = open(PATH, "r")
    lines = []
    for line in file :
        lines.append(line[:-1])
    subsystems = lines[lines.index('Subsystems:') : lines.index('')][1:]
    for x in range(1, len(subsystems)+1):
        DICT_HASH["hash{0}".format(x)] = {}


def update_hash_tabels():
    file = open(PATH, "r")
    lines = []
    for line in file :
        lines.append(line[:-1])
    observations = lines[lines.index('NormalObservations:') : lines.index('TotalBuggyObservations:')][1: -1]
    subsystems = lines[lines.index('Subsystems:') : lines.index('')][1:]
    sys_ins = lines[lines.index('SYSINS:'): lines.index('SYSOUTS:')][1: -1]
    sys_outs = lines[lines.index('SYSOUTS:'): lines.index('TotalRegularObservations:')][1: -1]
    total_reg_obs = lines[lines.index('TotalRegularObservations:') : lines.index('NormalObservations:')][1: -1]
    total_bug_obs = lines[lines.index('TotalBuggyObservations:') : lines.index('BuggyObservations:')][1: -1]
 #   min_range = lines[lines.index('MinRange:') : lines.index('MaxRange:')][1: -1]
  #  max_range = lines[-2:-1]

    indexes_subsystems = {}
    i =1
    for obs in observations:
        b = re.split("[\[\],]" , obs)
        sub = b[1][1:-1].split('_')
        index = 0
        if sub in indexes_subsystems.values():
            index = getKeysByValue( indexes_subsystems ,sub)
        else :
            indexes_subsystems[i] = sub
            index = i
            i = i+ 1
        in_1= [i for i, n in enumerate(b) if n == ' '][1]
        in_2= [i for i, n in enumerate(b) if n == ''][2]
        inputs = b[in_1+1 : in_2]
        outs = b[-2]
        str_in = ', '.join(inputs)
        DICT_HASH["hash{0}".format(int(index))][str_in] = outs
    bugs_components = []
    bug_obs = lines[lines.index('BuggyObservations:'): lines.index('BuggyIds')][1: -1]
    hits = 0
    for obs in bug_obs:
        b = re.split("[\[\],]", obs)
        sub = b[1][1:-1].split('_')
        index = 0
        if sub in indexes_subsystems.values():
            index = getKeysByValue( indexes_subsystems ,sub)
        else:
            indexes_subsystems[i] = sub
            index = i
            i = + 1
        in_1 = [i for i, n in enumerate(b) if n == ' '][1]
        in_2 = [i for i, n in enumerate(b) if n == ''][2]
        inputs = b[in_1 + 1: in_2]
        outs = b[-2]
        str_in = ', '.join(inputs)
        if str_in in DICT_HASH["hash{0}".format(int(index))] and DICT_HASH["hash{0}".format(int(index))][
            str_in] != outs:
            hits = hits + 1
            if index not in bugs_components:
                bugs_components.append(index)

    if len(bugs_components) == 0:
        daignosis = []
    else:
        daignosis = indexes_subsystems[bugs_components[0]]
        for x in bugs_components:
            daignosis = intersection(daignosis, indexes_subsystems[x])
        print(daignosis)

    num_comp = len('_'.join(subsystems).split('_'))
    num_sys_ins = len(''.join(sys_ins).split(', '))
    num_sys_outs = len(''.join(sys_outs).split(', '))
    num_reg_obs = int(''.join(total_reg_obs))
    num_buggy_obs = int(''.join(total_bug_obs))
    num_input_per_comp = 3
    num_bugs = 1
    input_min_range = 1 #int(''.join(min_range))
    input_max_range = 2#int(''.join(max_range))
    sucess_Rate = hits / num_buggy_obs
    extra_comp = num_comp - len(daignosis)

    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = ['num_comp', 'num_sys_ins', 'num_sys_outs', 'num_reg_obs', 'num_buggy_obs', 'num_input_per_comp',
                      'num_bugs', 'input_min_range', 'input_max_range', 'sucess_Rate', 'extra_comp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Components|#SYSINS|#SYSOUTS|#REGOBS|#INPUTSPERCOMP|#BUGS|#INRANGE|#BUGGYOBS|SUCCESSRATE|#EXTRACOMP
  #      writer.writeheader()
        writer.writerow({'num_comp': num_comp, 'num_sys_ins': num_sys_ins , 'num_sys_outs' : num_sys_outs ,'num_reg_obs' : num_reg_obs,
                         'num_buggy_obs' : num_buggy_obs, 'num_input_per_comp' : num_input_per_comp ,'num_bugs' :num_bugs
                            , 'input_min_range' :input_min_range , 'input_max_range' : input_max_range, 'sucess_Rate' : sucess_Rate, 'extra_comp' : extra_comp})


generate_hash()
update_hash_tabels()
