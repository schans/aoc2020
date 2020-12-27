#!/usr/bin/env python

import fileinput

S = set()

for line in fileinput.input():
    S.add(int(line.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1'), 2))

print("max", max(S))
print("missing", set(range(min(S), max(S))) - S)
