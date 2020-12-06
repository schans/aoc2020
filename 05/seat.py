#!/usr/bin/env python

import argparse
import logging


def parse_seat(seat_str):
    seat_bin = seat_str.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    logging.debug("Seat %s, %s, %s", seat_str.strip(), seat_bin, int(seat_bin, 2))
    return int(seat_bin, 2)


def parse_data(fp):
    fp.seek(0, 0)
    seats = set([parse_seat(line) for line in fp])
    return seats


def set_logging(loglevel="INFO"):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s %(message)s')


def print_max(seats):
    logging.info("Max: %s", max(seats))


def print_missing(seats):
    missing = set(range(min(seats), max(seats))) - seats
    logging.info("Missing %s", missing)


def main(args):
    seats = parse_data(args.data)
    print_max(seats)
    print_missing(seats)


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
