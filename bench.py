#!/usr/bin/env python3

"""
Python script to benchmark the Tetravex solver.

Matinfoly 2019 - Diego Dorn.
"""

import sys
from time import time
import itertools
from collections import defaultdict

import click
import matplotlib.pyplot as plt

from main import solve
from gen import gen

def mean(xs):
    """Avergage of xs"""
    if xs:
        return sum(xs) / len(xs)
    return 0

def replace_int(string, **x):
    """Return the integer in the string or if it is a varable name,
    return the corresponding one from the dict"""
    if string in x:
        return x[string]
    return int(string)


def generate_params_from_pattern(pattern, ranges):
    pattern = pattern.split()

    terms = list(set(s for s in pattern if not s.isnumeric()))
    assert len(ranges) == 1 or len(ranges) == len(terms)

    yield terms

    if len(ranges) == 1:
        product = itertools.product(*[range(ranges[0][0], ranges[0][1]) for _ in terms])
    else:
        product = itertools.product(*[range(start, end) for start, end in ranges])

    for parms in product:
        yield tuple(map(lambda s: replace_int(s, **{t: v for t,v in zip(terms, parms)}), pattern))


@click.command()
@click.argument('pattern', default='4 4 x')
@click.option('-r', '--repetitions', default=10, help='Number of puzzles with the same parameters ro average.')
@click.option('-p', '--param-range', default=(2, 8), multiple=True, help='Range for the parameters. Pass one or one for each')
@click.option('-x', '--abscisse', default=2, help='Abscisse of the graph. 0=width, 1=height, 2=colors')
@click.option('-v', '--verbose', is_flag=True, help='Print sat solver output')
def main(pattern, repetitions, param_range, abscisse, verbose):
    """
    Plot performance against various parameters.

    This script is very versatile, one can choose the parameters that varies
    with the `pattern` string. The pattern is a string with 3 space
    separated components. The first is the width, then height and number of colors.
    Each of those can be either an integer, in which case the parametter is fixed
    or a name for varying parameters.

    There can be more than one varying parameter in which case every combination
    will be generated. Be careful as the computing time increses rapidely.
    If a name is used in multiple place (for instance "x x 4") they will allways
    have the same value. Thus "x x 4" plots the time taken for a N by N grid.

    The range for each parameter can be set with the `--param-range` flag. If
    only one is passed, then every parameter will have the same range, othewise
    one need to pass the same number of range than parameter names in the pattern.


    If the graph is not looking like a graph, make sure you passed the
    right `--abscisse` flag.
    """

    variables, *params_list = list(generate_params_from_pattern(pattern, param_range))

    times = defaultdict(list)

    for params in params_list:
        print(params)
        puzzle = gen(*params)

        total = 0

        for _ in range(repetitions):
            start_time = time()
            solve(*params, puzzle, verbose=verbose)
            end_time = time()

            total += end_time - start_time
            times[params].append(end_time - start_time)

        times[params] = times[params][:-4]

        # times.append(total / repetitions)

    print()
    for data in zip(params_list, times.values()):
        print(*data)


    sort_key = pattern.split()[abscisse]
    d = defaultdict(list)
    for l, value in times.items():
        x = l[abscisse]
        y = value

        name = list(l)
        for i, n in enumerate(reversed(pattern.split())):
            if n == sort_key:
                a = name.pop(len(pattern.split()) - i - 1)

        d[tuple(name)].append((x, y))

    for name, xys in d.items():

        name = list(name)
        for i, n in enumerate(pattern.split()):
            if n == sort_key:
                name.insert(i, 'x')
        name = str(tuple(name)).replace("'x'", 'x')

        xs = [x for x, d in xys]
        ys = [y for x, y in xys]
        print(name)

        plt.boxplot(ys, positions=xs, widths=0.03)
        plt.plot(xs, list(map(mean, ys)), label=name)

    plt.legend()
    plt.xticks(xs)
    plt.show()


if __name__ == '__main__':
    main()
