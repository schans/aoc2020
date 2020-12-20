#!/usr/bin/env python

import argparse
import logging

import numpy as np

from math import sqrt


class Tile:
    # 'id t o m p l'
    def __init__(self, id, t):
        self.id = id
        self.t = t
        self.flipped = False
        self.placed = False
        self.rot = 0
        self.loc = (-1, -1)

    def flip(self):
        self.t = np.fliplr(self.t)
        self.flipped = not self.flipped
        return self

    def rot90(self):
        self.t = np.rot90(self.t)
        self.rot += 90
        self.rot %= 360
        return self

    def set_loc(self, loc):
        self.loc = loc
        self.placed = True
        logging.debug("Place %s", self)
        return self

    def dump(self):
        s = ""
        for r in self.t:
            l = [str(x) for x in r]
            s += "".join(l)
            s += "\n"
        return s

    def __str__(self):
        s = f"Tile id:{self.id} placed:{self.placed} flip:{self.flipped} rot:{self.rot} loc:{self.loc}"
        return s

    def __repr__(self):
        return 'Tile:'+self.id


def parse_data(fp):
    tiles = list()
    t = list()

    fp.seek(0, 0)

    lines = [line.strip() for line in fp.readlines()]
    for line in lines:
        # while line := fp.readline():
        #     line = line.strip()
        if line == "":
            tiles.append(Tile(n, np.array(t)))
            t = list()
            continue

        if line.startswith("Tile"):
            n = int(line[5:-1])
            continue

        line = line.replace('.', '0').replace('#', '1')
        tl = [int(x) for x in list(line)]
        t.append(tl)

    logging.info("Found %d tiles", len(tiles))
    return tiles


def reset_except(tiles, tile):
    for t in tiles:
        if t.id == tile.id:
            continue
        t.set_loc((-1, -1))
        t.placed = False


def solve(tiles):
    # iterate, rotate and flip start tile for (0,0)
    for tile in tiles:
        for flip in [False, True]:
            if flip:
                tile.flip()
            for rot in [False, True, True, True]:
                if rot:
                    tile.rot90()
                reset_except(tiles, tile)
                solved = place_all(tiles, tile)
                if solved:
                    return solved


def place_all(tiles, first):
    size = int(sqrt(len(tiles)))

    placed = dict()
    wrong = False

    placed[(0, 0)] = first
    first.set_loc((0, 0))

    # iterate ltr per row down
    for x in range(0, size):
        if wrong:
            break
        for y in range(0, size):
            if wrong:
                break
            if (x, y) in placed:
                # first has been placed
                continue

            logging.debug("Tryint to fill (%d, %d)", x, y)
            fit = None
            for tile in tiles:
                left = None
                up = None
                if y:
                    left = placed[(x, y-1)]
                if x:
                    up = placed[(x-1, y)]

                if tile.placed:
                    continue

                # todo multiple can fit..?
                fit = try_place(left, up, tile)
                if fit:
                    placed[(x, y)] = tile
                    tile.set_loc((x, y))
                    break
            if not fit:
                # no fit found config does not work
                logging.debug("Failed attempt")
                wrong = True
                break

    if len(tiles) == len(placed):
        # Solved!
        logging.info("Solved!")
        return placed


def try_place(left, up, tile):
    for flip in [False, True]:
        if flip:
            tile.flip()
        for rot in [False, True, True, True]:
            if rot:
                tile.rot90()

            if up:
                up_match = is_match(up, tile, 'n')
            else:
                up_match = True

            if left:
                left_match = is_match(left, tile, 'w')
            else:
                left_match = True

            if up_match and left_match:
                return True
    return False


def is_match(tile, candidate, direction) -> bool:
    if direction == 'n':
        l1 = tile.t[0]
        l2 = candidate.t[-1]
    elif direction == 'w':
        l1 = tile.t[:, 0]
        l2 = candidate.t[:, -1]
    elif direction == 's':
        l1 = tile.t[-1]
        l2 = candidate.t[0]
    elif direction == 'e':
        l1 = tile.t[:, 0]
        l2 = candidate.t[:, -1]

    return np.array_equal(l1, l2)


def print_solve(tiles, placed, border=True, pretty=True):
    size = int(sqrt(len(tiles)))
    tsize = len(tiles[0].t[0])

    if border:
        tmin = 0
        tmax = tsize
    else:
        tmin = 1
        tmax = tsize - 1

    print_if('+' + '-'*(size*tsize+size-1) + "+\n", pretty)
    for x in range(size-1, -1, -1):
        for row in range(tmin, tmax):
            print_if("|", pretty)
            for y in range(size-1, -1, -1):
                tile = placed[(x, y)]
                l = [str(x) for x in tile.t[row]]
                print("".join(l[tmin:tmax]), end="")
                print_if("|", pretty)
            print()
        print_if('+' + '-'*(size*tsize+size-1) + "+\n", pretty)


def print_if(line, on):
    if not on:
        return
    print(line, end="")


def main(args):
    tiles = parse_data(args.data)

    placed = solve(tiles)

    # gather output
    size = int(sqrt(len(tiles)))
    tl = placed[(0, 0)]
    tr = placed[(0, size-1)]
    bl = placed[(size-1, 0)]
    br = placed[(size-1, size-1)]
    logging.info("tl:%d, tr:%d, bl:%d, br:%d %d",
                 tl.id, tr.id, bl.id, br.id, tl.id * tr.id * bl.id * br.id)

    # print input for part 2
    print_solve(tiles, placed, border=False, pretty=False)


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
