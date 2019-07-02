import numpy as np
import itertools
from LinearCombinationComponent import LinearCombinationComponent

from GenerationRelatedStuff import parse_file_to_list_of_lines

class Diagnoser:
    """
    Component that can process a list of observations and buggy observation and return a diagnosis.
    Each observation is in the form of [subsystem is, ids of input components, inputs, id of output component, output]
    """
    def __init__(self, list_of_observations):
        # Build equation systems for each subsystem
        subsystem_to_as = {}
        subsystem_to_b = {}
        self.subsystem_to_observations = {}

        for subsystem, input_comp_ids, input_vals, output_comp_id, output_value in list_of_observations:

            # Dictionaries of input-output for the regular implementation (for partially observed component)
            if subsystem not in self.subsystem_to_observations:
                self.subsystem_to_observations[subsystem] = {}
            self.subsystem_to_observations[subsystem][str(input_vals)] = output_value

            # Manage input that enters more than a single component
            unique_ins_and_vals = dict(zip(input_comp_ids, input_vals))
            input_comp_ids, input_vals = [k for k in unique_ins_and_vals], [v for v in unique_ins_and_vals.values()]

            if subsystem not in subsystem_to_as:
                subsystem_to_as[subsystem] = []
            subsystem_to_as[subsystem].append(input_vals)
            if subsystem not in subsystem_to_b:
                subsystem_to_b[subsystem] = []
            subsystem_to_b[subsystem].append(output_value)

        # Validate as and b for each subsystem
        if subsystem_to_b.keys() != subsystem_to_as.keys():
            Exception("Somehow the amount of input and output components isn't equal")

        # Build numpy arrays for equation solver
        subsystem_to_solver_input = {}
        self.subsystem_to_status = {}
        for subsystem in subsystem_to_as.keys():

            unique_ins = []     # Will contain, if possible, unique input values (prevent same equation in the solver)
            unique_ins_outs = []    # output of the unique equations

            for index, ins in enumerate(subsystem_to_as[subsystem]):
                if ins not in unique_ins:
                    unique_ins.append(ins)
                    unique_ins_outs.append(subsystem_to_b[subsystem][index])

            ins_for_solver = unique_ins     # list of lists
            outs_for_solver = unique_ins_outs    # list of numbers

            subsystem_to_solver_input[subsystem] = (ins_for_solver, outs_for_solver)
            self.subsystem_to_status[subsystem] = "PARTIAL"

        # Try to find the linear combination based on known observations
        self.subsystem_to_component = {}

        for subsystem in self.subsystem_to_status.keys():
            # To find all subgroups of possible equation systems
            indexes = set(range(len(subsystem_to_solver_input[subsystem][0])))
            requested_equation_number = len(subsystem_to_as[subsystem][0]) + 1   # +1 for b
            possible_equation_indexes = map(set, itertools.combinations(indexes, requested_equation_number))
            ins_for_solver, outs_for_solver = subsystem_to_solver_input[subsystem]

            for possible_equations in possible_equation_indexes:
                chosen_ins_for_solver = [ins_for_solver[i] for i in possible_equations]
                chosen_ins_for_solver = [i+[1] for i in chosen_ins_for_solver]  # +1 for b
                chosen_ins_for_solver = np.array(chosen_ins_for_solver)
                chosen_outs_for_solver = np.array([outs_for_solver[i] for i in possible_equations])

                try:
                    ans = np.linalg.solve(chosen_ins_for_solver, chosen_outs_for_solver)
                    self.subsystem_to_status[subsystem] = "FULL"
                    self.subsystem_to_component[subsystem] = LinearCombinationComponent([float("%.2f" % round(x, 4)) for x in ans[:-1]],
                                                                                        float("%.2f" % round(ans[-1], 4))) # the rounding prevents values like 11.99999999999996
                    print("SOLVED {}: Got {}".format(subsystem, self.subsystem_to_component[subsystem].to_string()))
                    break
                except np.linalg.LinAlgError:
                    pass

    # Accepts a list of observations (resembles a single observation of the system)
    # Returns a set of components = diagnosis
    def full_diagnosis(self, list_of_buggy_obs):
        # Validate we got one diagnosis per subsystem
        if set([obs[0] for obs in list_of_buggy_obs]) != self.subsystem_to_status.keys() or \
                len(list_of_buggy_obs) != len(self.subsystem_to_status.keys()):
            Exception("{} is not a valid observation of the system".format(list_of_buggy_obs))

        # Check what subsystems have a conflict
        conflicted_subsystems = []
        for obs in list_of_buggy_obs:
            if self.is_conflict(obs):
                conflicted_subsystems.append(obs[0])

        # Build the diagnosis
        ans = str.join('_', conflicted_subsystems)
        ans = ans.split('_')
        return list(set(ans))

    # Accepts a buggy observation (single subsystem) and returns if a conflict occurred
    def is_conflict(self, buggy_obs):
        # Get observation's data
        subsystem = buggy_obs[0]
        input_comp_ids = buggy_obs[1]
        input_vals = buggy_obs[2]
        output_val = buggy_obs[4]
        # Manage input that enters more than a single component
        unique_ins_and_vals = dict(zip(input_comp_ids, input_vals))
        input_comp_ids, input_vals = [k for k in unique_ins_and_vals], [v for v in unique_ins_and_vals.values()]

        if self.subsystem_to_status[subsystem] == "FULL":
            # Check if the input values fit in the linear combination. If False -> found a conflict
            return self.subsystem_to_component[subsystem].calc_value(input_vals) != output_val
        else:
            # If subsystem is not fully observed, use the method from the paper - if witnessed other observation
            # with different results then found a conflict
            return str(input_vals) in self.subsystem_to_observations[subsystem] and \
                    self.subsystem_to_observations[subsystem][str(input_vals)] != output_val

        # Gets a diagnosis (list of ids) and bug ids (list of ids) and returns number of hits
    def get_hits(self, buggy_ids, all_buggy_obs, number_of_subsystems):
        hits, all_extra_comp = 0, 0
        parsed_full_diagnosis = [all_buggy_obs[x:x + number_of_subsystems] for x in
                                 range(0, len(all_buggy_obs), number_of_subsystems)]
        for fd in parsed_full_diagnosis:
            diagnosis = self.full_diagnosis(fd)
            if any(x in diagnosis for x in buggy_ids):
                hits += 1
                all_extra_comp += len(
                    set(diagnosis) - set(buggy_ids))  # TODO: Make sure extra comp=0 if we have no hit
            else:
                pass
        return hits, all_extra_comp / len(parsed_full_diagnosis)


# a = np.array([[1, 1, 1],[1,2,1], [2,1,1]])
# b = np.array([5, 7, 7])
#
# print(np.linalg.solve(a,b))
#lines = parse_file_to_list_of_lines("ProblemDataset\example_graph_2_1_250_0-9.txt")
# lines = parse_file_to_list_of_lines("ProblemDatasetLG\\SystemModule_1_10_0-9.txt")
# observations = lines[lines.index('NormalObservations:'): lines.index('TotalBuggyObservations:')][1: -1]
# observations = [eval(obs) for obs in observations]
# diagnoser = Diagnoser(observations)
# print(diagnoser.full_diagnosis([
#     ['2_6', [6], [3], 2, 99],
#     ['3', ['SYSIN'], [3], 3, 5],
#     ['5_1', [1], [3], 5, 25],
#     ['7', ['SYSIN'], [9], 7, 15],
#     ['10', ['SYSIN'], [3], 10, 2],
#     ['11_4', [4, 10], [9, 3], 11, 178],
#     ['12_8', [3, 8], [3, 9], 12, -550],
#     ['13_1', [7, 1], [9, 3], 13, 79],
#     ['14_4', [4, 3], [9, 3], 14, 360],
#     ['16_4', [7, 4], [9, 9], 16, -136],
#     ['17', ['SYSIN'], [3], 17, 16],
#     ['18_9', [9, 7], [3, 9], 18, -111],
#     ['19_15_4', [15, 4], [3, 9], 19, -92],
#     ['20_8', [17, 8], [3, 9], 20, -477],
# ]))
