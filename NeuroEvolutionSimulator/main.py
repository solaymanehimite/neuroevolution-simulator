import random
import sys
import pygame

from pygame.locals import *
from organism import Organism
from utils import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()

        self.map = {}
        self.generation_time = 0
        self.grid_size = 60
        self.organism_size = self.screen.get_width() / self.grid_size
        self.spawn_organisms()

    def spawn_organisms(self):
        for i in range(100):
            x, y = random.randint(0, self.grid_size), random.randint(0, self.grid_size)
            self.map[f"{x}, {y}"] = Organism(
                pygame.Vector2(x, y), self, generate_genes(4)
            )

    def check_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        for key in self.map:
            organism = self.map[key]
            organism.update()

        self.generation_time += 1

        if self.generation_time > 60:
            new_map = []
            for key in self.map:
                organism = self.map[key]
                if fitness(organism):
                    new_map.append(organism)
            self.map = cross_over(self, new_map)
            self.generation_time = 0

    def render(self):
        self.screen.fill((0, 0, 0))

        # render organisms
        for key in self.map:
            organism = self.map[key]
            organism.render()

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.render()


if __name__ == "__main__":
    Game().run()
