"""
Instructions: https://adventofcode.com/2023/day/15
"""

import re
from typing import List, Dict

from AdventOfCode2023 import read_data


def solve_part_1(data: str) -> int:
    data = data.split(',')
    return sum(get_hash(step) for step in data)


def solve_part_2(data: str) -> int:
    boxes = [{} for _ in range(256)]
    data = data.split(',')
    for step in data:
        boxes = execute_step(step, boxes)
    return calc_focusing_power(boxes)


def execute_step(step: str, boxes: List[Dict[str, str]]) -> List[Dict[str, str]]:
    x = re.split(r'[-=]', step)
    if not x[-1]:
        return perform_dash_operation(x[0], boxes)
    return perform_equals_operation(x[0], boxes, x[1])


def get_hash(s: str) -> int:
    cur_val = 0
    for ch in s:
        cur_val += ord(ch)
        cur_val *= 17
        cur_val %= 256
    return cur_val


def perform_dash_operation(label: str, boxes: List[Dict[str, str]]) -> List[Dict[str, str]]:
    h = get_hash(label)
    if label in boxes[h]:
        boxes[h].pop(label)
    return boxes


def perform_equals_operation(label: str, boxes: List[Dict[str, str]], focal_l: str) -> List[Dict[str, str]]:
    h = get_hash(label)
    boxes[h][label] = focal_l
    return boxes


def calc_focusing_power(boxes: List[Dict[str, str]]) -> int:
    res = 0
    for i in range(len(boxes)):
        for j, focal_l in enumerate(boxes[i].values()):
            res += (i + 1) * (j + 1) * int(focal_l)
    return res


if __name__ == '__main__':
    sample = read_data.get_data_00('sample.txt')
    my_input = read_data.get_data_00('input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
