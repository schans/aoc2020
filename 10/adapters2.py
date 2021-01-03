#!/usr/bin/env python

import fileinput
from functools import lru_cache

A = list()

A = [int(l) for l in fileinput.input()]
# for l in fileinput.input():
#     A.append(int(l))

A.append(0)
A.append(max(A)+3)
A.sort()

ones = threes = 0
for i in range(1, len(A)):
    if (A[i] - A[i-1]) == 1:
        ones += 1
    elif (A[i] - A[i-1]) == 3:
        threes += 1


@lru_cache()
def count_paths(i):
    cnt = 0
    j = i+1
    while j < len(A):
        if 1 <= (A[j] - A[i]) <= 3:
            cnt += count_paths(j)
            j += 1
        else:
            break
    # leaf node
    if cnt == 0:
        cnt += 1
    return cnt


print('ones-thress',  ones*threes)
print('combinations', count_paths(0))
