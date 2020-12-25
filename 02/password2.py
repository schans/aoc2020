#!/usr/bin/env python

import fileinput

t1 = 0
t2 = 0
for line in fileinput.input():
    (count, char, passwd) = line.split(' ')
    [low, high] = [int(x) for x in count.split('-')]
    c = char[:-1]

    if low <= passwd.count(c) <= high:
        t1 += 1

    if (passwd[low-1] == c) ^ (passwd[high-1] == c):
        t2 += 1

print(t1, t2)
