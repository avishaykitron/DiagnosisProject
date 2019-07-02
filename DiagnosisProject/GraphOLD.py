import csv
from LinearCombinationComponent import LinearCombinationComponent
from random import randint
import copy

class Graph:

    """
    A graph
    Will resemble a graph of components of linear combination (form: a0*x0+a2*x2+...+an-1*xn-1+b)
    ASSUMPTION: If a component has a SYSIN then it accepts only one input (->[comp]->)
    """

    def __init__(self, csv_path, obs_low_bound=1, obs_high_bound=2, debug=False):

        self.id_to_comp = {}
        self.id_to_inputs = {}
        self.obs_low_bound = obs_low_bound
        self.obs_high_bound = obs_high_bound


        try:
            with open(csv_path, 'r') as f:
                reader = csv.reader(f)
                content = list(reader)
                # Add V
                for count, stringed_comp in enumerate(content[0][1:-1]):
                    # create a component
                    new_comp = LinearCombinationComponent(None, None)
                    new_comp.update_from_string(stringed_comp)
                    self.id_to_comp[count+1] = new_comp

                # Add E (the inputs of each component)
                for count, stringed_comp in enumerate(content[0][1:-1]):
                    comp_id = count + 1
                    inputs = ['SYSIN']*len(self.id_to_comp[comp_id].multipliers)   # Empty list for the inputs, assumes all inputs are SYSINS
                    for col_index, is_input in enumerate(content[comp_id][1:-1]):
                        if int(is_input) > -1:
                            possible_input_index = col_index+1
                            inputs[int(is_input)] = possible_input_index
                    self.id_to_inputs[comp_id] = inputs

                # Save a list of SYSOUTs (id of component whose output is visible)
                self.sysouts = []
                for count, is_sysout in enumerate(content[-1][1:-1]):
                    if is_sysout == "TRUE":
                        self.sysouts.append(count + 1)
                self.sysouts.reverse() # ASSUMPTION: final SYSOUT is at last column of components in CSV

                # Print for debug
                if debug:
                    for key, value in self.id_to_comp.items():
                        print("{} : {}".format(key, value.to_string()))
                    for key, value in self.id_to_inputs.items():
                        print("{} : {}".format(key, value))
                    print("SYSOUTS: {}".format(self.sysouts))

        except FileNotFoundError:
            print("Unable to read {}".format(csv_path))

    # Returns a dictionary of (id : list(comps)) representing minimal subsystems
    def get_subsystems(self, debug=False):
        subsystems = {}
        for out_comp_id in self.sysouts:
            curr_subsystem = [out_comp_id]
            for inp in self.id_to_inputs[out_comp_id]:
                curr_subsystem.extend(self.expand_comp(inp))
            subsystems[str.join('_', ["{}".format(i) for i in curr_subsystem])] = curr_subsystem

        if debug:
            for key, value in subsystems.items():
                print("{} : {}".format(key, value))
        return subsystems

    # Helper for get_subsystems
    def expand_comp(self, cid):
        if cid == "SYSIN" or cid in self.sysouts:
            return []

        ans = [cid]
        for inp in self.id_to_inputs[cid]:
            if inp != "SYSIN" and inp not in self.sysouts:
                ans.extend(self.expand_comp(inp))

        return ans

    # Run inputs through the graph and returns a list of tuples (comp_id, SYSOUT value) with all SYSOUTs
    def run_in_graph(self, sysins):
        ans = []
        #curr_ins = list(sysins.values())
        curr_ins = sysins
        already_calculated = {}
        for out_comp_id in self.sysouts:
            result, _, already_calculated = self.calc_subgraph(out_comp_id,
                                                               curr_ins,
                                                               already_calculated)
            ans.append((out_comp_id, result))
        return ans, already_calculated

    # Helper for run_in_graph - calc/expand MAKE SURE sysins and memoization are updated
    # bug - sysin values are incorrect - - 26/6
    def calc_subgraph(self, comp_id, sysins, memoization, prev_id=-1):
        if comp_id == "SYSIN":
            return sysins[str(prev_id)], sysins, memoization
        elif comp_id in memoization.keys():
            return memoization[comp_id], sysins, memoization
        else:
            calced_ins = []
            for inp in self.id_to_inputs[comp_id]:
                res, sysins, memoization = self.calc_subgraph(inp, sysins, memoization, comp_id)
                calced_ins.append(res)
            c_ans = self.id_to_comp[comp_id].calc_value(calced_ins)
            memoization[comp_id] = c_ans
            return c_ans, sysins, memoization

    # generate valid samples (based on the current graph) with random inputs
    def generate_samples(self, number_of_sample):
        all_observations = []
        subsystems = self.get_subsystems()

        number_of_sysins_to_generate = 0
        for ins in self.id_to_inputs.values():
            number_of_sysins_to_generate += sum([1 if x == 'SYSIN' else 0 for x in ins])

        for index in range(number_of_sample):
            # form: ['1':70, '2':71, '3':72, '4':73, '5':74]
            curr_ins = dict(zip(
                [str(i+1) for i in range(number_of_sysins_to_generate)],
                [randint(self.obs_low_bound,self.obs_high_bound) for i in range(number_of_sysins_to_generate)]))

            partial_observations, already_calculated = self.run_in_graph(curr_ins) # holds out_comp_id and result
            for obs in reversed(partial_observations):
                to_add_obs = ["SUBSYSTEM", ['input components'], [], 'output comp id', -1]
                to_add_obs[3] = obs[0]
                to_add_obs[4] = obs[1]
                for ss in subsystems.keys():
                    if str(obs[0]) == ss.split("_")[0]:
                        to_add_obs[0] = ss
                        to_add_obs[1] = self.get_ins_of_subsystems(ss)

                        for inp in to_add_obs[1]:
                            if (inp == "SYSIN"):
                                #continue
                                to_add_obs[2].append(curr_ins[ss])   # ADDED for full probing management - 26/6
                            #elif self.id_to_inputs[inp] != ['SYSIN']:
                            elif inp not in subsystems[ss]: # NEW
                                to_add_obs[2].append(already_calculated[inp])
                            else: # TODO ouput of prev if single comp (3), input comp else (2)
                                to_add_obs[2].append(curr_ins[str(inp)]) # NEW
                                #to_add_obs[2].append(id_to_ins[inp])

                all_observations.append(to_add_obs)
        return all_observations

    # generate invalid samples (based on buggy graph) with random inputs.
    # Returns the observations and ids of buggy comps
    def generate_buggy_samples(self, number_of_samples, number_of_bugs=1):
        if number_of_bugs > len(self.id_to_comp.keys()):
            print("Too many requested bugs ({})".format(number_of_bugs))
            return [], []
        ids = [randint(1, len(self.id_to_comp.keys())) for _ in range(number_of_bugs)]
        buggy_graph = self.plant_bug(ids)
        buggy_obs = buggy_graph.generate_samples(number_of_samples)
        return buggy_obs, ids

    # Returns a new Graph with an implanted "bug" in comp
    def plant_bug(self, comp_ids):
        buggy_graph = copy.deepcopy(self)
        for cid in comp_ids:
            old_comp = self.id_to_comp[cid]
            defected = copy.deepcopy(old_comp)
            new_ms = []
            for m in defected.multipliers:
                new_ms.append(2 * m)
            defected.update_from_ints(new_ms, defected.b + 1)
            buggy_graph.id_to_comp[cid] = defected
        return buggy_graph

    # Export graph & valid observations details into a file (for later use)
    def export_to_file(self, reg_observations, buggy_observations, defect_ids, path="example_graph_2_output.txt"):
        with open(path, "w+") as f:
            f.write("Subsystems:\n")

            subsystems = self.get_subsystems()
            for ss in subsystems:
                f.write("{}\n".format(ss))

            f.write("\nSYSINS:\n")
            ins = []
            for comp_id in self.id_to_comp.keys():
                if "SYSIN" in self.id_to_inputs[comp_id]:
                    ins.append(comp_id)
            f.write(str.join(", ", [str(i) for i in ins]))

            f.write("\n\nSYSOUTS:\n")
            f.write(str.join(", ", [str(i) for i in self.sysouts]))

            f.write("\n\nTotalRegularObservations:\n{}".format(int(len(reg_observations) / len(self.sysouts))))

            f.write("\n\nNormalObservations:\n")
            for obs in reg_observations:
                f.write("{}\n".format(obs))

            f.write("\nTotalBuggyObservations:\n{}".format(int(len(buggy_observations) / len(self.sysouts))))

            f.write("\n\nBuggyObservations:\n")
            for bobs in buggy_observations:
                f.write("{}\n".format(bobs))
            f.write('\nBuggyIds\n')
            f.write(str.join(", ", [str(d) for d in defect_ids]))

            f.write("\n\nMinRange:\n")
            f.write(str(int(self.obs_low_bound)))
            f.write("\n\nMaxRange:\n")
            f.write(str(int(self.obs_high_bound)))
            f.write("\n")




    # Return ins of the subsystems (ids of comps that accepts the sub-system's inputs)
    def get_ins_of_subsystems(self, sub_system_id, curr_c=-1, iteration=0):
        out_comp = curr_c
        if out_comp == -1:
            out_comp = int(str.split(sub_system_id, "_")[0])
        ret = []
        # added the OR for full probing management - 26/6
        if 'SYSIN' in self.id_to_inputs[out_comp] or (out_comp in self.sysouts and iteration>0):
            ret = ['SYSIN'] if iteration == 0 else [out_comp]
        else:
            for i in self.id_to_inputs[out_comp]:
                ret.extend(self.get_ins_of_subsystems(sub_system_id, curr_c=int(i), iteration=iteration+1))
        return ret

    # Returns a string representation of the graph
    def to_string(self):
        for key, value in self.id_to_comp.items():
            print("{} : {}".format(key, value.to_string()))
        for key, value in self.id_to_inputs.items():
            print("{} : {}".format(key, value))
        print("SYSOUTS: {}".format(self.sysouts))


example_graph = Graph("C:\\Users\\landauof\\Desktop\\DiagnosisProject\\DiagnosisProject\\example_graph_3.csv", debug=False)
#example_graph.get_subsystems(debug=False)
obs = example_graph.generate_samples(5)
# buggy_example = example_graph.plant_bug([1, 2])
# print('EXAMPLE')
# example_graph.to_string()
# print('BUGGY')
# buggy_example.to_string()
bobs, def_ids = example_graph.generate_buggy_samples(5)
example_graph.export_to_file(reg_observations=obs, buggy_observations=bobs, defect_ids=def_ids,  path="example_graph_3_output.txt")
