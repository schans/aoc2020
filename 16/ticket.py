#!/usr/bin/env python

import argparse
import logging


def parse_ticket(line):
    return [int(x) for x in line.split(',')]


def parse_rule(line):
    ranges = set()
    parts = line.split(': ')
    str_ranges = parts[1].split(' or ')
    for r in str_ranges:
        minv, maxv = r.split('-')
        ranges.add((int(minv), int(maxv)))

    return {
        'name': parts[0],
        'ranges': ranges
    }


def parse_data(fp):
    tickets = list()
    rules = list()
    s_rules = True  # start in state rules
    s_mine = False
    s_nearby = False
    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            # new section, set all states false
            s_rules = False
            s_mine = False
            s_nearby = False
        if line == "your ticket:":
            s_mine = True
            continue
        if line == "nearby tickets:":
            s_nearby = True
            continue
        if s_rules:
            rules.append(parse_rule(line))
        elif s_mine:
            my_ticket = parse_ticket(line)
        elif s_nearby:
            tickets.append(parse_ticket(line))
    return rules, my_ticket, tickets


def get_error_rate(rules, tickets):
    rate = 0
    for ticket in tickets:
        rate += get_invalid_number(rules, ticket)
    return rate


def get_invalid_number(rules, ticket):
    logging.debug("Checking ticket: %s", ticket)
    for n in ticket:
        found = False
        for rule in rules:
            logging.debug("Checking for %d in rule: %s", n, rule)
            if is_num_in_ranges(rule['ranges'], n):
                found = True
                continue

        if not found:
            logging.debug("Invalid number %d on ticket %s", n, ticket)
            return n
    return 0


def is_num_in_ranges(ranges, num):
    for r in ranges:
        if num in range(r[0], r[1]+1):
            logging.debug("Found %d in %s", num, r)
            return True
    return False


def get_valid_tickets(rules, tickets):
    valid = list()
    for ticket in tickets:
        if not get_invalid_number(rules, ticket):
            valid.append(ticket)
    return valid


def find_cols_for_rules(rules, tickets):
    for rule in rules:
        find_cols_for_rule(rule, tickets)
        # for easy sorting
        rule['num_cols'] = len(rule['cols'])
    # sort
    rules.sort(key=lambda x: x['num_cols'])


def find_cols_for_rule(rule, tickets):
    rule['cols'] = set()  # possibilities

    # column loop over ticketss
    for i in range(0, len(tickets[0])):
        match = True
        for ticket in tickets:
            n = ticket[i]
            if not is_num_in_ranges(rule['ranges'], n):
                match = False
                break
        if match:
            logging.debug("Found col %d for rule %s", i, rule['name'])
            rule['cols'].add(i)


def assign_col_for_rules(rules):
    taken = set()
    for rule in rules:
        assign_col_for_rule(rule, taken)


def assign_col_for_rule(rule, taken):
    options = rule['cols'] - taken
    if len(options) == 1:
        c = options.pop()
        rule['col'] = c
        taken.add(c)
        logging.info("Assigned col %d, to rule %s", c, rule['name'])
        return


def get_ticket_number(rules, my_ticket):
    num = 1
    for rule in rules:
        if rule['name'].startswith("departure"):
            num *= my_ticket[rule['col']]
    return num


def main(args):
    rules, my_ticket, tickets = parse_data(args.data)
    logging.info("Parsed rules: %d, tickets: %d", len(rules), len(tickets))
    logging.info("My ticket: %s", my_ticket)
    logging.info("Ticket scanning error rate: %d", get_error_rate(rules, tickets))

    tickets = get_valid_tickets(rules, tickets)
    logging.info("Valid tickets: %d", len(tickets))

    find_cols_for_rules(rules, tickets)
    assign_col_for_rules(rules)

    logging.info("My ticket total number is: %d", get_ticket_number(rules, my_ticket))


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
