#!/usr/bin/env python

import fileinput

T = list()
S = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

for line in fileinput.input():
    T.append(list(line.strip()))

maxx = len(T[0])
tmul = 1
for s in S:
    c, x = 0, 0
    for y in range(0, len(T), s[1]):
        if T[y][x % maxx] == '#':
            c += 1
        x += s[0]
    tmul *= c
    print(s, c)

print('mul', tmul)
