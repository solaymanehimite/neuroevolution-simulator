import pygame
import sys
import random

from organism import Organism
from ui_manager import UiManager
from utils import cross_over, fitness, generate_genes
from pygame.locals import QUIT, KEYDOWN, K_SPACE, SRCALPHA, K_TAB


class Game:

    def __init__(self):

        # pygame stuff
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()

        # game props
        self.generation_time = 0
        self.generation = 0
        self.succes_rate = 0
        self.score_sum = 0
        self.grid_size = 60
        self.organism_size = 600 / self.grid_size
        self.lifespan = 120
        self.organism_count = 150
        self.genes_count = 12

        self.map = []
        self.overlay = self.generate_fitness_overlay()
        self.ui_manager = UiManager()

        self.running = True
        self.spawn_organisms()

    def generate_fitness_overlay(self):
        overlay = pygame.Surface((self.grid_size, self.grid_size), SRCALPHA)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                org = Organism(pygame.Vector2(i, j), self, generate_genes(12))
                color = (255, 0, 0) if fitness(org) > 0.5 else (0, 0, 0)
                overlay.set_at((i, j), color)

        overlay.set_colorkey((0, 0, 0))
        overlay.set_alpha(50)
        overlay = pygame.transform.scale(
            overlay,
            (600, 600),
        )
        return overlay.convert_alpha()

    def spawn_organisms(self):
        for i in range(150):
            x, y = [random.randint(0, self.grid_size),
                    random.randint(0, self.grid_size)]

            self.map.append(Organism(pygame.Vector2(
                x, y), self, generate_genes(12)))

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:
                    self.running = not self.running
                if ev.key == K_TAB:
                    self.ui_manager.toggle_info_panel()

    def regerenate_organisms(self):
        self.generation_time = 0
        self.generation += 1

        new_map = []
        for organism in self.map:
            if fitness(organism) > 0.5:
                new_map.append(organism)

        self.map = cross_over(self, new_map)

    def update(self):
        self.ui_manager.simulation_info["gen"] = self.generation
        self.ui_manager.simulation_info["scs"] = int((
            self.succes_rate / self.organism_count) * 100)
        self.ui_manager.simulation_info["scr"] = f"{self.score_sum / self.organism_count:0.2f}"

        self.succes_rate = 0
        self.score_sum = 0

        if self.running:
            self.generation_time += 1

        if self.generation_time > 120:
            self.regerenate_organisms()

        self.ui_manager.update()

    def render(self):
        self.screen.fill((0, 0, 0))

        for organism in self.map:
            if self.running:
                organism.update()
            self.score_sum += fitness(organism)
            if fitness(organism) > 0.5:
                self.succes_rate += 1
            organism.render()

        self.screen.blit(self.overlay, (0, 0))
        self.ui_manager.render(self.screen)

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()


if __name__ == "__main__":
    Game().run()
