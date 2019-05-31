class LinearCombinationComponent:

    """
    A component in a system.
    Will resemble a linear combination (form: a0*x0+a2*x2+...+an-1*xn-1+b)
    """

    def __init__(self, multipliers, b):
        self.multipliers = multipliers
        self.b = b

    # Override multipliers and b using given ones (from string)
    def update_from_string(self, stringed_component):
        parsed_comps = [int(unit.split("*")[0]) for unit in stringed_component.split(" + ")]
        self.multipliers = parsed_comps[:-1]
        self.b = int(parsed_comps[-1])

    # Get a list of values for all xi and returns a number
    def calc_value(self, inputs):
        if len(inputs) != len(self.multipliers):
            Exception("Number of inputs is not equal to number of multipliers")
        return sum([a*x for a, x in zip(self.multipliers, inputs)])+self.b

    # Returns a string of "a0*x0+a1*x1+...+an*xn+b" with the values of ai & b
    def to_string(self):
        ans = ""
        for i, ai in enumerate(self.multipliers):
            ans += "{}*x{} + ".format(ai, i)
        return ans+"{}".format(self.b)

    # Gets a list of multipliers and b and updates own values
    def update_from_ints(self, n_multipliers, n_b):
        self.multipliers = n_multipliers
        self.b = n_b
