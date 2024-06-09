import random
import sys
import pygame

from pygame.locals import *
from organism import Organism
from utils import *


class Game:

    def __init__(self):

        # pygame stuff
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        # ui stuff
        self.font = pygame.font.Font("res/Monocraft.ttf", 18)
        self.char_width, self.char_height = self.font.size("A")
        self.char_height += 3
        self.sidebar_tab = "info"
        self.sidebar_padding = 600
        self.padding = 10
        self.tabs = {
            "info": [pygame.image.load("res/info.png"), pygame.Rect(600, 570, 67, 30)],
            "organism": [
                pygame.image.load("res/organism.png"),
                pygame.Rect(666, 570, 66, 30),
            ],
            "settings": [
                pygame.image.load("res/settings.png"),
                pygame.Rect(732, 570, 67, 30),
            ],
        }
        self.sidebar = True
        self.mouse_pos = [0, 0]
        pygame.mouse.set_visible(False)

        # game props
        self.generation_time = 0
        self.generation = 0
        self.grid_size = 60
        self.organism_size = 600 / self.grid_size
        self.lifespan = 120
        self.organism_count = 200
        self.genes_count = 12

        self.map = {}
        self.selected_organism_index = None
        self.selected_organism = None
        self.overlay = self.generate_fitness_overlay()

        self.running = True
        self.spawn_organisms()

    def generate_fitness_overlay(self):
        overlay = pygame.Surface((self.grid_size, self.grid_size), SRCALPHA)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                org = Organism(pygame.Vector2(i, j), self, generate_genes(12))
                color = (255, 0, 0) if fitness(org) else (0, 0, 0)
                overlay.set_at((i, j), color)

        overlay.set_colorkey((0, 0, 0))
        overlay.set_alpha(50)
        overlay = pygame.transform.scale(
            overlay,
            (600, 600),
        )
        return overlay.convert_alpha()

    def label(
        self, text, position, color=(255, 255, 255), anchor="topleft", back=False
    ):
        if back:
            render = self.font.render(text, False, color, (0, 0, 0))
        else:
            render = self.font.render(text, False, color)
        if anchor == "topleft":
            self.screen.blit(render, render.get_rect(topleft=position))
        elif anchor == "center":
            self.screen.blit(render, render.get_rect(center=position))

    def spawn_organisms(self):
        for i in range(100):
            x, y = random.randint(0, self.grid_size), random.randint(0, self.grid_size)
            self.map[i] = Organism(pygame.Vector2(x, y), self, generate_genes(12))

    def render_sidebar(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.sidebar:
            pygame.draw.rect(self.screen, (10, 10, 10), (600, 0, 200, 600))
            if self.sidebar_tab == "info":
                # sim info
                fps = f"{self.clock.get_fps():.0f}"
                info = [
                    ("oragnisms", self.organism_count),
                    ("genes", self.genes_count),
                    ("lifespan", self.lifespan),
                    ("framerate", fps),
                    ("generation", self.generation),
                ]
                for i, item in enumerate(info):
                    label, value = item
                    length = len(label) + len(str(value)) - 1
                    spaces = " " * (13 - length)
                    text = f"{label}:{spaces}{value}"
                    render = self.font.render(text, False, (255, 255, 255))
                    self.screen.blit(
                        render,
                        render.get_rect(
                            left=self.sidebar_padding + self.padding,
                            top=self.padding + (i * self.char_height),
                        ),
                    )

            if self.sidebar_tab == "organism":
                if self.selected_organism:

                    # id
                    self.label(
                        f"id: {self.selected_organism_index}",
                        (self.sidebar_padding + self.padding, self.padding),
                    )
                    # color
                    self.label(
                        "color:",
                        (
                            self.sidebar_padding + self.padding,
                            self.padding + self.char_height,
                        ),
                    )
                    self.label(
                        self.selected_organism.hex_color,
                        (
                            self.sidebar_padding + self.padding + self.char_width * 6,
                            self.padding + self.char_height,
                        ),
                        color=self.selected_organism.color,
                    )

                    # render gene header
                    self.label(
                        "genes:",
                        (
                            self.sidebar_padding + self.padding,
                            self.padding + self.char_height * 2,
                        ),
                    )

                    # render genes
                    for i, gene in enumerate(self.selected_organism.genes):
                        self.label(
                            gene,
                            (
                                self.sidebar_padding
                                + self.padding
                                + self.char_width
                                + self.char_width * 3 * (i % 4),
                                self.padding
                                + self.char_height * 3
                                + (i // 4) * self.char_height,
                            ),
                            color=(200, 200, 200),
                        )

                    # render brain header
                    self.label(
                        "Brain:",
                        (700, self.char_height * 10),
                        anchor="center",
                    )

                    # render brain
                    input_neurons, output_neurons, surf = (
                        self.selected_organism.render_brain()
                    )
                    surf.set_colorkey((0, 0, 0))
                    surf_pos = surf.get_rect(center=(700, self.char_height * 15))
                    self.screen.blit(surf, surf_pos)

            # sidebar buttons
            for tab in self.tabs:
                image, rect = self.tabs[tab]
                color = (10, 10, 10) if self.sidebar_tab == tab else (100, 100, 100)
                pygame.draw.rect(self.screen, color, rect)
                self.screen.blit(
                    image,
                    image.get_rect(center=(rect.centerx, rect.centery)),
                )

                if rect.collidepoint(self.mouse_pos) and mouse_pressed:
                    self.sidebar_tab = tab

    def check_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == KEYDOWN:
                if ev.key == K_SPACE:
                    self.running = not self.running

    def reset(self):
        self.generation += 1
        new_map = []
        for key in self.map:
            organism = self.map[key]
            if fitness(organism):
                new_map.append(organism)
        self.map = cross_over(self, new_map)
        self.generation_time = 0

    def update(self):

        # update mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos[0] += (mouse_pos[0] - self.mouse_pos[0]) / 2
        self.mouse_pos[1] += (mouse_pos[1] - self.mouse_pos[1]) / 2

        if self.running:
            self.generation_time += 1

        if self.selected_organism_index in self.map:
            self.selected_organism = self.map[self.selected_organism_index]

        if self.generation_time > 120:
            self.reset()

    def render_mouse(self):
        mouse_points = [
            self.mouse_pos,
            pygame.Vector2(self.mouse_pos[0] + 11, self.mouse_pos[1] + 12),
            pygame.Vector2(self.mouse_pos[0], self.mouse_pos[1] + 17),
        ]
        pygame.draw.polygon(
            self.screen,
            (0, 0, 0),
            mouse_points,
        )
        pygame.draw.polygon(
            self.screen,
            (255, 255, 255),
            mouse_points,
            1,
        )

    def render(self):
        self.screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        tile_pos = pygame.Vector2(
            mouse_pos[0] // self.organism_size, mouse_pos[1] // self.organism_size
        )

        # render organisms
        for key in self.map:
            organism = self.map[key]
            if self.running:
                organism.update()
            organism.render()
            if mouse_pressed and organism.pos == tile_pos:
                self.selected_organism_index = key

        self.render_sidebar()
        self.render_mouse()
        self.screen.blit(self.overlay, (0, 0))

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.render()


if __name__ == "__main__":
    Game().run()
