#!/usr/bin/env python

import argparse
import logging


def calc_numer(d, turns):
    numbers = list()
    reverse = dict()
    last = -1
    for i in range(0, turns):

        if i < len(d):
            n = d[i]
            logging.debug("init %d, %d", i+1, d[i])
        else:
            n = next_number(numbers, reverse)
            if i % 1_000_000 == 0:
                logging.debug("turn %d, %d, len(rev): %d", i+1, n, len(reverse))

        numbers.append(n)
        # buf one round before storing in reverse index
        if last > -1:
            reverse[last] = i
        last = n
    return numbers[-1]


def next_number(numbers, reverse):
    n = numbers[-1]
    if n in reverse:
        return len(numbers) - reverse[n]
    return 0


def main(args):
    data = [
        # [0, 3, 6],
        # [1, 3, 2],
        # [2, 1, 3],
        # [1, 2, 3],
        # [2, 3, 1],
        # [3, 2, 1],
        # [3, 1, 2],
        [11, 18, 0, 20, 1, 7, 16]
    ]
    for d in data:
        logging.info("%dth %s => %d", args.turns, d, calc_numer(d, args.turns))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('turns', help="amount of turns", type=int)
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
