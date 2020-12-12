#!/usr/bin/env python

import argparse
import logging

VECTORS = {
    'N': [0, 1],
    'E': [1, 0],
    'S': [0, -1],
    'W': [-1, 0]
}

WINDS = ['N', 'E', 'S', 'W']


def parse_data(fp):
    fp.seek(0, 0)

    data = list()

    fp.seek(0, 0)
    while line := fp.readline():
        row = (line[0:1], int(line.strip()[1:]))
        logging.debug("line: %s", row)
        data.append(row)

    return data


def sail_away(data, ship):
    for d in data:
        move(ship, d)


def move(ship, d):
    dx = 0
    dy = 0
    if d[0] == 'L':
        ship['d'] = WINDS[(WINDS.index(ship['d']) - int(d[1]/90)) % 4]
    elif d[0] == 'R':
        ship['d'] = WINDS[(WINDS.index(ship['d']) + int(d[1]/90)) % 4]
    elif d[0] == 'F':
        dx = VECTORS[ship['d']][0]
        dy = VECTORS[ship['d']][1]
    else:
        dx = VECTORS[d[0]][0]
        dy = VECTORS[d[0]][1]

    ship['x'] += d[1] * dx
    ship['y'] += d[1] * dy


def point_away(data, ship, waypoint):
    for d in data:
        move_trans(ship, waypoint, d)


def move_trans(s, p, d):
    if d[0] == 'L':
        rot(p, int(d[1]/90), False)
    elif d[0] == 'R':
        rot(p, int(d[1]/90), True)
    elif d[0] == 'F':
        s['x'] = s['x'] + d[1] * p[0]
        s['y'] = s['y'] + d[1] * p[1]
    else:
        p[0] += d[1] * VECTORS[d[0]][0]
        p[1] += d[1] * VECTORS[d[0]][1]


def rot(p, times, clockwise=True):
    for _ in range(times):
        if clockwise:
            rot_cw(p)
        else:
            rot_ccw(p)


def rot_cw(p):
    y = -1 * p[0]
    p[0] = p[1]
    p[1] = y


def rot_ccw(p):
    y = p[0]
    p[0] = -1 * p[1]
    p[1] = y


def main(args):
    data = parse_data(args.data)

    ship = {
        'x': 0,
        'y': 0,
        'd': 'E'
    }

    sail_away(data, ship)
    logging.info("Ship at: %d x %d  = %d, facing %s",
                 ship['x'], ship['y'], abs(ship['x']) + abs(ship['y']), ship['d'])

    ship = {
        'x': 0,
        'y': 0,
        'd': 'E'
    }
    waypoint = [10, 1]

    point_away(data, ship, waypoint)

    logging.info("Waypoint at: %d x %d", waypoint[0], waypoint[1])
    logging.info("Ship at: %d x %d  = %d, facing %s",
                 ship['x'], ship['y'], abs(ship['x']) + abs(ship['y']), ship['d'])


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
    args = parse_args()
    set_logging(args.log)
    main(args)
