#!/usr/bin/env python3

"""
Solver for Tetravex.


This is the main file for Tetravex solverm created as a group project
during Mathinfoly 2019. This script is used to solve them, and random puzzles
can be generated with gen.py, a pretty version of a game's data can be viewed
inside a terminal with output.py. On can also generate a tikz output with
tikz_out.py.

Convention for text representation of Tetrevex games:
    first line:
        two integers representing the width and height of the board
    second line:
        an integer for the numer of colors
    next width*height lines:
        4 space-separeted integers for the color of the sides.
        The first, second, third and fourth integers are respectively
        the top, right, bottom and left side of a tile.

Convention for SAT variables names:
    Each variable encode a position and a tile.
    Let t be the tile number (between 1 and n*n).
    Let p be the position on the board, increasing in reading order.
    The variable corresponding to "The tile t is at p" is p * nb_tiles + t.
    Therefore if n is a variable, one can extract t and p.
        t = n % nb_tiles
        p = n // nb_tiles

    Those variables are enough to represent any configuration of a n*n board
    and to solve the Tetravex problem.

By Romain Ageron, Diego Dorn, Yohann D'Anello, Alexia Gross, Elias Suvanto.
Matinfoly 2019.

GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
"""

import os
import subprocess

import click

from output import print_game

END = ' 0\n'


def dim(p, t, nb_tiles):
    """Convert a (position, tile) tuple to a dimacs variable name."""
    return p * nb_tiles + t + 1


def pt(dim, nb_tiles):
    """Convert a dimacs variable id to a (position, tile) tuple."""
    return divmod(dim - 1, nb_tiles)


def gen_unique_tiles_on_spot(n):
    """
    Each position must have only one tile.
    This generates the CNF describing this.
    """

    # for all position there is a tile
    # yield "c There is a tile at each position 0",

    for p in range(n):
        # p1 or p2 or ...
        yield tuple(dim(p, ti, n) for ti in range(n))

    # there are not two true at the same time (#uniquness)
    # yield "c place unique tile",
    for p in range(n):
        for t1 in range(n):
            for t2 in range(t1+1, n):
                yield -dim(p, t1, n), -dim(p, t2, n)

    # Each tile is on only one spot
    # yield "c tile unique place",
    for t in range(n):
        for p1 in range(n):
            for p2 in range(p1 + 1, n):
                yield -dim(p1, t, n), -dim(p2, t, n)


def gen_adjacents(h, l, c, tiles, donut):

    n = len(tiles)

    right_incomp = [[] for _ in range(n)]
    bottom_incomp = [[] for _ in range(n)]

    for i, t1 in enumerate(tiles):
        for j, t2 in enumerate(tiles):
            if i != j:
                if t1[1] != t2[3]:
                    right_incomp[i].append(j)
                if t1[2] != t2[0]:
                    bottom_incomp[i].append(j)
    # yield "c", right_incomp
    # yield "c", bottom_incomp

    for p in range(n):
        i, j = divmod(p, l)
        for t1 in range(n):
            # Si on est dans la dernière colonne, pas besoin
            # de verifier la compat a droite.
            if j != l - 1:
                for t2 in right_incomp[t1]:
                    # yield 'c', '-'*20, p+1, t
                    yield (-dim(p,t1,n), -dim(p+1, t2, n))
            elif donut:
                for t2 in right_incomp[t1]:
                    # yield 'c', '-'*20, p+1, t
                    yield (-dim(p,t1,n), -dim(p+1-l, t2, n))


            # Si on est dans la dernière ligne, pas besoin
            # de verifier la compat en bas.
            if i != h - 1:
                for t2 in bottom_incomp[t1]:
                    yield (-dim(p, t1, n), -dim(p + l, t2, n))
            elif donut:
                for t2 in bottom_incomp[t1]:
                    yield (-dim(p, t1, n), -dim(p % l, t2, n))



def solve(h, l, c, tiles, donut=False, verbose=False, clean=False):
    """
    Get the permutation that solves the given puzzle.

    Return:
        None if not satisfiable
        ret[position] = tile_nb
    """

    nb_tiles = h * l

    # generate a list of clause for the DIMACS file

    a = list(gen_unique_tiles_on_spot(nb_tiles))
    b = list(gen_adjacents(h, l, c, tiles, donut))
    clauses = a + b

    # Write the DIMACS file.

    with open('in', 'w') as f:
        print("p cnf", nb_tiles * nb_tiles, len(clauses), file=f)
        for clause in clauses:
            print(*clause, 0, file=f)

    # Let the SAT solver run !
    if verbose:
        os.system('glucose in out')
    else:
        os.system('glucose in out -verb=0 > /dev/null')

    with open('out', 'r') as f:
        out = f.read()

    if clean:
        os.remove('in')
        os.remove('out')

    # Parsing the result

    if 'UNSAT' in out:
        return

    # Building the permutation function
    values = map(int, out.split())
    pairs = {}
    for v in values:
        if v > 0:
            p, t = pt(v, nb_tiles)
            pairs[p] = t

    return pairs


@click.command()
@click.option('-c', '--clean', is_flag=True, help='Remove intermediate files (dimacs in and out)')
@click.option('-v', '--verbose', is_flag=True, help='Show glucose output')
@click.option('--donut', is_flag=True, help='Tries to solve the puzzle on a donut, that is, borders on opposite sides must have the same color')
@click.option('-i', '--hide-input', is_flag=True, help='Remove pretty print of the input before solve')
@click.option('-b', '--only-bijection', is_flag=True, help='Print only the bijection if there is one. Overrides -v and -i.')
@click.option('-r', '--only-reorder', is_flag=True, help='Print only the tiles in the right order, in the usual input format.')
def main(verbose, donut, clean, hide_input, only_bijection, only_reorder):
    """
    Solver for Teraflex.

    Input:
        - first line:
            two integers representing the width and height of the board
        - second line:
                  an integer for the numer of colors
        - next width*height lines:
                4 space-separeted integers for the color of the sides.
                The first, second, third and fourth integers are respectively
                the top, right, bottom and left side of a tile.
    """

    if only_bijection and only_reorder:
        print('--only_reorder and --only_bijection are not compatible, please choose one.')
        quit(1)
    if only_bijection or only_reorder:
        hide_input = True
        verbose = False

    # input

    h, l = map(int, input().split())
    nb_tiles = h * l
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(nb_tiles)]

    if not hide_input:
        print('Input:')
        print_game(h, l, c, tiles)

    # Computation

    bijection = solve(h, l, c, tiles, verbose=verbose, donut=donut, clean=clean)

    # Output

    if bijection:
        if only_bijection:
            for y in range(h):
                for x in range(l):
                    print('{:>4}'.format(bijection[y*l + x]), end='')
                print()
        elif only_reorder:
            print(h, l)
            print(c)
            for p in range(len(tiles)):
                print(" ".join(map(str, tiles[bijection[p]])))
        else:
            print('Solution:')
            print_game(h, l, c, tiles, bijection)
    else:
        print('no solution')



if __name__ == '__main__':
    main()
