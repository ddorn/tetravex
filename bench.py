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
    if xs:
        return sum(xs) / len(xs)
    return 0

def replace_int(string, **x):
    print(string, x)
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
@click.option('-r', '--repetitions', default=10, help='Number of puzzles with the same parameters ro average.')
@click.option('-a', '--start', default=2, help='Begin of range of parameters')
@click.option('-b', '--end', default=6, help='End of range of parameters')
@click.argument('pattern', default='4 4 x')
def main(pattern, repetitions, start, end):
    variables, *params_list = list(generate_params_from_pattern(pattern, start, end))
    print(params_list, variables)

    times = defaultdict(list)

    for params in params_list:
        puzzle = gen(*params)

        total = 0

        for _ in range(repetitions):
            start_time = time()
            solve(*params, puzzle)
            end_time = time()

            total += end_time - start_time
            times[params].append(end_time - start_time)

        # times.append(total / repetitions)

    print()
    for data in zip(params_list, times.values()):
        print(*data)

    abs_label = 2
    d = defaultdict(list)
    for l, value in times.items():
        x = l[abs_label]
        y = value
        name = l[:abs_label] + l[abs_label + 1:]

        d[name].append((x, y))

    for name, xys in d.items():

        name = list(name)
        name.insert(abs_label, 'x')
        name = str(tuple(name)).replace("'x'", 'x')

        xs = [x for x, d in xys]
        ys = [y for x, y in xys]
        print(name)
        plt.boxplot(ys, positions=xs, widths=0.03, )
        plt.plot(xs, list(map(mean, ys)), label=name)

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
