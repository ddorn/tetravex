#!/usr/bin/env python3

"""
generateur aléatoire :
    prendre les conditions et générer une grille complète et résolue


By Alexia Gross
"""

import random
import click


def gen(height, width, colors):
    """
    Generate a doable HEIGHTxWIDTH Tetravex puzzle with COLORS colors.
    """

    assert height > 1
    assert width > 1
    assert colors > 1

    size = height * width

    grille=[[0,0,0,0] for t in range (size)]  #4 couleurs pour une tuile
    c = colors - 1

    for i in range (size):
        colonne = i % width
        if width - 1 != colonne :
            grille[i][1] = grille[i+1][3]=random.randint(0, c)
        else:
            grille[i][1]= random.randint(0, c)
        if colonne==0:
            grille[i][3] = random.randint(0, c)

    for i in range (size):
        if i < (height - 1) * width:
            grille[i][2] = grille[i + width][0] = random.randint(0, c)
        else:
            grille[i][2]  = random.randint(0, c)
        if i < width:
            grille[i][0] = random.randint(0, c)

    random.shuffle(grille)

    return grille

@click.command()
@click.argument('height', default=4)
@click.argument('width', default=4)
@click.argument('colors', default=4)
def generate(height, width, colors):
    grid = gen(height, width, colors)

    # output on stdout
    print(width, height)
    print(colors)
    for t in grid:
        print(*t)

if __name__ == '__main__':
    generate()

