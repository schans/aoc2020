#!/usr/bin/env python

import argparse
import logging


def parse_data(fp):
    cubes = set()
    fp.seek(0, 0)
    x = 0
    while line := fp.readline():
        y = 0
        for _, c in enumerate(line):
            if c == '#':
                cubes.add((x, y, 0, 0))
            y += 1
        x += 1
    return cubes


def get_range(cubes, i, d4=False):
    if not d4 and i == 3:
        return [0]
    low = min(c[i] for c in cubes)
    high = max(c[i] for c in cubes)
    # extend box with one
    return range(low-1, high+2)


def pertubate(cubes, d4=False):
    # pre-calc bounding box ranges
    ranges = list()
    for i in range(0, 4):
        ranges.append(get_range(cubes, i, d4))

    new_cubes = set()
    for x in ranges[0]:
        for y in ranges[1]:
            for z in ranges[2]:
                for w in ranges[3]:
                    nb = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                for dw in [-1, 0, 1]:
                                    if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                                        if (x+dx, y+dy, z+dz, w+dw) in cubes:
                                            nb += 1
                    if (x, y, z, w) in cubes:
                        if nb == 2 or nb == 3:
                            new_cubes.add((x, y, z, w))
                    else:
                        if nb == 3:
                            new_cubes.add((x, y, z, w))

    return new_cubes


def solve(cubes, nstep, d4=False):
    for i in range(nstep):
        cubes = pertubate(cubes, d4)
        logging.debug("After step %d, num cubes: %d", i, len(cubes))
    return len(cubes)


def main(args):
    cubes = parse_data(args.data)
    logging.info("Starting cubes %s", cubes)
    answer = solve(cubes, args.nstep, )
    logging.info("Number of cubes after %d step is in 3d: %d", args.nstep, answer)

    answer = solve(cubes, args.nstep, True)
    logging.info("Number of cubes after %d step is in 4d: %d", args.nstep, answer)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
    parser.add_argument('nstep', help="amount of steps", type=int)
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
