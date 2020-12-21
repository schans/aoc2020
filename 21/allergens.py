#!/usr/bin/env python

import argparse
import logging


def parse_data(fp):
    rcpts = list()
    fp.seek(0, 0)
    lines = [line.strip() for line in fp.readlines()]

    for line in lines:
        if line == "":
            continue

        p = line.replace('(', '').replace(')', '').replace(',', '').split(" contains ")
        rcpt = {
            'ingrs': set(p[0].split(" ")),
            'alrgs': set(p[1].split(" ")),
        }
        rcpts.append(rcpt)
    return rcpts


def parse_recepies(rcpts):
    alrgs = dict()
    for rcpt in rcpts:
        for a in rcpt['alrgs']:
            logging.debug("%s must be in %s", a, rcpt['ingrs'])
            if a in alrgs:
                logging.debug("%s must now be in %s", a, alrgs[a] & rcpt['ingrs'])
                alrgs[a] &= rcpt['ingrs']
            else:
                alrgs[a] = rcpt['ingrs'].copy()

    solved = False
    while not solved:
        solved = True
        for a in alrgs:
            if len(alrgs[a]) == 1:
                logging.debug("%s is %s", a,  alrgs[a])
                for r in alrgs:
                    if len(alrgs[r]) > 1:
                        alrgs[r] -= alrgs[a]
                        if len(alrgs[r]) > 1:
                            solved = False

    return alrgs


def find_safe(rcpts, alrgs):
    all_ingrs = set()
    for r in rcpts:
        all_ingrs |= r['ingrs']

    unsafe = set()
    for a in alrgs:
        unsafe |= alrgs[a]

    return all_ingrs - unsafe


def count_ingr_in_rcpts(rcpts, ingrs):
    count = 0
    for r in rcpts:
        for i in r['ingrs']:
            if i in ingrs:
                count += 1
    return count


def get_sorted_ingredient(alrgs):
    ingrs = list()
    for a in sorted(alrgs.keys()):
        ingrs.append(alrgs[a].pop())
    return ','.join(ingrs)


def main(args):
    rcpts = parse_data(args.data)
    logging.info("Found %d recepies!", len(rcpts))
    alrgs = parse_recepies(rcpts)
    safe = find_safe(rcpts, alrgs)
    logging.info("Safe %s", safe)
    logging.info("Safe count is %d", count_ingr_in_rcpts(rcpts, safe))
    logging.info("Sorted ingredients %s", get_sorted_ingredient(alrgs))


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
