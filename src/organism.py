import pygame
from pygame import *

from brain import Brain


class Organism:

    def __init__(self, pos, game, genes=False):
        self.game = game
        self.brain = Brain(3, 4, genes)
        self.genes = genes
        self.pos = pos
        self.inputs = []
        self.outputs = []
        self.get_color()

    def get_color(self):
        self.hex_color = "".join(self.genes[0:3])
        self.color = Color("#" + self.hex_color)

    def render(self):
        mouse_position = pygame.mouse.get_pos()
        pygame.draw.rect(
            self.game.screen,
            (255, 255, 255) if not self.genes else self.color,
            (
                self.pos.x * self.game.organism_size + 1,
                self.pos.y * self.game.organism_size + 1,
                self.game.organism_size - 2,
                self.game.organism_size - 2,
            ),
        )
        rect = Rect(
            self.pos.x * self.game.organism_size + 1,
            self.pos.y * self.game.organism_size + 1,
            self.game.organism_size - 2,
            self.game.organism_size - 2,
        )
        if rect.collidepoint(mouse_position[0], mouse_position[1]):
            pygame.draw.circle(self.game.screen, self.color,
                               rect.center, 10, 2)

    def render_brain(self) -> Surface:
        neuron_radius = 8
        weight_length = 120
        neuron_padding = 30
        surface = Surface(
            (
                neuron_radius * 4 + weight_length,
                (neuron_radius * 2 + neuron_padding)
                * max(self.brain.weights.shape[0],
                      self.brain.weights.shape[1]),
            )
        )

        input_neurons = []
        for i in range(self.brain.weights.shape[0]):
            neuron = self.inputs[i]
            position = (
                neuron_radius,
                (neuron_radius * 2 + neuron_padding) * i
                + neuron_radius
                + neuron_padding / 2,
            )
            draw.circle(
                surface,
                (255, 255, 255) if neuron >= 0.5 else (100, 100, 100),
                position,
                neuron_radius,
            )
            input_neurons.append(position)

        # output neurons
        output_neurons = []
        for i in range(self.brain.weights.shape[1]):
            neuron = self.outputs[i]
            position = (
                surface.get_width() - neuron_radius,
                (neuron_radius * 2 + neuron_padding) * i
                + neuron_radius
                + neuron_padding / 2,
            )
            draw.circle(
                surface,
                (255, 255, 255) if neuron >= 0.5 else (100, 100, 100),
                position,
                neuron_radius,
            )
            output_neurons.append(position)

        # render weights
        for i in range(self.brain.weights.shape[0]):
            for j in range(self.brain.weights.shape[1]):
                weight_color = (
                    (0, 255, 0) if self.brain.weights[i, j] > 0.5 else (
                        255, 0, 0)
                )
                draw.line(
                    surface,
                    weight_color,
                    input_neurons[i],
                    output_neurons[j],
                    2,
                )

        return input_neurons, output_neurons, surface

    def update(self):
        self.inputs = [
            1,
            self.pos.x / (self.game.grid_size - 1),
            self.pos.y / (self.game.grid_size - 1),
        ]
        self.outputs = self.brain.feed(self.inputs)

        if self.outputs[0] > 0.25:
            self.pos.x += 1
        if self.outputs[1] > 0.25:
            self.pos.x -= 1

        if self.outputs[2] > 0.25:
            self.pos.y += 1
        if self.outputs[3] > 0.25:
            self.pos.y -= 1

        self.pos.x = max(min(self.game.grid_size - 1, self.pos.x), 0)
        self.pos.y = max(min(self.game.grid_size - 1, self.pos.y), 0)
