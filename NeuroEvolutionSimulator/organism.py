import pygame

from brain import Brain


class Organism:

    def __init__(self, pos, game, genes=False):
        self.game = game
        self.brain = Brain(3, 4, genes)
        self.genes = genes
        self.pos = pos

    def render(self):
        pygame.draw.rect(
            self.game.screen,
            (255, 255, 255) if not self.genes else pygame.Color("#" + self.genes[0]),
            (
                self.pos.x * self.game.organism_size + 1,
                self.pos.y * self.game.organism_size + 1,
                self.game.organism_size - 2,
                self.game.organism_size - 2,
            ),
        )

    def update(self):
        inputs = [
            1,
            self.pos.x / (self.game.grid_size - 1),
            self.pos.y / (self.game.grid_size - 1),
        ]
        outputs = self.brain.feed(inputs)
        if outputs[0]:
            self.pos.x += 1
        if outputs[1]:
            self.pos.x -= 1
        if outputs[2]:
            self.pos.y += 1
        if outputs[3]:
            self.pos.y -= 1

        self.pos.x = max(min(self.game.grid_size - 1, self.pos.x), 0)
        self.pos.y = max(min(self.game.grid_size - 1, self.pos.y), 0)
