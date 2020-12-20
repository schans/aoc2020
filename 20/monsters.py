#!/usr/bin/env python

import argparse
import logging
import numpy as np

# pip install regex for overlap support
import regex

"""
          1        2
12345678901234567890
                  #
#    ##    ##    ###
 #  #  #  #  #  #
"""

# ascii art regex :D
MONSTER = list()
MONSTER.append(regex.compile(r'..................1.', regex.ASCII))
MONSTER.append(regex.compile(r'1....11....11....111', regex.ASCII))
MONSTER.append(regex.compile(r'.1..1..1..1..1..1...', regex.ASCII))

# number of ones in the monster drawing
MONSTER_NR_ONES = 15


def parse_data(fp):
    tile = list()
    fp.seek(0, 0)
    lines = [line.strip() for line in fp.readlines()]
    for line in lines:
        if line == "":
            continue
        tile.append(list(line))
    return np.array(tile, np.int8)


def solve(sea):
    # rotates and flips
    for flip in [False, True]:
        if flip:
            logging.debug("Flip!")
            sea = np.fliplr(sea)
        for rot in [False, True, True, True]:
            if rot:
                logging.debug("Rotate!")
                sea = np.rot90(sea)
            logging.debug('Try current orientation')
            monsters = find_monsters(sea)
            if monsters:
                return monsters


def count_sea(sea, monsters):
    count = np.sum(sea)
    logging.debug("Sea total count: %d", count)
    # assume no overlapping monsters.. seems legit
    return count - len(monsters)*MONSTER_NR_ONES


def find_monsters(sea):
    c1 = set()
    c2 = set()
    c3 = set()
    lines = line_rep(sea)

    for i in range(1, len(lines)-1):
        # overlap as there can be more than one match per line
        iter1 = MONSTER[1].finditer(lines[i], overlapped=True)
        for res1 in iter1:
            c1.add((i, res1.start()))
    logging.debug('Candidates after first match: %d', len(c1))

    for (i, start) in c1:
        # overlap as there can be more than one match per line
        iter2 = MONSTER[2].finditer(lines[i+1], overlapped=True)
        for res2 in iter2:
            if res2.start() == start:
                c2.add((i, start))
    logging.debug('Candidates after second match: %d', len(c2))

    for (i, start) in c2:
        if lines[i-1][start+18] == '1':
            c3.add((i, start))
    logging.debug('Candidates after third match: %d', len(c3))

    return c3


def line_rep(sea):
    shape = sea.shape
    lines = list()
    for i in range(0, shape[0]):
        line = "".join([str(n) for n in sea[i]])
        lines.append(line)
    return lines


def main(args):
    sea = parse_data(args.data)

    monsters = solve(sea)
    logging.info("Found %d monsters!", len(monsters))
    logging.info("The sea roughness is : %d", count_sea(sea, monsters))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
    return parser.parse_args()


def set_logging(loglevel="INFO"):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s %(message)s')


if __name__ == '__main__':
    parsed_args = parse_args()
    set_logging(parsed_args.log)
    main(parsed_args)
