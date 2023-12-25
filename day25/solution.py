"""
Instructions: https://adventofcode.com/2023/day/25
"""

from typing import List, Dict, Set

import networkx

from AdventOfCode2023 import read_data


def solve(data: List[str]) -> int:
    d = parse_data(data)
    g = create_graph(d)
    cut_pairs = networkx.minimum_edge_cut(g)
    g.remove_edges_from(cut_pairs)
    connected = list(networkx.connected_components(g))
    return len(connected[0]) * len(connected[1])


def create_graph(dict_data: Dict[str, Set[str]]) -> networkx.Graph:
    graph = networkx.Graph()
    for k, v in dict_data.items():
        for vv in v:
            graph.add_edge(k, vv)
    return graph


def parse_data(data: List[str]) -> Dict[str, Set[str]]:
    d = {}
    for row in data:
        k = row.split(':', 1)[0]
        v = row.split()[1:]
        d[k] = set(v)
    items = list(d.items())
    for k, v in items:
        for vv in v:
            if vv not in d:
                d[vv] = {k}
            else:
                d[vv].add(k)
    return d


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve(sample)
    part_1 = solve(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
