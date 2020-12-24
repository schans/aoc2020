#!/usr/bin/env python

import argparse
import logging

C = dict()  # all tiles cache


class Tile(object):
    def __init__(self, coord):
        self.black = False  # start white
        self.black_next = False  # next day color
        self.coord = coord  # (x,y)

        # neighbors
        self.n = {
            (2, 0): None,  # e
            (1, -1): None,  # se
            (-1, -1): None,  # sw
            (-2, 0): None,  # w
            (-1, 1): None,  # nw
            (1, 1): None  # ne
        }

    def flip(self):
        self.black = not self.black

    def get_neighbor(self, d):
        if not self.n[d]:
            x = self.coord[0]+d[0]
            y = self.coord[1]+d[1]
            if (x, y) in C:
                self.n[d] = C[(x, y)]
            else:
                self.n[d] = Tile((x, y))
                C[(x, y)] = self.n[d]

        return self.n[d]

    def nb_populate(self):
        for c in self.n:
            self.get_neighbor(c)

    def nb_count(self):
        c = 0
        for t in self.n.values():
            if t and t.black:
                c += 1
        return c

    @staticmethod
    def add(x, y):
        if (x, y) in C:
            return
        t = Tile((x, y))
        C[(x, y)] = t
        for d in t.n:
            x = t.coord[0]+d[0]
            y = t.coord[1]+d[1]
            if (x, y) in C:
                t.n[d] = C[(x, y)]

    def __repr__(self):
        return 'Tile({})'.format(self.coord)

    def __str__(self):
        if self.black:
            c = 'b'
        else:
            c = 'w'
        return 'Tile({} {})'.format(c, self.coord)


def parse_data(fp):
    rules = list()
    fp.seek(0, 0)
    lines = [line.strip() for line in fp.readlines()]
    for l in lines:
        dirs = list()
        i = 0
        while i < len(l):
            # e, se, sw, w, nw, and ne
            if l[i] == 's':
                if l[i+1] == 'e':
                    dirs.append((1, -1))
                    i += 2
                elif l[i+1] == 'w':
                    dirs.append((-1, -1))
                    i += 2

            elif l[i] == 'n':
                if l[i+1] == 'e':
                    dirs.append((1, 1))
                    i += 2
                elif l[i+1] == 'w':
                    dirs.append((-1, 1))
                    i += 2
            elif l[i] == 'e':
                dirs.append((2, 0))
                i += 1
            elif l[i] == 'w':
                dirs.append((-2, 0))
                i += 1

        rules.append(dirs)
    return rules


def flip_all(rules):
    # initial white tile
    ref = Tile((0, 0))
    C[(0, 0)] = ref
    for dirs in rules:
        flip(dirs, ref)


def flip(dirs, ref):
    p = ref
    n = None
    # walkd
    for d in dirs:
        n = p.get_neighbor(d)
        p = n
    # and flip
    n.flip()


def pop_grid():
    # fill in the grid
    maxx = max([abs(d[0]) for d in C.keys()])
    maxy = max([abs(d[1]) for d in C.keys()])
    maxx += maxx % 2 + 2
    maxy += maxy % 2 + 2
    for x in range(-1 * maxx, maxx, 2):
        for y in range(-1 * maxy, maxy, 2):
            Tile.add(x, y)

    for x in range(-1 * maxx - 1, maxx, 2):
        for y in range(-1 * maxy - 1, maxy, 2):
            Tile.add(x, y)


def days(num_days):
    pop_grid()
    for d in range(0, num_days):

        # populate neighbors for black nodes
        coords = list(C.keys())
        for coord in coords:
            # if C[coord].black:
            C[coord].nb_populate()

        # flippery
        for t in C.values():
            t.black_next = t.black
            if t.black and (t.nb_count() == 0 or t.nb_count() > 2):
                t.black_next = False
            if not t.black and t.nb_count() == 2:
                t.black_next = True

        # move state
        for t in C.values():
            t.black = t.black_next

        logging.info("Black tiles after %d days: %d", d+1, count_black())


def count_black():
    c = 0
    for t in C.values():
        if t.black:
            c += 1
    return c


def main(args):
    rules = parse_data(args.data)
    logging.info("Found %d rules!", len(rules))
    flip_all(rules)
    logging.info("Black tiles after rules: %d", count_black())
    days(100)


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
