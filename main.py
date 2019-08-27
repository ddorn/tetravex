#!/usr/bin/env python3

"""
Solver for Tetravex.


Convention for SAT variables names:
    Each variable encode a position and a tile.
    Let t be the tile number (between 1 and n*n).
    Let p be the position on the board, increasing in reading order.
    The variable corresponding to "The tile t is at p" is p * NTILES + t.
    Therefore if n is a variable, one can extract t and p.
        t = n % NTILES
        p = n // NTILES

    Those variables are enough to represent any configuration of a n*n board
    and to solve the Tetravex problem.

Matinfoly 2019.
"""

import os
from output import print_game

END = ' 0\n'
NTILES = 4


def dim(p, t):
    """Convert a (position, tile) tuple to a dimacs variable name."""
    return p * NTILES + t + 1


def pt(dim):
    """Convert a dimacs variable id to a (position, tile) tuple."""
    return divmod(dim - 1, NTILES)


def gen_unique_tiles_on_spot(n):
    """
    Each position must have only one tile.
    This generates the CNF describing this.
    """

    # for all position there is a tile
    # yield "c There is a tile at each position 0",

    for p in range(NTILES):
        # p1 or p2 or ...
        yield tuple(dim(p, ti) for ti in range(n))

    # there are not two true at the same time (#uniquness)
    # yield "c place unique tile",
    for p in range(NTILES):
        for t1 in range(NTILES):
            for t2 in range(t1+1, NTILES):
                yield -dim(p, t1), -dim(p, t2)

    # Each tile is on only one spot
    # yield "c tile unique place",
    for t in range(NTILES):
        for p1 in range(NTILES):
            for p2 in range(p1 + 1, NTILES):
                yield -dim(p1, t), -dim(p2, t)


def gen_adjacents(h, l, c, tiles):
    right_incomp = [[] for _ in range(NTILES)]
    bottom_incomp = [[] for _ in range(NTILES)]

    for i, t1 in enumerate(tiles):
        for j, t2 in enumerate(tiles):
            if i != j:
                if t1[1] != t2[3]:
                    right_incomp[i].append(j)
                if t1[2] != t2[0]:
                    bottom_incomp[i].append(j)
    # yield "c", right_incomp
    # yield "c", bottom_incomp

    for p in range(NTILES):
        i, j = divmod(p, l)
        for t1 in range(NTILES):
            # Si on est dans la dernière colonne, pas besoin
            # de verifier la compat a droite.
            if j != l - 1:
                for t2 in right_incomp[t1]:
                    # yield 'c', '-'*20, p+1, t
                    yield (-dim(p,t1), -dim(p+1, t2))

            # Si on est dans la dernière ligne, pas besoin
            # de verifier la compat en bas.
            if i != h - 1:
                for t2 in bottom_incomp[t1]:
                    yield (-dim(p, t1), -dim(p + l, t2))


def main():
    """
    Solver for Teraflex.

    Input:
        n: size of the tetravex
        c: number of colors
        c1 c2 c3 c4: (n*n lines) top, right, bottom and left side of a tile.
    """

    global NTILES

    # input

    h, l = map(int, input().split())
    NTILES = h * l
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(NTILES)]

    print('Input:')
    print_game(h, l, c, tiles)

    # generate a list of clause for the DIMACS file

    a = list(gen_unique_tiles_on_spot(h*l))
    b = list(gen_adjacents(h, l, c, tiles))
    clauses = a + b

    # Write the DIMACS file.

    with open('in', 'w') as f:
        print("p cnf", NTILES * NTILES, len(clauses), file=f)
        for clause in a + b:
            print(*clause, 0, file=f)

    # Let the SAT solver run !
    os.system("glucose in out")

    with open('out', 'r') as f:
        out = f.read()

    # Parsing the result
    if 'UNSAT' in out:
        print('No solution!')
        return
    values = map(int, out.split())
    pairs = {}
    for v in values:
        if v > 0:
            p, t = pt(v)
            pairs[p] = t

    print_game(h, l, c, tiles, pairs) # [tiles[pairs[p]] for p in range(NTILES)], )
    # for i in range(NTILES):
    #     print(f'Tile {i + 1} is at ({pairs[i] % l}, {pairs[i] // l}).')

if __name__ == '__main__':
    main()
