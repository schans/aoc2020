#!/usr/bin/env python

import argparse
import logging


def parse_data(fp) -> list:
    tree_lines = list()

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            continue
        else:
            line = line.replace('.', '0').replace('#', '1')
            tl = [int(x) for x in list(line)]
            logging.debug("line: %s", list(tl))
            tree_lines.append(tl)

    logging.info("Found %d tree lines", len(tree_lines))
    return tree_lines


def run_sum(tree_lines, col_step, row_step=1):
    col = 0
    count = 0
    for line in tree_lines[::row_step]:
        count += line[col % len(line)]
        col += col_step

    logging.info("Tree count (%d, %d): %d", col_step, row_step, count)
    return count


def main(args):
    tree_lines = parse_data(args.data)
    one = run_sum(tree_lines, 1)
    two = run_sum(tree_lines, 3)
    three = run_sum(tree_lines, 5)
    four = run_sum(tree_lines, 7)
    five = run_sum(tree_lines, 1, 2)
    logging.info("Total: %d", one * two * three * four * five)


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
