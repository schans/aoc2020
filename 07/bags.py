#!/usr/bin/env python

# pip install networkx

import argparse
import logging

import networkx as nx


def parse_rule(G, rule_str, my_bag):
    # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    # faded blue bags contain no other bags.
    parts = rule_str.rstrip('.').split('contain ')
    words = parts[0].split(' ')
    holder_id = ' '.join(words[0:2])
    # skip what own bag can contain
    if holder_id == my_bag:
        return
    G.add_node(holder_id)

    logging.debug("Holder bag: '%s'", holder_id)
    if not parts[1].startswith('no other'):
        contains = parts[1].split(',')
        for contain in contains:
            words = contain.strip().split(' ')
            num = int(words[0])
            bag_id = ' '.join(words[1:3])
            G.add_node(bag_id)
            G.add_edge(bag_id, holder_id, weight=num)
            logging.debug("* holds %d of '%s'", num, bag_id)


def parse_data(G, fp, my_bag):
    fp.seek(0, 0)
    while line := fp.readline():
        line = line.strip()
        if line == "":
            continue
        logging.debug("Parsing: %s", line)
        parse_rule(G, line, my_bag)
    return


def fetch_connected_nodes(G, node, seen=None, depth=0):
    if seen == None:
        seen = set([node])
        # print(node)

    depth += 1
    for neighbor in G.neighbors(node):
        if neighbor not in seen:
            seen.add(neighbor)
            #print(' ' + '*'*depth + ' ' + neighbor)
            fetch_connected_nodes(G, neighbor, seen, depth)
    return seen


def do_count(G, my_bag):
    count = 0
    for node in G.nodes():
        #print("* " + node)
        if contains_bag(G, node, my_bag):
            count += 1
    return count


def contains_bag(G, bag, my_bag):

    for neighbor in G.predecessors(bag):
        #print(bag + '>' + neighbor)

        if neighbor == my_bag:
            return True
        if contains_bag(G, neighbor, my_bag):
            return True
    return False


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
    my_bag = 'shiny gold'

    G = nx.DiGraph(format='weighted_adjacency_matrix')
    parse_data(G, args.data, my_bag)

    logging.info("My bag: %s", my_bag)
    logging.info("Number of nodes %d, edges %d", G.number_of_nodes(), G.number_of_edges())

    # use nx breath first search
    bt = nx.bfs_tree(G, my_bag, reverse=False)
    edges = list(bt.edges())
    logging.debug("BFS: %s", edges)
    logging.info("BFS: Numer bags can hold my bag is: %d", len(edges))

    # use custom search
    connected = fetch_connected_nodes(G, my_bag)
    logging.debug("Connected: %s", connected)
    logging.info("Connected: Numer bags can hold my bag is: %d", len(connected) - 1)

    # use recurse count
    logging.info("Recursive count %d", do_count(G, my_bag))
    if args.plot:
        plot(G)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', help="Log level",
                        choices=['debug', 'info', 'warn', 'error'], default='info')
    parser.add_argument('-p', '--plot', help="show plot", action="store_true")
    parser.add_argument('data', help="input data file", type=argparse.FileType('r'))
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
