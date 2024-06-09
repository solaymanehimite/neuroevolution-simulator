import numpy as np
from pygame import *


class Brain:
    def __init__(self, num_inputs, num_outputs, genes):
        num_genes = len(genes)
        self.weights = np.zeros((num_inputs, num_outputs))
        for i, gene in enumerate(genes):
            decimal_value = int(gene, 16)  # Convert hex to decimal
            normalized_value = decimal_value / (16**2 - 1)
            row_index = i % num_inputs  # Cycling through rows
            col_index = i % num_outputs  # Cycling through columns
            self.weights[row_index, col_index] = normalized_value

    def step_function(self, x):
        return np.where(x > 0.5, 1, 0)

    def feed(self, inputs):
        output = np.dot(inputs, self.weights)
        output = self.step_function(output)
        return output
