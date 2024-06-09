import random
import pygame
from organism import Organism


hex_chars = list("1234567890abcdef")
input_labels = [
    "x",
    "y",
    "tick",
]
output_labels = ["right", "left", "down", "up"]


def generate_gene():
    return "".join(random.choice(hex_chars) for i in range(2))


def generate_genes(n):
    return [generate_gene() for i in range(n)]


def fitness(organism):
    if organism.pos.y > 50 and organism.pos.x > 50:
        return True
    return False


def cross_over(game, organisms):
    new_organisms = {}
    for i in range(100):
        organism_1 = random.choice(organisms)
        organism_2 = random.choice(organisms)
        new_genes = []
        for gene_1, gene_2 in zip(organism_1.genes, organism_2.genes):
            if random.randint(0, 20) == 0:
                new_genes.append(random.choice([gene_1, gene_2])[::-1])
            new_genes.append(random.choice([gene_1, gene_2]))
        position = pygame.Vector2(
            random.randint(0, game.grid_size), random.randint(0, game.grid_size)
        )
        new_organisms[i] = Organism(position, game, new_genes)

    return new_organisms
