#!/usr/bin/env python

import fileinput
from functools import lru_cache

T = set()  # all (black) tiles

D = {
    'e': (2, 0),
    'se': (1, -1),
    'sw': (-1, -1),
    'w': (-2, 0),
    'nw': (-1, 1),
    'ne': (1, 1)
}

for l in fileinput.input():
    # walkabout
    x = y = 0
    while len(l) > 0:
        if l[:2] in D:
            x += D[l[:2]][0]
            y += D[l[:2]][1]
            l = l[2:]
        elif l[:1] in D:
            x += D[l[:1]][0]
            y += D[l[:1]][1]
            l = l[1:]
        else:
            # newlines, etc
            l = l[1:]

    # add/flip
    if (x, y) in T:
        T.remove((x, y))
    else:
        T.add((x, y))


def nbrs(t):
    for d in D.values():
        x = t[0] + d[0]
        y = t[1] + d[1]
        yield (x, y)


def propagate(num_days):
    global T
    for d in range(num_days):
        t_new = set()
        # all (black) neigbors are candidates
        candidates = set()
        for t in T:
            for nbr in nbrs(t):
                candidates.add(nbr)

        for c in candidates:
            nbc = 0
            for nbr in nbrs(c):
                if nbr in T:
                    nbc += 1
            # flippery
            if c in T:
                if 1 <= nbc <= 2:
                    t_new.add(c)
            else:
                if nbc == 2:
                    t_new.add(c)

        # move state
        T = t_new
        # print(f"Black tiles {len(T)} after {d+1} days")


print("part 1", len(T))
propagate(100)
print("part 2:", len(T))
