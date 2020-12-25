#!/usr/bin/env python

import fileinput


# remap for precedence, overload to map back
# equal: + => *, * => /
# reverse: + => *, * => +


class MyNum:
    """ map sub to mul """

    def __init__(self, n):
        self.n = int(n)

    def __truediv__(self, x):
        return MyNum(self.n * x.n)

    def __mul__(self, x):
        # redefine minus as multiplication
        return MyNum(self.n + x.n)

    def __add__(self, x):
        return MyNum(self.n * x.n)


remaps = [
    {'+': '*', '*': '/'},
    {'+': '*', '*': '+'}
]

for rm in remaps:
    tot = 0
    for line in fileinput.input():
        s = ""
        for _, c in enumerate(line.strip()):
            if c in "01234567890":
                s += "MyNum(" + c + ")"
            elif c in rm:
                s += rm[c]
            else:
                s += c
        tot += eval(s).n
    print(tot)
