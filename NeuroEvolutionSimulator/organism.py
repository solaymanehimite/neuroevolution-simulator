import pygame


class Organism:

    def __init__(self, pos, game, genes=None):
        self.game = game
        self.genes = genes
        self.pos = pos

    def render(self):
        pygame.draw.rect(
            self.game.screen,
            (255, 255, 255),
            (
                self.pos.x * self.game.organism_size,
                self.pos.y * self.game.organism_size,
                self.game.organism_size,
                self.game.organism_size,
            ),
        )
