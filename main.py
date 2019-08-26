"""
Solver for Tetravex.


Convention for SAT variables names:
    Each variable encode a position and a color.
    Let c be the color number from 0 to c-1 included.
    Let s be side of the tile as follows:
        0 => Top
        1 => Right
        2 => Bottom
        3 => Left
    Let p be the position on the board, increasing right then down.
    The variable corresponding to "The side s of the tile p has color c"
    is (4 * p + s)* c + c + 1. Therefore is n is a variable, one can extract
    p, s and c this way:
        c = (n - 1) % c
        s = (n // c - 1) % 4
        p = (n // c - 1) // 4.

    Those variables are enough to represent any configuration of a n*n board
    and to solve the Teravex problem.

Matinfoly 2019.
"""


END = ' 0\n'
COL = 0


def print0(*args, **kwargs):
    """Print anything with a 0 and a newline at the end"""
    kwargs.update(end=END)
    print(*args, **kwargs)


def dim(p, s, c):
    """Convert a (Position, Side, Color) triplet to a dimacs variable name."""
    return (4 * p + s) * COL + c + 1

def psc(dim):
    """Convert a variable id to a (Position, Side, Color) triplet."""
    return ((dim - 1) % COL,
            (n // COL - 1) % 4,
            (n // COL - 1) // 4)


def gen_unique_color_on_spot(n, c):
    """
    Each quarter of tile on the board must have only one color.
    This generates the CNF describing this.
    """

    # forall p,s exists c such that x_psc
    for p in range(n*n):
        for s in range(4):
            # ps1 or ps2 or ...
            print0(*(dim(p, s, col) for col in range(c)))

    # there are not two true at the same time (#uniquness)
    for p in range(n*n):
        for s in range(4):
            for c1 in range(c):
                for c2 in range(c1+1, c):
                    print0(-dim(p, s, c1), -dim(p, s, c2))


def gen_form_tiles(n, c, tiles):
    ...


def gen_adjacents(n, c):
    ...


def gen_unique_place(n, c, tiles):
    ...


def main():
    """
    Solver for Teraflex.

    Input:
        n: size of the teravex
        c: number of colors
        c1 c2 c3 c4: (n*n lines) top, right, bottom and left side of a tile.
    """

    global COL

    # input

    n = int(input())
    COL = c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(n*n)]

    # generate DIMACS on stdout

    gen_unique_color_on_spot(n, c)
    gen_form_tiles(n, c, tiles)
    gen_adjacents(n, c)
    gen_unique_place(n, c, tiles)




if __name__ == '__main__':
    main()
