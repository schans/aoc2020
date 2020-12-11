#!/usr/bin/env python

import argparse
import logging

import os


def parse_data(fp):
    fp.seek(0, 0)

    data = list()

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip().replace('L', '1').replace('.', '0')
        row = [int(x) - 1 for x in list(line)]
        logging.debug("line: %s", row)
        data.append(row)

    return data


def print_seats(data):
    taken = 0
    os.system('clear')
    # os.system('cls')
    print('-'*len(data[0]))
    for row in data:
        for seat in row:
            if seat < 0:
                print('.', end='')
            elif seat == 0:
                print('L', end='')
            elif seat == 1:
                print('#', end='')
                taken += 1
        print()
    print('-'*len(data[0]))
    print(f"+ Taken [{taken}]")
    print('-'*len(data[0]))


def assign_seats(data, count_func, max_count):
    flips = 0
    i = 0
    new_data = list()
    while i < len(data):
        j = 0
        new_data.append(list())

        while j < len(data[0]):

            new_data[i].append(data[i][j])
            if data[i][j] == 0:
                # empty
                nb = count_func(data, i, j)
                if nb == 0:
                    new_data[i][j] = 1
                    flips += 1

            elif data[i][j] == 1:
                # taken
                nb = count_func(data, i, j)
                if nb >= max_count:
                    new_data[i][j] = 0
                    flips += 1
            j += 1
        i += 1
    logging.debug("Flips: %d", flips)
    return new_data, flips


def count_neighbors(data, i, j):
    nb = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if k == 0 and l == 0:
                # skip self
                continue
            row = i + k
            col = l + j
            if 0 <= row < len(data) and 0 <= col < len(data[0]):
                if data[row][col] > 0:
                    nb += 1
    return nb


def count_see(data, i, j):
    nb = 0

    # n
    nb += looksee(data, i, j, -1, 0)
    # ne
    nb += looksee(data, i, j, -1, 1)
    # e
    nb += looksee(data, i, j, 0, 1)
    # se
    nb += looksee(data, i, j, 1, 1)
    # s
    nb += looksee(data, i, j, 1, 0)
    # sw
    nb += looksee(data, i, j, 1, -1)
    # w
    nb += looksee(data, i, j, 0, -1)
    # nw
    nb += looksee(data, i, j, -1, -1)

    return nb


def looksee(data, i, j, dx, dy):
    row = i + dx
    col = j + dy
    while 0 <= row < len(data) and 0 <= col < len(data[0]):
        if data[row][col] > -1:
            return data[row][col]
        row += dx
        col += dy
    return 0


def find_equilibrium(data, count_func, max_count, out=True):
    flips = 1
    while flips > 0:
        data, flips = assign_seats(data, count_func, max_count)
        if out:
            print_seats(data)
    return data


def main(args):
    data = parse_data(args.data)
    data = find_equilibrium(data, count_neighbors, 4, args.plot)
    print_seats(data)

    data = parse_data(args.data)
    data = find_equilibrium(data, count_see, 5, args.plot)
    print_seats(data)

    logging.info("Dimensions: %dx%d", len(data), len(data[0]))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
    parser.add_argument('-p', '--plot', help="show plot", action="store_true")
    return parser.parse_args()


def set_logging(loglevel="INFO"):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s %(message)s')


if __name__ == '__main__':
    args = parse_args()
    set_logging(args.log)
    main(args)
