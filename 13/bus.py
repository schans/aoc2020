#!/usr/bin/env python

import argparse
import logging

DATA = {
    'test': {
        'time': 939,
        'busses': [int(x) for x in '7,13,x,x,59,x,31,19'.replace('x', '1').split(',')]
    },
    'prod': {
        'time': 1000066,
        'busses': [int(x) for x in '13,x,x,41,x,x,x,37,x,x,x,x,x,659,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19,x,x,x,23,x,x,x,x,x,29,x,409,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17'.replace('x', '1').split(',')]
    }
}


def find_bus(d='test'):
    t = DATA[d]['time']
    min = 10000
    for bus in DATA[d]['busses']:
        if bus == 1:
            continue
        w = wait_time(t, bus)
        if w < min:
            min = w
            best = bus
        logging.debug('%d: %d mod %d, wait: %d', bus, int(t/bus), t % bus, w)
    return best


def solve_brute(r):
    m = max(r)
    i = r.index(m)
    for n in range(1, 1145159583560291):
        if validate(r, (n * m) - i):
            return (n*m) - i


def validate(busses, n):
    i = 0
    while i < len(busses):
        if busses[i] > 0:
            if (n + i) % busses[i] > 0:
                return False
        i += 1
    return True


def solve(v):
    # to tupples
    r = list()
    i = len(v) - 1
    while i >= 0:
        if v[i] > 1:
            r.append((i, v[i]))
        i -= 1

    while len(r) > 1:
        t1 = r.pop()
        t2 = r.pop()
        t0 = reduce_to_one(t1, t2)
        r.append(t0)
        logging.debug("reduce %s + %s => %s", t1, t2, t0)

    return t0[1]-t0[0]


def reduce_to_one(t1, t2):
    i = t1[0]
    j = t2[0]
    n = t1[1]
    m = t2[1]
    # use t1 for stepping as it will be the largest
    for k in range(n-i, n*m, n):
        if (k + i) % n == 0 and (k + j) % m == 0:
            return (n*m - k, n*m)


def wait_time(x, y):
    return ((int(x / y) + 1)*y) - x


def main(args):
    d = 'test'
    best = find_bus(d)
    logging.info("%s: best bus: %d, wait at %d => %d",
                 d, best, wait_time(DATA[d]['time'], best), best * wait_time(DATA[d]['time'], best))

    r = DATA[d]['busses']
    logging.debug("Busses: %s", r)
    logging.info("Brute force: %d",  solve_brute(r))
    logging.info("Solved: %d", solve(DATA[d]['busses']))

    d = 'prod'
    best = find_bus(d)
    logging.info("%s: best bus: %d, wait at %d => %d",
                 d, best, wait_time(DATA[d]['time'], best), best * wait_time(DATA[d]['time'], best))

    # no chance! => logging.info("Brute force: %d",  solve_brute(r))
    logging.info("Solved: %d", solve(DATA[d]['busses']))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
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
