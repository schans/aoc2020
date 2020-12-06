#!/usr/bin/env python

import argparse
import logging
import string


def parse_seat(seat_str):
    seat_bin = seat_str.strip().replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    logging.debug("Seat %s, %s, %s", seat_str.strip(), seat_bin, int(seat_bin, 2))
    return int(seat_bin, 2)


def init_pp():
    return dict()


def parse_data(fp) -> list:

    passports = list()
    pp = init_pp()

    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            passports.append(pp)
            pp = init_pp()
        else:
            logging.debug("line: %s", line)
            fields = line_to_fields(line)
            # pp = merge pp and fields
            pp = {**pp, **fields}

    # last group
    passports.append(pp)
    logging.info("Found %d passports", len(passports))
    return passports


def line_to_fields(line) -> dict:
    fields = dict()
    parts = line.strip().split(' ')
    for part in parts:
        (k, v) = part.split(':')
        fields[k] = v
    return fields


def is_valid_passport(pp) -> bool:
    logging.debug("Check passport: %s", pp)
    # ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm
    required = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}
    for req in required:
        if not req in pp:
            logging.debug('Passort: %s => missing %s', pp, req)
            return False

    if not 1920 <= int(pp['byr']) <= 2002:
        return False

    if not 2010 <= int(pp['iyr']) <= 2020:
        return False

    if not (pp['hgt'].endswith('cm') or pp['hgt'].endswith('in')):
        return False

    if pp['hgt'].endswith('cm'):
        if not (150 <= int(pp['hgt'][:-2]) <= 193):
            return False
    else:
        if not (59 <= int(pp['hgt'][:-2]) <= 76):
            return False

    if not (pp['hcl'].startswith('#') and len(pp['hcl']) == 7 and pp['hcl'][1:].isalnum()):
        return False

    if not 2020 <= int(pp['eyr']) <= 2030:
        return False

    if not pp['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
        return False

    if not (len(pp['pid']) == 9 and pp['pid'].isdigit()):
        return False

    return True


def print_valid_count(passports):
    sum = 0
    for pp in passports:
        if is_valid_passport(pp):
            sum += 1

    logging.info("Sum: %d", sum)


def print_missing(seats):
    missing = set(range(min(seats), max(seats))) - seats
    logging.info("Missing %s", missing)


def main(args):
    passports = parse_data(args.data)
    print_valid_count(passports)
    # print_sum(groups)


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
