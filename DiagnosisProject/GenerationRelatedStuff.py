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
def generate_instance_file(graph_path, num_reg_observations, num_buggy_observations, num_defect, high, low, out_path):
    graph = Graph(csv_path=graph_path, obs_low_bound=low, obs_high_bound=high)

    reg_obs = graph.generate_samples(num_reg_observations)
    buggy_obs, ids = graph.generate_buggy_samples(num_buggy_observations, number_of_bugs=num_defect)

    graph.export_to_file(reg_obs, buggy_obs, ids, path=out_path)


def get_keys_by_value(dict_of_elements, value_to_find):
    list_of_items = dict_of_elements.items()
    for item in list_of_items:
        if item[1] == value_to_find:
            return item[0]
    return 0


# Function that parse a file to list of lines.
def parse_file_to_list_of_lines(path):
    file = open(path, "r")
    lines = []
    for line in file:
        lines.append(line[:-1])
    return lines


# Function that generate hash table for each sub-system.
def generate_hash(lines):
    subsystems = lines[lines.index('Subsystems:'): lines.index('')][1:]
    for x in range(1, len(subsystems)+1):
        DICT_HASH["hash{0}".format(x)] = {}


# Function that takes the normal observation, and update the hash tables.
def update_normal_obs(lines):
    observations = lines[lines.index('NormalObservations:'): lines.index('TotalBuggyObservations:')][1: -1]
    i = 1
    indexes_subsystems = {}
    for obs in observations:
        str_in, outs, index, i = parse_line_of_observation(obs, indexes_subsystems, i)
        DICT_HASH["hash{0}".format(int(index))][str_in] = outs

    return indexes_subsystems


# Function that gets suspect observation and check if it abnormal.
# In case that there is abnormal observation, we create diagnosis, calculates hits, and return them.
def generate_diagnosis(lines, indexes_subsystems):
    subsystems = lines[lines.index('Subsystems:'): lines.index('')][1:]
    bugs_components = []
    bug_obs = lines[lines.index('BuggyObservations:'): lines.index('BuggyIds')][1: -1]
    hits = 0
    is_there_hits = 0
    counter = 1
    for obs in bug_obs:
        str_in, outs, index, i = parse_line_of_observation(obs, indexes_subsystems, 1)
        if str_in in DICT_HASH["hash{0}".format(int(index))] and DICT_HASH["hash{0}".format(int(index))][str_in]!= outs:
            if is_there_hits == 0:
                hits = hits + 1
                is_there_hits = 1
            if index not in bugs_components:
                bugs_components.append(index)
        if counter % len(subsystems) == 0:
            is_there_hits = 0
        counter = counter + 1
    diagnosis = []
    if len(bugs_components) != 0:
        for x in bugs_components:
            diagnosis = list(dict.fromkeys(diagnosis + indexes_subsystems[x]))

    return diagnosis, hits


# Function that write the diagnosis and the properties of the system to results file.
def write_diagnosis_to_result(lines, diagnosis, hits):
    subsystems = lines[lines.index('Subsystems:'): lines.index('')][1:]
    sys_ins = lines[lines.index('SYSINS:'): lines.index('SYSOUTS:')][1: -1]
    sys_outs = lines[lines.index('SYSOUTS:'): lines.index('TotalRegularObservations:')][1: -1]
    total_reg_obs = lines[lines.index('TotalRegularObservations:'): lines.index('NormalObservations:')][1: -1]
    total_bug_obs = lines[lines.index('TotalBuggyObservations:'): lines.index('BuggyObservations:')][1: -1]
    min_range = lines[lines.index('MinRange:'): lines.index('MaxRange:')][1: -1]
    buggy_ids = lines[lines.index('BuggyIds'):lines.index('MinRange:')][1: -1]
    max_range = lines[-1:]
    num_comp = '_'.join(subsystems).split('_')
    num_comp = len(list(dict.fromkeys(num_comp)))
    num_sys_ins = len(''.join(sys_ins).split(', '))
    num_sys_outs = len(''.join(sys_outs).split(', '))
    num_reg_obs = int(''.join(total_reg_obs))
    num_buggy_obs = int(''.join(total_bug_obs))
    num_input_per_comp = 3
    num_bugs = len(list(dict.fromkeys(''.join(buggy_ids).split(', '))))
    input_min_range = int(''.join(min_range))
    input_max_range = int(''.join(max_range))
    sucess_rate = hits / num_buggy_obs
    extra_comp = len(diagnosis) - num_bugs

    with open('results.csv', 'a', newline='') as csvfile:
        fieldnames = ['num_comp', 'num_sys_ins', 'num_sys_outs', 'num_reg_obs', 'num_buggy_obs', 'num_input_per_comp',
                      'num_bugs', 'input_min_range', 'input_max_range', 'sucess_Rate', 'extra_comp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Components|#SYSINS|#SYSOUTS|#REGOBS|#INPUTSPERCOMP|#BUGS|#INRANGE|#BUGGYOBS|SUCCESSRATE|#EXTRACOMP
        writer.writerow({'num_comp': num_comp, 'num_sys_ins': num_sys_ins , 'num_sys_outs' : num_sys_outs ,'num_reg_obs' : num_reg_obs,
                         'num_buggy_obs' : num_buggy_obs, 'num_input_per_comp' : num_input_per_comp ,'num_bugs' :num_bugs
                            , 'input_min_range' :input_min_range , 'input_max_range' : input_max_range, 'sucess_Rate' : sucess_rate, 'extra_comp' : extra_comp})


# Function that parse line of observation to inputs, output, and the index of the subsystem.
def parse_line_of_observation(obs, indexes_subsystems, i):
    b = re.split("[\[\],]", obs)
    sub = b[1][1:-1].split('_')
    if sub in indexes_subsystems.values():
        index = get_keys_by_value(indexes_subsystems, sub)
    else:
        indexes_subsystems[i] = sub
        index = i
        i = + 1
    in_1 = [i for i, n in enumerate(b) if n == ' '][1]
    in_2 = [i for i, n in enumerate(b) if n == ''][2]
    inputs = b[in_1 + 1: in_2]
    outs = b[-2]
    str_in = ', '.join(inputs)

    return str_in, outs, index, i


# graph_path, num_reg_observations, num_buggy_observations, num_defect, out_path
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 10, 10, 1,low=0, high=9, out_path="ProblemDatasetLG\\SystemModule_1_10_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 50, 10, 1,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_1_50_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 250, 10, 1,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_1_250_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 10, 10, 2,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_2_10_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 50, 10, 2,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_2_50_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 250, 10, 2,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_2_250_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 10, 10, 3,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_3_10_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 50, 10, 3,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_3_50_0-9.txt")
# generate_instance_file("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\SystemModule.csv", 250, 10, 3,low=0, high=9, out_path= "ProblemDatasetLG\\SystemModule_3_250_0-9.txt")
