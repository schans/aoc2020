#!/usr/bin/env python

import argparse
import logging


def parse_data(fp):
    decks = list()
    fp.seek(0, 0)
    lines = [line.strip() for line in fp.readlines()]

    deck = list()
    for line in lines:
        if line == "":
            deck.reverse()
            decks.append(deck)
            deck = list()
            continue

        if line.startswith("Player"):
            continue

        deck.append(int(line.strip()))
    deck.reverse()
    decks.append(deck)
    return decks


def play(decks):
    # assume 2 players
    while True:
        draw = [decks[0].pop(), decks[1].pop()]
        if draw[0] > draw[1]:
            decks[0] = sorted(draw, reverse=False) + decks[0]
        else:
            decks[1] = sorted(draw, reverse=False) + decks[1]
        if len(decks[0]) == 0 or len(decks[1]) == 0:
            return
    return


def recurse(decks):
    # assume 2 players
    logging.debug("Recurse Game %s", decks)
    seen0 = set()
    seen1 = set()
    while True:
        # use str repr as hash
        s0 = str(decks[0])
        s1 = str(decks[1])

        if s0 in seen0 or s1 in seen1:
            logging.debug("Found loop")
            return True  # player 1 win
        seen0.add(s0)
        seen1.add(s1)

        draw = [decks[0].pop(), decks[1].pop()]
        if draw[0] <= len(decks[0]) and draw[1] <= len(decks[1]):
            # play recursive...
            subdecks = list()
            subdecks.append(decks[0][-1*draw[0]:].copy())
            subdecks.append(decks[1][-1*draw[1]:].copy())
            if recurse(subdecks):
                decks[0] = [draw[1], draw[0]] + decks[0]
            else:
                decks[1] = [draw[0], draw[1]] + decks[1]

        else:
            if draw[0] > draw[1]:
                decks[0] = sorted(draw, reverse=False) + decks[0]
            else:
                decks[1] = sorted(draw, reverse=False) + decks[1]

        if len(decks[0]) == 0 or len(decks[1]) == 0:
            if len(decks[1]) == 0:
                logging.debug("Player1 win")
            else:
                logging.debug("Player2 win")
            return len(decks[1]) == 0
    return


def find_safe(rcpts, alrgs):
    all_ingrs = set()
    for r in rcpts:
        all_ingrs |= r['ingrs']

    unsafe = set()
    for a in alrgs:
        unsafe |= alrgs[a]

    return all_ingrs - unsafe


def main(args):
    decks = parse_data(args.data)
    logging.info("Found %d decks with %d cards per deck!", len(decks), len(decks[0]))

    play(decks)
    # print(decks)
    logging.info("Combat Player1 score %d", sum([(i+1) * v for i, v in enumerate(decks[0])]))
    logging.info("Combat Player2 score %d", sum([(i+1) * v for i, v in enumerate(decks[1])]))

    decks = parse_data(args.data)
    recurse(decks)
    # print(decks)
    logging.info("Recurse Combat Player1 score %d", sum([(i+1) * v for i, v in enumerate(decks[0])]))
    logging.info("Recurse Combat Player2 score %d", sum([(i+1) * v for i, v in enumerate(decks[1])]))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
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
