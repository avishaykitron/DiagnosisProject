import csv
from DiagnosisProject.LinearCombinationComponent import LinearCombinationComponent

class Graph:

    """
    A graph
    Will resemble a graph of components of linear combination (form: a0*x0+a2*x2+...+an-1*xn-1+b)
    """

    def __init__(self, csv_path):
        self.id_to_comp = {}
        self.id_to_inputs = {}
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

                for key, value in self.id_to_comp.items():
                    print("{} : {}".format(key, value.to_string()))
                for key, value in self.id_to_inputs.items():
                    print("{} : {}".format(key, value))

        except FileNotFoundError:
            print("Unable to read {}".format(csv_path))

    # Run inputs through the graph and returns a list of tuples (comp_id, SYSOUT value) with all SYSOUTs
    def run_in_graph(self, sysins):
        pass

    # generate valid samples (based on the current graph) with random inputs
    def generate_samples(self, number_of_sample):
        pass

    # Returns a new Graph with an implanted "bug" in comp
    def plant_bug(self, comp):
        pass

    # Returns a string representation of the graph
    def to_string(self):
        pass


example_graph = Graph("DiagnosisProject\\example_graph.csv")
example_graph.run_in_graph([0, 1, 2, 3, 4, 5])
