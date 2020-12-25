#!/usr/bin/env python

import argparse
import logging


def parse_data(fp) -> list:
    entries = list()

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            continue
        else:
            entries.append(int(line))

    logging.info("Found %d entries", len(entries))
    return entries


def find_2sum(entries, total):
    for i in range(len(entries)):
        for j in range(len(entries)):
            if entries[i] + entries[j] == total:
                return (entries[i], entries[j])
    logging.error("Sum %d not found in entries", sum)
    return (0, 0)


def find_3sum(entries, total):
    for i in range(len(entries)):
        for j in range(len(entries)):
            for k in range(len(entries)):
                if entries[i] + entries[j] + entries[k] == total:
                    return (entries[i], entries[j], entries[k])
    logging.error("Sum %d not found in entries", sum)
    return (0, 0)


def main(args):
    entries = parse_data(args.data)
    (num1, num2) = find_2sum(entries, 2020)
    logging.info("Found: %d + %d = %d => %d", num1, num2, num1+num2, num1*num2)
    (num1, num2, num3) = find_3sum(entries, 2020)
    logging.info("Found: %d + %d + %d = %d => %d", num1, num2, num3, num1+num2+num3, num1*num2*num3)


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
