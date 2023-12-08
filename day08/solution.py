"""
Instructions: https://adventofcode.com/2023/day/8
"""

import functools
import math
import re
from typing import List, Tuple, Dict

from AdventOfCode2023 import read_data


def solve_part_1(data: str) -> int:
    directions, nodes = handle_input(data)
    return navigate_single(directions, nodes)


def solve_part_2(data: str) -> int:
    directions, nodes = handle_input(data)
    nums = navigate_multiple(directions, nodes)
    lcm = functools.reduce(lambda a, b: get_lcm(a, b), nums)
    return lcm


def handle_input(data: str) -> Tuple[str, Dict[str, List[str]]]:
    data = re.findall(r'\w+', data)
    directions = data[0]
    nodes = {data[i]: data[i + 1:i + 3] for i in range(1, len(data), 3)}
    return directions, nodes


def reached_last(cur: str, ending_last_char_only: bool) -> bool:
    if not ending_last_char_only:
        return cur == 'ZZZ'
    return cur[-1] == 'Z'


def navigate_single(directions: str, nodes: Dict[str, List[str]], starting: str = 'AAA',
                    ending_last_char_only: bool = False) -> int:
    cur = starting
    i = 0
    while not reached_last(cur, ending_last_char_only):
        cur_dir = directions[i % len(directions)]
        cur_dir_i = 0 if cur_dir == 'L' else 1
        cur = nodes[cur][cur_dir_i]
        i += 1
    return i


def get_all_starting(nodes: Dict[str, List[str]]) -> List[str]:
    return [k for k in nodes.keys() if k[-1] == 'A']


def navigate_multiple(directions: str, nodes: Dict[str, List[str]]) -> List[int]:
    cur = get_all_starting(nodes)
    res = []
    for cur_node in cur:
        res.append(navigate_single(directions, nodes, cur_node, True))
    return res


def get_lcm(a: int, b: int) -> int:
    return abs(a * b) // math.gcd(a, b)


if __name__ == '__main__':
    sample_input_1 = read_data.get_data_00('sample_1.txt')
    sample_input_2 = read_data.get_data_00('sample_2.txt')
    my_input = read_data.get_data_00('input.txt')

    example_1 = solve_part_1(sample_input_1)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample_input_2)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
