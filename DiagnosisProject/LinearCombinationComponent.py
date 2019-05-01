class LinearCombinationComponent:

    """
    A component in a system.
    Will resemble a linear combination (form: a0*x0+a2*x2+...+an-1*xn-1+b)
    """

    def __init__(self, multipliers, b):
        self.multipliers = multipliers
        self.b = b

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
