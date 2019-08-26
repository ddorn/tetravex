"""
Solver for Tetravex.


Convention for SAT variables names:
    Each variable encode a position and a tile.
    Let t be the tile number (between 1 and n*n).
    Let p be the position on the board, increasing right then down.
    The variable corresponding to "The tile t is at p" is p * NTILES + t.
    Therefore if n is a variable, one can extract t and p.
        t = n % NTILES
        p = n // NTILES

    Those variables are enough to represent any configuration of a n*n board
    and to solve the Tetravex problem.

Matinfoly 2019.
"""


END = ' 0\n'
NTILES = 0


def print0(*args, **kwargs):
    """Print anything with a 0 and a newline at the end"""
    kwargs.update(end=END)
    print(*args, **kwargs)


def dim(p, t):
    """Convert a (position, tile) tuple to a dimacs variable name."""
    return p * NTILES + t


def psc(dim):
    """Convert a dimacs variable id to a (position, tile) tuple."""
    return (dim % NTILES, dim // NTILES)


def gen_unique_tiles_on_spot(n, t):
    """
    Each position must have only one tile.
    This generates the CNF describing this.
    """

    # for all position there is a tile
    for p in range(n*n):
        # p1 or p2 or ...
        print0(*(dim(p, ti, t) for ti in range(t)))

    # there are not two true at the same time (#uniquness)
    for p in range(n*n):
        for t1 in range(t):
            for t2 in range(t1+1, t):
                print0(-dim(p, t1), -dim(p, t2))


def gen_adjacents(n, c):
    ...


def main():
    """
    Solver for Teraflex.

    Input:
        n: size of the tetravex
        c: number of colors
        c1 c2 c3 c4: (n*n lines) top, right, bottom and left side of a tile.
    """

    # input

    n = int(input())
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(n*n)]

    # generate DIMACS on stdout

    print("HEADER")
    gen_unique_tiles_on_spot(n, c)
    gen_adjacents(n, c)


if __name__ == '__main__':
    main()
