#!/usr/bin/env python
import fileinput

from pyparsing import *

integer = pyparsing_common.integer

operand = integer

multop = oneOf("* /")
plusop = oneOf("+ -")
plmuop = oneOf('+ *')


def calculate(a, b, op):
    if op == '+':
        return int(a)+int(b)
    if op == '-':
        return int(a)-int(b)
    if op == '*':
        return int(a)*int(b)
    return -1


def evaluate(s):
    # assign a
    a = s.pop(0)
    if isinstance(a, ParseResults):
        a = evaluate(a)

    # check if done
    if not s:
        return a

    # op
    op = s.pop(0)

    # assing b
    b = s.pop(0)
    if isinstance(b, ParseResults):
        b = evaluate(b)

    # calc and recurse
    subexpr = [calculate(a, b, op)]
    subexpr.extend(s)
    return evaluate(subexpr)


# multiplication and addition equal
expr = infixNotation(
    operand,
    [
        (plmuop, 2, opAssoc.LEFT),
    ],
)

total1 = 0
for line in fileinput.input():
    result = evaluate(expr.parseString(line))
    total1 += result
    # line = line.strip()
    # print(f"{line} = {result}")

# addition before multiplication
expr = infixNotation(
    operand,
    [
        (plusop, 2, opAssoc.LEFT),
        (multop, 2, opAssoc.LEFT),
    ],
)

total2 = 0
for line in fileinput.input():
    result = evaluate(expr.parseString(line))
    total2 += result
    # line = line.strip()
    # print(f"{line} = {result}")

print(f"Grant total part 1 = {total1}")
print(f"Grant total part 2 = {total2}")
