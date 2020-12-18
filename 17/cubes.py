#!/usr/bin/env python

import argparse
import logging

import numpy as np
from pprint import pprint

dim = 15

def parse_data(fp):
    cubes = set()
    fp.seek(0, 0)
    x = 0
    while line := fp.readline():
        y = 0
        for _, c in enumerate(line):
            if c == '#':
                cubes.add((x, y , 0, 0))
            y += 1
        x +=1 
    return cubes

def pertubate(cubes, zdim=0):
    new_cubes = set()
    for x in range(-1*dim, dim):
        for y in range(-1*dim, dim):
            for z in range(-1*dim, dim):
                for w in range(-1*zdim, zdim+1):
                    nb = 0
                    for dx in [-1, 0 ,1]:
                        for dy in [-1, 0 ,1]:
                            for dz in [-1, 0 ,1]:
                                for dw in [-1, 0 ,1]:
                                    if dx!=0 or dy!=0 or dz!=0 or dw!=0:
                                        if (x+dx, y+dy, z+dz, w+dw) in cubes:
                                            nb+=1
                    # print(x, y, z, w)
                    if (x,y,z,w) in cubes:
                        if nb == 2 or nb == 3:
                            # print("add", x, y, z, w)
                            new_cubes.add((x,y,z,w))
                    else:
                        if nb == 3:
                            # print("add", x, y, z,w)
                            new_cubes.add((x,y,z, w))
                    
    return new_cubes


def print_z(cubes, z, w=0):
    for c in cubes:
        if c[2] == z and c[3] == w:
            print(c)


def main(args):
    nstep = args.nstep
    cubes = parse_data(args.data)
    print(cubes)

    for _ in range(nstep):
        cubes = pertubate(cubes, 15)
        print_z(cubes,0)
        print(len(cubes))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
    parser.add_argument('nstep', help="amount of steps", type=int)
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
