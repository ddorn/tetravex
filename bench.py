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


def replace_int(string, **x):
    print(string, x)
    if string in x:
        return x[string]
    return int(string)


def generate_params_from_pattern(pattern, start, end):
    pattern = pattern.split()

    terms = [s for s in pattern if not s.isnumeric()]
    terms.sort()
    yield terms

    product = itertools.product(*[range(start, end) for t in terms])
    for parms in product:
        yield list(map(lambda s: replace_int(s, **{t: v for t,v in zip(terms, parms)}), pattern))


@click.command()
@click.option('-r', '--repetitions', default=10, help='Number of puzzles with the same parameters ro average.')
@click.option('-a', '--start', default=2, help='Begin of range of parameters')
@click.option('-b', '--end', default=6, help='End of range of parameters')
@click.argument('pattern', default='4 4 x')
def main(pattern, repetitions, start, end):
    variables, *params_list = list(generate_params_from_pattern(pattern, start, end))
    print(params_list, variables)

    times = []
    for params in params_list:
        puzzle = gen(*params)

        total = 0

        for _ in range(repetitions):
            start_time = time()
            solve(*params, puzzle)
            end_time = time()

            total += end_time - start_time

        times.append(total / repetitions)

    print()
    for data in zip(params_list, times):
        print(*data)

    abs_label = 1
    f = [(l.pop(abs_label), l, value) for l, value in zip(params_list, times)]
    d = defaultdict(list)

    for x, name, y in f:
        d[tuple(name)].append((x, y))

    print(d)

    for name, xys in d.items():
        print(name, xys)
        xs = [a for a, b in xys]
        ys = [b for a, b in xys]
        name = list(name)
        name.insert(abs_label, 'x')
        name = str(tuple(name)).replace("'x'", 'x')
        plt.plot(xs, ys, label=name)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
