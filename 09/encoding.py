#!/usr/bin/env python

import argparse
import logging

from copy import deepcopy


def parse_data(fp):
    fp.seek(0, 0)
    data = [int(line) for line in fp]
    return data


def check_data(data, preamble):
    i = preamble
    while i < len(data):
        if not is_sum_of(data[i-preamble:i], data[i]):
            return data[i]
        i += 1
    return -1


def is_sum_of(data, num) -> bool:
    logging.debug("Checking for %d in %s", num, data)
    i = 0
    while i < len(data):
        j = i + 1
        while j < len(data):
            if data[i] + data[j] == num:
                return True
            j += 1
        i += 1
    return False


def find_contiguous_sum(data, num):
    i = 0
    j = 0
    s = 0
    while i < len(data):
        j = i + 1
        s = data[i]
        while j < len(data):
            s += data[j]
            logging.debug("Checking sum(%s) = %d == %d", data[i:j+1], s, num)
            if s == num:
                logging.info("Found sum(%s) = %d == %d", data[i:j+1], s, num)
                return min(data[i:j+1]), max(data[i:j+1])
            elif s > num:
                j = len(data)
            j += 1
        i += 1
    return -1, -1


def main(args):
    data = parse_data(args.data)
    logging.info("Using preamble: %d, data: %d", args.preamble, len(data))
    val = check_data(data, args.preamble)
    logging.info("Invalid number is %d", val)
    min_val, max_val = find_contiguous_sum(data, val)
    logging.info("Found %d + %d = %d", min_val, max_val, min_val+max_val)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('-p', '--preamble', help="Preamble", type=int, required=True)
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
