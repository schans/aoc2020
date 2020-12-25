#!/usr/bin/env python

# prod
pubs = (2959251, 4542595)

# test
# pubs = (17807724, 5764801)


def trans(subj, n=1):
    v = 1
    for i in range(n):
        v *= subj
        v %= 20201227
    return v


loops = list()
for p in pubs:
    subj = 7
    pub = 1
    for i in range(1, 1_000_000_000):

        pub *= subj
        pub %= 20201227
        if pub == p:
            loops.append((i, pub))
            break

print(loops)
subj = loops[0][1]
loop = loops[1][0]
key = trans(subj, loop)
# print('keygen1', subj, 'loops', loop, 'key', key)

subj = loops[1][1]
loop = loops[0][0]
key2 = trans(subj, loop)
# print('keygen2', subj, 'loops', loop, 'key', key2)

assert key == key2
print('key', key)
