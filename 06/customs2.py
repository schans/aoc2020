#!/usr/bin/env python

import fileinput

a2z = 'abcdefghijklmnopqrstuvwxyz'

G = list()
H = list()

c1 = set()
c2 = set(a2z)
for line in fileinput.input():
    line = line.strip()
    if line == "":
        G.append(len(c1))
        H.append(len(c2))
        c1 = set()
        c2 = set(a2z)
    else:
        c1 = c1 | set(line)
        c2 = c2.intersection(set(line))

print('p1', sum(G))
print('p2', sum(H))
