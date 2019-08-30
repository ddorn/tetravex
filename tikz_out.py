#!/usr/bin/env python3

"""
Generate a tikz view of a Tetravex board.

Matinfoly 2019 - Diego Dorn
"""


import colorsys
from output import gen_colors


def color2tikz(rgb):
    return f'{{rgb,255:red,{rgb[0]}; green,{rgb[1]}; blue,{rgb[2]} }}'


def main():
    """
    Generate the tikz code for a Tetravex board given as input.
    The input is in the same way as in _main.py_.
    """

    h, l = map(int, input().split())
    NTILES = h * l
    c = int(input())
    tiles = [list(map(int, input().split())) for _ in range(NTILES)]
    colors = list(gen_colors(c))
    space = 1.2

    s = r"""
\begin{figure}[h!]
\begin{center}
\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=1cm,y=1cm]
"""
    # s += rf"   \clip (0, 0) rectangle ({l}, {h});"

    for y in range(h):
        for x in range(l):
            t = y * l + x
            tile = tiles[t]

            tl = h - space * y, space * x
            tr = h - space * y, space * x + 1
            bl = h - space * y - 1, space * x
            br = h - space * y - 1, space * x + 1
            ctr = h - space * y - 0.5, space * x + 0.5

            sommets = [tl, tr, br, bl]
            for i in range(4):
                a = sommets[i]
                b = sommets[(i + 1) % 4]
                s += fr'   \draw [black, fill={color2tikz(colors[tile[i]])}] {a} -- {b} -- {ctr} -- cycle;' + '\n'

    s += r"\end{tikzpicture}" + '\n'
    s += r"\end{center}" + '\n'
    s += r'\caption{TIIIIIIITREE PATATE}' + '\n'
    s += r"\end{figure}"

    print(s)

if __name__ == '__main__':
    main()
