#!/usr/bin/env python3

"""
Solver for Tetravex.


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

Matinfoly 2019.
"""

import os

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


def gen_adjacents(h, l, c, tiles):

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

            # Si on est dans la dernière ligne, pas besoin
            # de verifier la compat en bas.
            if i != h - 1:
                for t2 in bottom_incomp[t1]:
                    yield (-dim(p, t1, n), -dim(p + l, t2, n))


def solve(h, l, c, tiles):
    """
    Get the permutation that solves the given puzzle.

    Return:
        None if not satisfiable
        f[position] = tile.
    """

    nb_tiles = h * l

    # generate a list of clause for the DIMACS file

    a = list(gen_unique_tiles_on_spot(h*l))
    b = list(gen_adjacents(h, l, c, tiles))
    clauses = a + b

    # Write the DIMACS file.

    with open('in', 'w') as f:
        print("p cnf", nb_tiles * nb_tiles, len(clauses), file=f)
        for clause in a + b:
            print(*clause, 0, file=f)

    # Let the SAT solver run !
    os.system("glucose in out")

    with open('out', 'r') as f:
        out = f.read()

    # Parsing the result
    if 'UNSAT' in out:
        return

    values = map(int, out.split())
    pairs = {}
    for v in values:
        if v > 0:
            p, t = pt(v, nb_tiles)
            pairs[p] = t

    return pairs


@click.command()
# @click.option('input_file', click.File('r'))
# @click.option('-s', '--sat-solver', default='glucose', help='SAT solver to use.')
def main():  # input_file):  #, sat_solver):
    """
    Solver for Teraflex.

    Input:
        n: size of the tetravex
        c: number of colors
        c1 c2 c3 c4: (n*n lines) top, right, bottom and left side of a tile.
    """

    # input

    h, l = map(int, input().split())
    nb_tiles = h * l
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(nb_tiles)]

    print('Input:')
    print_game(h, l, c, tiles)

    bijection = solve(h, l, c, tiles)

    if bijection:
        print_game(h, l, c, tiles, bijection)
    else:
        print('no solution')

    # print_game(h, l, c, tiles, pairs) # [tiles[pairs[p]] for p in range(NTILES)], )
    # # for i in range(NTILES):
    # #     print(f'Tile {i + 1} is at ({pairs[i] % l}, {pairs[i] // l}).')
    # with open("output", "w") as f:
    #     f.write(str(h) + " " + str(l) + "\n")
    #     f.write(str(c) + "\n")
    #     for p in range(len(tiles)):
    #         f.write(" ".join(map(str, tiles[pairs[p]])) + "\n")


if __name__ == '__main__':
    main()
