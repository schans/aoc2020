#!/usr/bin/env python

import fileinput

N = set()
for line in fileinput.input():
    n = int(line)
    N.add(n)
    if 2020 - n in N:
        v1 = n
    for m in N:
        if 2020 - n - m in N:
            v2 = n
            v3 = m

print(v1*(2020-v1))
print(v2*v3*(2020-v2-v3))
