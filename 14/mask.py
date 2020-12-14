#!/usr/bin/env python

import argparse
import logging

from math import pow


def parse_instruction(line):
    (opcode, val) = line.strip().split(' = ')
    if opcode.startswith("mask"):
        # int(mask_str, 2)
        instruction = {
            'opcode': 'mask',
            'mask': val,
            'mask_x0': int(val.replace('X', '0'), 2),
            'mask_x1': int(val.replace('X', '1'), 2)
        }
    elif opcode.startswith("mem"):
        instruction = {
            'opcode': 'mem',
            'addr': int(opcode.split('[')[1][:-1]),
            'value': int(val)
        }
    else:
        logging.error("Unkown instruction: %s", line)
    logging.debug("Instruction: %s", instruction)
    return instruction


def parse_data(fp):
    fp.seek(0, 0)
    code = [parse_instruction(line) for line in fp]
    return code


def run_code(code, mem):
    # line 0 must be mask
    for instr in code:
        if instr['opcode'] == 'mask':
            mask_x0 = instr['mask_x0']
            mask_x1 = instr['mask_x1']
        else:
            addr = instr['addr']
            val = (instr['value'] | mask_x0) & mask_x1
            mem[addr] = val
            logging.debug("Memset %d to %d", addr, val)
    return


def run_code2(code, mem):
    # line 0 must be mask
    for instr in code:
        if instr['opcode'] == 'mask':
            mask_x0 = instr['mask_x0']
            mask_x1 = instr['mask_x1']
            mask = instr['mask']
        else:
            # some masking
            addr = instr['addr']
            mask_xor = mask_x0 ^ mask_x1
            r_0 = (addr | mask_x0) & ~ mask_xor

            # find the X's
            x_count = mask.count('X')
            mutations = int(pow(2, x_count))
            x_pos = list()
            for i in range(0, len(mask)):
                if mask[len(mask) - i - 1] == 'X':
                    x_pos.append(i)

            logging.debug("addr: %s (%d)", bin(addr), addr)
            logging.debug("mxor: %s", bin(mask_xor))
            logging.debug("mask: %s (%d) %s", mask, mutations, x_pos)
            logging.debug("r_0 : %s (%d)", bin(r_0), r_0)

            for i in range(0, mutations):
                # r_0 is the "lowest" permutation with all zeros for X
                perm = r_0
                for k in range(0, x_count):
                    # check if bit is set
                    if (1 << k) & i > 0:
                        # add by shifted x pos
                        perm += (1 << x_pos[k])
                logging.debug("Memset %d to %d", perm, instr['value'])
                mem[perm] = instr['value']
    return


def main(args):
    code = parse_data(args.data)

    mem = [0] * 65196
    run_code(code, mem)
    logging.info("Sum mem: %d", sum(mem))

    mem = dict()
    run_code2(code, mem)
    logging.info("Sum2 mem: %d", sum(mem.values()))


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
