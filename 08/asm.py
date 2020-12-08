#!/usr/bin/env python

import argparse
import logging

from copy import deepcopy


def parse_instruction(line):
    (opcode, val) = line.strip().split(' ')
    logging.debug("Opcode %s -> %d", opcode, int(val))
    instruction = {
        'opcode': opcode,
        'value': int(val),
        'executed': False
    }
    return instruction


def parse_data(fp):
    fp.seek(0, 0)
    code = [parse_instruction(line) for line in fp]
    return code


def run_code(code):
    ip = 0
    reg = 0
    while ip < len(code):
        instr = code[ip]
        if instr['executed']:
            logging.error("Loop detected in line %d: %s reg: %d", ip, instr, reg)
            return 1, reg
        ip, reg = execute(instr, ip, reg)
        instr['executed'] = True
    return 0, reg


def execute(instr, ip, reg):
    logging.debug("Executing %d: %s reg: %d", ip + 1, instr, reg)
    if instr['opcode'] == 'nop':
        return ip + 1, reg

    if instr['opcode'] == 'acc':
        return ip + 1, reg + instr['value']

    if instr['opcode'] == 'jmp':
        return ip + instr['value'], reg

    logging.error("Unkown opcode %d: %s", ip + 1, instr)
    return 999999999, reg


def reset(code):
    for instr in code:
        instr['executed'] = False


def try_change(code, new, orig):
    for instr in code:
        if instr['opcode'] == orig:
            instr['opcode'] = new
            exit_code, val = run_code(code)
            if not exit_code:
                logging.info("Found solution: %d", val)
                return
            instr['opcode'] = orig
            reset(code)

    logging.info("%s to %s does not work.", orig, new)
    return


def main(args):
    code = parse_data(args.data)
    exit_code, val = run_code(code)
    logging.info("Program halted with value %d", val)
    try_change(code, 'nop', 'jmp')
    try_change(code, 'jmp', 'nop')


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
