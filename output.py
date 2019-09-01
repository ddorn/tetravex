#!/usr/bin/env python3

import colorsys


BL = '◢'
BR = '◣'
TL = '◤'
TR = '◥'
BLC = '█' * 2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def gen_colors(nb):
    """Generate n bright distinct RGB triplets"""

    for i in range(nb):
        # prop around the circle
        p = i / nb + 0.82
        rgb = colorsys.hsv_to_rgb(p % 1, 1, 1)
        yield tuple(round(255*c) for c in rgb)


def printfg(txt, fg, end=''):
    print(f"\033[38;2;{fg[0]};{fg[1]};{fg[2]}m{txt}\033[m", end=end)


def pprint(txt, fg, bg, end=''):
    """Print a colored txt"""
    print(f"\033[48;2;{bg[0]};{bg[1]};{bg[2]};38;2;{fg[0]};{fg[1]};{fg[2]}m{txt}\033[m", end=end)


def print_tile(tile, y, n=6, label=None):
    """
    Print the y-th line of a tile with no newline.

    :tile:
        A quadruplet of rgb colors
    :n:
        size of the tile.
    """
    assert 0 <= y < n

    t, r, b, l = tile


    h = n // 2
    for x in range(n):
        if x < y:
            if n - x < y + 1:
                printfg(BLC, b)
            elif n - x == y + 1:
                printfg(BLC, BLACK)
            else:
                printfg(BLC, l)

        elif x == y:
            if x == h and label is not None:
                printfg((str(label) + '  ')[:2], WHITE)
            else:
                printfg(BLC, BLACK)

        else:
            if n - x - 1 < y:
                printfg(BLC, r)
            elif n - x - 1 == y:
                printfg(BLC, BLACK)
            else:
                printfg(BLC, t)


def print_game(h, l, c, tiles, order=None):
    """
    Print a Tetravex board.

    h*l:
        Size of the board.
    c:
        Number of colors.
    tiles:
        A list of n*n tiles to place on the board
        the order is increasing in reading order.
        A tile is a 4-uplet of colors ranging between 1 and c.
        A color of 0 will be an empty tile.
    order:
        The optional permutation of the tiles.
    """

    colors = [BLACK] + list(gen_colors(c))

    # reorder if needed
    if order:
        tiles = [tiles[order[i]] for i in range(h*l)]
    else:
        order = list(range(h*l))

    tiles = [
        [colors[i + 1] for i in tile]
        for tile in tiles
    ]

    LINES = 7  # height of a tile

    # Top border
    print(end='╔')
    for x in range(l):
        print('═'*LINES*2, end='╤' if x != l-1 else '╗')
    print()

    for y in range(h):
        # A line of tiles
        for line in range(LINES):
            print(end='║')
            for x in range(l):
                tile = tiles[y * l + x]
                print_tile(tile, line, LINES, label=order[y*l + x])
                print(end='║' if x == l-1 else '│')
            print()

        # Separation between lines
        if y != h-1:
            print(end='╟')
            for x in range(l):
                print('─'*LINES*2, end='┼' if x != l-1 else '╢')
            print()

    # Bottom border
    print(end='╚')
    for x in range(l):
        print('═'*LINES*2, end='╧' if x != l-1 else '╝')
    print()


if __name__ == '__main__':
    # if run as main, print the inputed game
    h, l = map(int, input().split())
    nb_tiles = h * l
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(nb_tiles)]

    print_game(h, l, c, tiles)

