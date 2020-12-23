#!/usr/bin/env python

import argparse
import logging


TEST = [int(i) for i in list("389125467")]
PROD = [int(i) for i in list("853192647")]


# SIZE = 9
# MOVES = 100
SIZE = 1_000_000
MOVES = 10_000_000
HEAD = list()
C = dict()  # cache index l->node


# dynamic growing linked list
class Node(object):
    def __init__(self, l):
        """Initialize this node with the given data."""
        self.l = l
        self.next = None
        self.prev = None
        self.prev_n = -1
        self.next_n = -1

    def next_node(self):
        if self.next:
            return self.next
        self.next = self.get_node(self.next_n)
        return self.next

    @staticmethod
    def get_node(l):
        if l in C:
            return C[l]

        # next label
        n_l = l + 1
        if n_l > SIZE:
            # close loop
            n_l = HEAD[0].l

        # prev label
        p_l = l-1
        if p_l < 1:
            p_l = SIZE

        n = Node(l)
        if p_l in C:
            n.prev = C[p_l]
        else:
            n.prev_n = p_l

        if n_l in C:
            n.next = C[n_l]
        else:
            n.next_n = n_l

        C[l] = n
        return n

    def __repr__(self):
        p = '_'
        if self.prev:
            p = self.prev.l
        elif self.prev_n > 0:
            p = "'" + str(self.prev_n)

        n = '_'
        if self.next:
            n = self.next.l
        elif self.next_n > 0:
            n = "'" + str(self.next_n)

        return 'n({}-{!r}-{})'.format(p, self.l, n)


def prep(cups):
    C.clear()
    prev = None
    head = None
    for i, l in enumerate(cups):
        n = Node(l)
        C[l] = n
        if not head:
            head = n
            head.prev_n = SIZE
        if prev:
            prev.next = n
            n.prev = prev
        prev = n

    n.next_n = i+2

    HEAD.append(head)
    logging.info('Head: %s', head)
    logging.info('Tail: %s', n)

    if SIZE <= len(cups):
        # close loop
        n.next = head
        head.prev = n

    return head


def first_n_str(n, h, cnt):
    s = ""
    for i in range(0, cnt):
        if n == h:
            s += "("+str(n.l)+") "
        else:
            s += str(n.l) + " "
        n = n.next_node()
    return s.strip()


def play(h):
    for i in range(MOVES):
        h = do_move(h, i)

    n = C[1]
    s = ""
    for _ in range(8):
        n = n.next_node()
        s += str(n.l) + ' '

    logging.info("Solution part 1: %s", s.strip())

    s1 = C[1].next_node()
    s2 = s1.next_node()

    logging.info("Solution part 2: %d * %d = %d", s1.l, s2.l, s1.l*s2.l)


def do_move(h, move):

    logging.debug("move %d, first %s", move+1, first_n_str(h, h, 9))
    c1 = h.next_node()
    c2 = c1.next_node()
    c3 = c2.next_node()

    logging.debug('pick up [%d,%d,%d]',  c1.l, c2.l, c3.l)

    d = h.l - 1
    if d == 0:
        d = SIZE

    while d in [c1.l, c2.l, c3.l]:
        d -= 1
        if d == 0:
            d = SIZE

    dest = Node.get_node(d)
    logging.debug('destination %d', dest.l)
    move_3_after_to_after(h, dest)

    return h.next_node()


def move_3_after_to_after(h, dest):

    c1 = h.next_node()
    c2 = c1.next_node()
    c3 = c2.next_node()
    c4 = c3.next_node()

    h.next = c4
    c4.prev = h

    dn = dest.next_node()

    dest.next = c1
    c1.prev = dest

    dn.prev = c3
    c3.next = dn


def main(args):
    # head = prep(TEST)
    # play(head)

    head = prep(PROD)
    play(head)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    return parser.parse_args()


def set_logging(loglevel="INFO"):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s %(message)s')


if __name__ == '__main__':
    parsed_args = parse_args()
    set_logging(parsed_args.log)
    main(parsed_args)
