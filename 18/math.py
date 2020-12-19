#!/usr/bin/env python

import argparse
import logging


def parse_data(fp):
    fp.seek(0, 0)
    return [line.strip() for line in fp.readlines()]


def evaluate(expression, ltr):
    logging.debug("Evaluating: '%s' (%s)", expression, ltr)
    if '(' in expression or ')' in expression:
        logging.error("Parse before evaluating!")

    toks = expression.split(' ')
    if len(toks) == 3:
        return calculate(toks[0], toks[2], toks[1])

    if ltr:
        s = calculate(toks[0], toks[2], toks[1])
        return evaluate(str(s) + ' ' + ' '.join(toks[3:]), ltr)

    else:
        if '+' in toks:
            i = toks.index('+')
            s = calculate(toks[i-1], toks[i+1], toks[i])
            l = ''
            r = ''
            if i > 1:
                l = ' '.join(toks[0:i-1]) + ' '
            if i < len(toks) - 2:
                r = ' ' + ' '.join(toks[i+2:])
            return evaluate(l + str(s) + r, ltr)
        else:
            s = calculate(toks[0], toks[2], toks[1])
            return evaluate(str(s) + ' ' + ' '.join(toks[3:]), ltr)

    return -100


def parse(expression, ltr):
    logging.debug("Parsing: '%s' (%s)", expression, ltr)

    first = expression.find('(')
    if first > -1:
        # find part between braces
        p_count = 0
        for i in range(first, len(expression)):
            if expression[i] == '(':
                p_count += 1
            elif expression[i] == ')':
                p_count -= 1

            if not p_count:
                sexpr = ''.join(expression[first+1:i])
                val = parse(sexpr, ltr)
                return parse(expression[0:first] + str(val) + expression[i+1:], ltr)
    else:
        return evaluate(expression, ltr)


def calculate(a, b, op):
    logging.debug("Calculate %s %s %s", a, op, b)
    if op == '+':
        return int(a)+int(b)
    if op == '-':
        return int(a)-int(b)
    if op == '*':
        return int(a)*int(b)
    logging.error("Unknow operator op %s", op)
    return -1


def main(args):
    expressions = parse_data(args.data)
    logging.info("Num expressions %s", len(expressions))
    total = 0
    for expr in expressions:
        s = parse(expr, True)
        logging.info("%s = %d", expr, s)
        total += s
    logging.info("LTR Grand sum is %d", total)
    total = 0
    for expr in expressions:
        s = parse(expr, False)
        logging.info("%s = %d", expr, s)
        total += s
    logging.info("SF Grand sum is %d", total)


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
