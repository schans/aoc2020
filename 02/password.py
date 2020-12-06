#!/usr/bin/env python

import argparse
import logging


def parse_seat(seat_str):
    seat_bin = seat_str.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    logging.debug("Seat %s, %s, %s", seat_str.strip(), seat_bin, int(seat_bin, 2))
    return int(seat_bin, 2)


def parse_data(fp) -> list:
    pwdata = list()

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            continue
        else:

            pwentry = dict()
            (count, char, passwd) = line.split(' ')
            (low, high) = count.split('-')
            pwentry['low'] = int(low)
            pwentry['high'] = int(high)
            pwentry['char'] = char[:-1]
            pwentry['passwd'] = passwd
            pwdata.append(pwentry)

    logging.info("Found %d passwords", len(pwdata))
    return pwdata


def is_valid_entry1(entry) -> bool:
    return entry['low'] <= entry['passwd'].count(entry['char']) <= entry['high']


def is_valid_entry2(entry) -> bool:

    return (entry['passwd'][entry['low']-1] == entry['char']) ^ (entry['passwd'][entry['high']-1] == entry['char'])


def print_valid_count(pwdata):
    count1 = 0
    count2 = 0
    for entry in pwdata:
        if is_valid_entry1(entry):
            count1 += 1
        if is_valid_entry2(entry):
            count2 += 1
    logging.info("Valid passwords 1: %d", count1)
    logging.info("Valid passwords 2: %d", count2)


def main(args):
    pwdata = parse_data(args.data)
    print_valid_count(pwdata)


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
