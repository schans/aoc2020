#!/usr/bin/env python

import argparse
import logging
import string


def init_set(mode):
    if mode == "diff":
        return set(string.ascii_lowercase)
    return set()


def parse_data(fp, mode) -> list:
    if not mode in {'common', 'diff'}:
        logging.error("Unknown mode %s", mode)
        return list()

    groups = list()
    charset = init_set(mode)

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            groups.append(charset)
            charset = init_set(mode)
        else:
            logging.debug("line: %s", set(line))
            if mode == "common":
                charset = charset | set(line)
            elif mode == "diff":
                charset = charset.intersection(set(line))

    # last group
    groups.append(charset)
    logging.info("Found %d grous, mode %s", len(groups), mode)
    return groups


def print_sum(groups):
    sum = 0
    for group in groups:
        logging.debug("%s -> %d", group, len(group))
        sum += len(group)

    logging.info("Sum: %d", sum)


def print_missing(seats):
    missing = set(range(min(seats), max(seats))) - seats
    logging.info("Missing %s", missing)


def main(args):
    groups = parse_data(args.data, "common")
    print_sum(groups)
    groups = parse_data(args.data, "diff")
    print_sum(groups)


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
