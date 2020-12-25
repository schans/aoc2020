#!/usr/bin/env python

import fileinput


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


# remap for precedence, overload to map back
# equal: + => *, * => /
# reverse: + =>v*, * => +

t1 = 0
t2 = 0
for line in fileinput.input():
    s1 = ""  # equal: + => *, * => /
    s2 = ""  # reverse: + =>v*, * => +
    for _, c in enumerate(line.strip()):
        if c in "01234567890":
            s1 += "MyNum(" + c + ")"
            s2 += "MyNum(" + c + ")"
        elif c == '*':
            # abuse minus for equal operator precendence
            s1 += '/'
            s2 += '+'
        elif c == '+':
            s1 += '*'
            s2 += '*'
        else:
            s1 += c
            s2 += c
    t1 += eval(s1).n
    t2 += eval(s2).n
print(t1, t2)
