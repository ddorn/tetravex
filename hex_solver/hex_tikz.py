#!/usr/bin/env python3

"""
This program takes tiles in input (color format) then the SAT solution.
Thanks to the standard library tkinter, it prints the hexa tiles before and after
the solution of the Tetravex puzzle.

Matinfoly 2019 - Elias Suvanto
"""

import tkinter
from math import *

import colorsys
from output import gen_colors


def color2tikz(rgb):
    return f'{{rgb,255:red,{rgb[0]}; green,{rgb[1]}; blue,{rgb[2]} }}'
    
#bijective function, 
def decode(indice):
    """the indice goes 1 to nb_tiles ^ 4"""
    indice = indice-1
    tile = indice // (nb_lines*nb_columns)
    indice = indice - tile*(nb_lines*nb_columns)
    i = indice//nb_columns
    j = indice-nb_columns*i
    return (i, j, tile)


def PutHex(line, column, col_tile, t):
    """prints a tile"""
    global s
    rayon = size
    x = rayon * ((3/2) * line) + marge*line*3 + 100
    y = rayon * (sqrt(3)/2 * line + sqrt(3) * column) -60 \
        + marge * (sqrt(3)*line + 2*sqrt(3)*column)
    
    points = [[x, y], [x + rayon, y], [x + rayon/2, y - rayon*(sqrt(3)/2)],\
    [x - rayon/2, y - rayon*(sqrt(3)/2)], [x - rayon, y], \
    [x - rayon/2, y + rayon*(sqrt(3)/2)], [x + rayon/2, y + rayon*(sqrt(3)/2)]]
    
    coord = [] # sens trigo
    for n in range(6):
        coord.append([points[0], points[1+n], points[1+(n+1)%6]])


    for _ in range(6):
        C.create_polygon(coord[_], fill=colors[col_tile[_]], width = 3, outline = "black")
        a,b,ctr = coord[_]
        
        s += fr'   \draw [black, fill={color2tikz(colors[col_tile[_]])}] {a} -- {b} -- {ctr} -- cycle;' + '\n'
    largeur = 20
    #(C.create_rectangle(x-largeur, y-largeur, x+largeur, y +largeur, fill="white"))
    #C.create_text((x,y), font=("Purisa", 15), text = str(line)+","+str(column))


def main():
    global colors, marge, size, W, H, C, tiles, nb_tiles, nb_lines, nb_columns, s
    s = r"""
    \begin{figure}[h!]
    \begin{center}
    \begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=1cm,y=1cm]
    """
    
    #Lire l'instance
    nb_lines = int(input())
    nb_columns = int(input())
    nb_tiles = nb_lines * nb_columns
    tiles = [list(map(int, input().split())) for _ in range(nb_tiles)]

    res = input() #because we don't want a certain line of the MINISAT Output
    SATsolution = list(map(int, input().split()))

    top = tkinter.Tk()
    size = 70
    W, H = 2*nb_columns*size, 2*nb_lines*size
    C = tkinter.Canvas(top, bg="white", height=H, width=W)

    marge = 5
    colors = ["royal blue", "aquamarine", "navy", "cyan", "yellow", \
        "orange", "red", "mint cream", "azure", "violet red", "white"]
    
    
    for line in range(nb_lines):
        for column in range(nb_columns):
            tile = line*nb_columns + column
            if 2 <= line + column <= 6:
                PutHex(line, column, tiles[tile], tile)
    #
    print(s)
    #
    for indice in SATsolution:
        if indice > 0:
            line,column,t = decode(indice)
            PutHex(line, column+nb_columns+2, tiles[t], t)
    C.pack()
    top.mainloop()

main()
