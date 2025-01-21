import random
import pygame
from organism import Organism

hex_chars = list("1234567890abcdef")


def generate_genes(n) -> list[str]:
    return ["".join(random.choice(hex_chars) for i in range(2))
            for i in range(n)]


def fitness(organism) -> int:
    # put your fitness function right here
    distance_to_corner = 60 - organism.pos.x
    score = 1 - (distance_to_corner / 30)
    return score


def cross_over(game, organisms) -> list[Organism]:

    if len(organisms) == 0:
        raise Exception("cannot reproduce 0 organisms")

    new_organisms = []

    for i in range(150):
        parents = random.choices(organisms, k=2)
        new_genes = []

        for g1, g2 in zip(parents[0].genes, parents[1].genes):

            if random.randint(0, 50) == 5:
                new_genes.append(random.choice([g1, g2])[::-1])
            else:
                new_genes.append(random.choice([g1, g2]))

        position = pygame.Vector2(
            random.randint(0, game.grid_size),
            random.randint(0, game.grid_size)
        )

        new_organisms.append(Organism(position, game, new_genes))

    return new_organisms
