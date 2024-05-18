import sys

import pygame
from pygame.locals import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

    def check_events(self):
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.render()


if __name__ == "__main__":
    Game().run()
