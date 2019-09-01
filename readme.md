# Tetravex - Matinfoly 2019

By Romain Ageron, Diego Dorn, Yohann D'Anello, Alexia Gross, Elias Suvanto.

### In short
This is a simple Tetravex solver using a SAT solver as its main algorithm.
It was created as a group projet during [Mathinfoly 2019](http://www.mathinfoly.org/).
an incredible math and cs french summer school.

### Thanks

First of all we want to thank all the Mathinfoly staff, Nicolas, Petru, Idriss
and all the others for this unforgetable week. A special thanks to Pascal Lafourcade
for his help, his delighting sense of humour and everything he taught us.

### Files

This project if composed of sevral parts:
 - `main.py`: The solver itsel, run  `./main.py --help` for more informations
 - `gen.py`: A script to generate random puzzles, see `./gen.py --help` for more.
 - `bench.py`: Mesure perfs and create plots
 - `output.py`: Pretty print of a game in the terminal
 - `tikz_out.py`: A script to generate tikz code to draw a Tetravex
 - `presentation.tex`: The slides used in the presentation of the project

### Install and requierments.

All the code is Python 3.6 code. Therefore one will need a Python 3.6 or newer interpreter and
on can install the dependancies with

	pip install -r requirements.txt

This will install `click` (command line utility) and `matplotlib` (for ploting).


In order to get the colors of `output.py` in the terminal right, you will need a
terminal that supports 24 bits colors our that converts them to 256 bits.
(in case of doubt, `terminator` is the best of them, your tty should to it too though)

### Conventions

#### Convention for text representation of Tetrevex games

Every script that takes an Tetravex game as input needs it in the followin form,
on stdin:
- first line:
    two integers representing the width and height of the board
- second line:
	  an integer for the numer of colors
- next width*height lines:
        4 space-separeted integers for the color of the sides.
        The first, second, third and fourth integers are respectively
        the top, right, bottom and left side of a tile.

#### Convention for SAT variables names:

Each SAT variable encodes a position and a tile.
Let t be the tile number (between 1 and n*n).
Let p be the position on the board, increasing in reading order.
The variable corresponding to "The tile t is at p" is `p * nb_tiles + t`.
Therefore if n is a variable, one can extract t and p.

	t = n % nb_tiles
	p = n // nb_tiles

Those variables are enough to represent any configuration of a n*n board
and to solve the Tetravex problem.



---
GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
Matinfoly 2019.
