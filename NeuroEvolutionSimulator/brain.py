import numpy as np


class Brain:
    def __init__(self, genes):
        self.weights = np.zeros((1, 4))
        for i, gene in enumerate(genes):
            decimal_value = int(gene, 16)  # Convert hex to decimal
            normalized_value = decimal_value / (
                16**6 - 1
            )  # Scale to be between 0 and 1
            self.weights[0, i] = normalized_value

    def step_function(self, x):
        return np.where(x > 0.5, 1, 0)

    def feed(self, inputs):
        output = np.dot(inputs, self.weights)
        output = self.step_function(output)
        return output
