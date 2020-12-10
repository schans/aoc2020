#!/usr/bin/env python

import argparse
import logging
import functools

import networkx as nx


def parse_data(fp):
    fp.seek(0, 0)
    data = [int(line) for line in fp]
    # add outlet
    data.append(0)
    data.sort()
    # add my adapter
    data.append(data[-1]+3)
    return data


def find_one_three_diffs(data):
    ones = 0
    threes = 0
    prev = data[0]
    for cur in data[1:]:
        if (cur - prev) == 1:
            ones += 1
        elif (cur-prev) == 3:
            threes += 1
        prev = cur

    return ones, threes


def build_tree(data):
    G = nx.DiGraph()
    G.add_nodes_from(data)
    i = 0
    j = 1
    while i < len(data) - 1:
        j = i+1

        # search up
        while j < len(data):
            if 1 <= (data[j] - data[i]) <= 3:
                logging.debug("Found edge %d -> %d", data[i], data[j])
                G.add_edge(data[i], data[j])
                j += 1
            else:
                break
        i += 1
    return G


@functools.lru_cache(maxsize=100)
def count_paths_from(G, n):
    paths = 0

    # count is the sum op descendants
    for d in G.neighbors(n):
        logging.debug("%d -> %d", n, d)
        paths += count_paths_from(G, d)

    # leaf node
    if paths == 0:
        paths += 1
    logging.debug("Paths from %d: %d", n, paths)
    return paths


def direct_count_paths_from(data, i, cache=dict()):
    if i in cache:
        return cache[i]

    paths = 0
    j = i+1

    # search up
    while j < len(data):
        if 1 <= (data[j] - data[i]) <= 3:
            logging.debug("Found edge %d -> %d", data[i], data[j])
            paths += direct_count_paths_from(data, j)
            j += 1
        else:
            break

    # leaf node
    if paths == 0:
        paths += 1
    logging.debug("Paths from %d: %d", data[i], paths)

    cache[i] = paths
    return paths


def plot(G):
    # pip install matplotlib
    import matplotlib.pyplot as plt

    pos = nx.nx_agraph.graphviz_layout(G)

    nx.draw(G, pos, with_labels=True, node_size=100, node_color='skyblue', font_size=10, edge_cmap=plt.cm.Blues)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # plt.savefig('graph.pdf')
    plt.show()


def main(args):
    data = parse_data(args.data)
    logging.info("Number of adapters: %d", len(data)-2)
    my_adapter = data[-1]
    logging.info("My adapter max jolt %d", my_adapter)
    ones, threes = find_one_three_diffs(data)
    logging.info("Ones: %d time threes: %d equals %d", ones, threes, ones*threes)
    G = build_tree(data)
    logging.info("Found %d possible combinations (digraph)", count_paths_from(G, 0))
    logging.info("Found %d possible combinations (direct)", direct_count_paths_from(data, 0))

    if args.plot:
        plot(G)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
    parser.add_argument('-p', '--plot', help="show plot", action="store_true")
    return parser.parse_args()


def set_logging(loglevel="INFO"):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(levelname)s %(message)s')


if __name__ == '__main__':
    args = parse_args()
    set_logging(args.log)
    main(args)
