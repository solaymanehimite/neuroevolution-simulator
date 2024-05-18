import random

hex_chars = list("1234567890abcdef")


def generate_gene():
    return "".join(random.choice(hex_chars) for i in range(6))
