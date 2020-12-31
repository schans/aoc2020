#!/usr/bin/env python

import fileinput
from functools import lru_cache

r = dict()  # rules
t = list()  # patterns

head = True
for l in fileinput.input():
    l = l.strip()
    if l == "":
        head = False
        continue
    if head:
        n, expr = l.split(': ')
        r[n] = list()
        for p in expr.split(' | '):
            r[n].append([x.replace('"', '').strip() for x in p.split(' ')])
    else:
        t.append(l)


@lru_cache(maxsize=100000)
def consume(l, n):
    # string is consumed but rules left
    if not l or len(l) == 0:
        return set()

    # tail
    if r[n][0][0] in ["a", "b"]:
        if r[n][0][0] == l[0]:
            return {l[1:]}
        else:
            return set()

    rule_matches = set()
    matches = list()
    submatches = set()

    for ruleset in r[n]:
        matches = [l]
        for rule in ruleset:
            submatches = set()
            for m in matches:
                submatches |= consume(m, rule)
            matches = submatches
        rule_matches |= matches
    return rule_matches


def count_matches():
    consume.cache_clear()
    s = 0
    for l in t:
        if '' in consume(l, '0'):
            s += 1
    return s


print(f'Patterns: {len(t)}')

s = count_matches()
print(f'Part 1, matches: {s}')

r['8'].append(['42', '8'])
r['11'].append(['42', '11', '31'])

s = count_matches()
print(f'Part 2, matches: {s}')
