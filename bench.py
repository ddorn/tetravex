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


def generate_params_from_pattern(pattern, start, end):
    pattern = pattern.split()

    terms = list(set(s for s in pattern if not s.isnumeric()))
    yield terms

    product = itertools.product(*[range(start, end) for t in terms])
    for parms in product:
        yield tuple(map(lambda s: replace_int(s, **{t: v for t,v in zip(terms, parms)}), pattern))


@click.command()
@click.argument('pattern', default='4 4 x')
@click.option('-r', '--repetitions', default=10, help='Number of puzzles with the same parameters ro average.')
@click.option('-a', '--start', default=2, help='Begin of range of parameters')
@click.option('-b', '--end', default=6, help='End of range of parameters')
@click.option('-x', '--abscisse', default=2, help='Abscisse of the graph. 0=width, 1=height, 2=colors')
@click.option('-v', '--verbose', is_flag=True, help='Print sat solver output')
def main(pattern, repetitions, start, end, abscisse, verbose):
    variables, *params_list = list(generate_params_from_pattern(pattern, start, end))

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
    plt.xticks(list(range(start, end)))
    plt.show()


if __name__ == '__main__':
    main()
