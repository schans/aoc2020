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
        return {}, False

    # tail
    if r[n][0][0] in ["a", "b"]:
        if r[n][0][0] == l[0]:
            return {l[1:]}, True
        else:
            return {}, False

    matches = set()
    ruleset_match = False
    for ruleset in r[n]:
        left, match = match_ruleset(ruleset, l)
        if match:
            matches |= left
            ruleset_match = True

    return matches, ruleset_match


def match_ruleset(ruleset, l):
    matches = [l]
    for rule in ruleset:
        submatches = set()
        for m in matches:
            left, match = consume(m, rule)
            if match:
                submatches |= left

        matches = submatches
        if len(matches) == 0:
            return {}, False
    return matches, True


def count_matches():
    s = 0
    for l in t:
        res, match = consume(l, '0')
        if match == True:
            for x in res:
                if x == '':
                    # print('MATCH', l)
                    s += 1
    return s


print(f'Patterns: {len(t)}')

s = count_matches()
print(f'Part 1, matches: {s}')

r['8'].append(['42', '8'])
r['11'].append(['42', '11', '31'])

consume.cache_clear()
s = count_matches()
print(f'Part 2, matches: {s}')
