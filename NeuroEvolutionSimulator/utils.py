import random
import pygame

from organism import Organism


hex_chars = list("1234567890abcdef")


def generate_gene():
    return "".join(random.choice(hex_chars) for i in range(6))


def generate_genes(n):
    return [generate_gene() for i in range(n)]


def fitness(organism):
    if organism.pos.x > 50:
        return True
    return False


def cross_over(game, organisms):
    new_organisms = {}
    for i in range(200):
        organism_1 = random.choice(organisms)
        organism_2 = random.choice(organisms)
        new_genes = random.choice([organism_1.genes, organism_2.genes])
        position = pygame.Vector2(
            random.randint(0, game.grid_size), random.randint(0, game.grid_size)
        )
        new_organisms[f"{int(position.x)},{int(position.y)}"] = Organism(
            position, game, new_genes
        )

    return new_organisms
