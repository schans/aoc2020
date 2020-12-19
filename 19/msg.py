#!/usr/bin/env python

import argparse
import logging
import re


def parse_data(fp):
    fp.seek(0, 0)
    lines = [line.strip() for line in fp.readlines()]
    rules = dict()
    msgs = set()
    head = True
    for line in lines:
        if line == '':
            head = False
            continue
        if head:
            p = line.split(': ')
            rules[int(p[0])] = p[1].replace('"', '').split(' ')
        else:
            msgs.add(line)

    return rules, msgs


def build_regex(rules):
    expr = get_expr(rules, 0)
    logging.debug("Regexp: ^%s$", expr)
    return re.compile('^' + expr + '$', re.ASCII)


def get_expr(rules, idx):
    # logging.debug("Parse rule %d: '%s'", idx, rules[idx])
    looped = None
    if str(idx) in rules[idx]:
        unlooped = rules[idx][0:rules[idx].index('|')]
        looped = rules[idx][rules[idx].index('|')+1:]
        rules[idx] = unlooped

    f = ''
    l = ''
    r = ''
    for n in rules[idx]:
        if n == '|':
            f = '('
            l = ')'
            r += n
        elif n in ['a', 'b'] or n.startswith('L'):
            r += n
        elif int(n) == idx:
            logging.debug("Loop in rule %d", idx)
            # block loop
            # unlooped = rules[idx][0:rules[idx].in]
            for i, rn in enumerate(rules[idx]):
                if rn == str(idx):
                    rules[idx][i] = 'L' + rn
            #print(get_expr(rules, idx))
            r += get_expr(rules, int(n))
        else:
            r += get_expr(rules, int(n))

    if looped:
        if len(looped) == 2:
            # 8: 42 | 42 8
            # 8: 42 | 42 ( 42 | 8 )
            # 8: 42 | 42 42 | 42 8
            # means (42)+
            return '('+r+')+'
        else:
            # 11: 42 31 | 42 11 31
            # 11: 42 31 | 42 (42 31 | 42 11 31) 31
            # 11: 42 31 | 42 42 31 31 | 42 42 11 31 31
            # means (42){d}(31){d}
            a = get_expr(rules, int(looped[0]))
            b = get_expr(rules, int(looped[2]))
            # couple of iterations.. up until number no longer changes
            expanded = '((' + a + b + ')'
            for k in range(2, 8):
                expanded += '|(' + a + '{'+str(k)+'}' + b + '{'+str(k)+'}' + ')'
            expanded += ')'
            return expanded

    else:
        return f + r + l


def match_count(msgs, r):
    c = 0
    for msg in msgs:
        if r.match(msg):
            c += 1
            logging.debug("Message match %s", msg)
    return c


def main(args):
    rules, msgs = parse_data(args.data)
    logging.info("Num rules:%d, msgs:%d", len(rules), len(msgs))
    r = build_regex(rules)
    logging.info("Numner of matching rules: %d", match_count(msgs, r))


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
