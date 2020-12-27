#!/usr/bin/env python

import fileinput

c1 = c2 = 0
p = dict()

def is_valid(p) -> bool:
    if not 1920 <= int(p['byr']) <= 2002: return False
    if not 2010 <= int(p['iyr']) <= 2020: return False
    if not (p['hgt'].endswith('cm') or p['hgt'].endswith('in')): return False
    if p['hgt'].endswith('cm'): 
        if not (150 <= int(p['hgt'][:-2]) <= 193): return False
    else:
        if not (59 <= int(p['hgt'][:-2]) <= 76): return False
    if not (p['hcl'].startswith('#') and len(p['hcl']) == 7 and p['hcl'][1:].isalnum()): return False
    if not 2020 <= int(p['eyr']) <= 2030: return False
    if not p['ecl'] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}: return False
    if not (len(p['pid']) == 9 and p['pid'].isdigit()): return False
    return True

for line in fileinput.input():
    if line.strip() == "":
        print(p)
        if p.keys() - {'cid'} == {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}:
            c1 += 1
            if is_valid(p):
                c2+=1
        p.clear()
    else:
        for kv in line.strip().split(' '):
            print(kv)
            (k, v) = kv.split(':')
            p[k] = v

print(c1, c2)


