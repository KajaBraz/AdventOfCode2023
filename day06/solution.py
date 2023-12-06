"""
Instructions: https://adventofcode.com/2023/day/6
"""

import re
from typing import List

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> int:
    data = [re.findall(r'\d+', row) for row in data]
    data = [[int(n) for n in row] for row in data]

    final = 1
    times, dists = data
    for i in range(len(times)):
        final *= beat_record(data[0][i], data[1][i])
    return final


def beat_record(time: int, dist: int) -> int:
    beaten = 0
    for acc in range(1, time):
        new_dist = (time - acc) * acc
        beaten = beaten + 1 if new_dist > dist else beaten
    return beaten


def solve_part_2(data: List[str]) -> int:
    data = [int(''.join(re.findall(r'\d+', row))) for row in data]
    return beat_record(data[0], data[1])


if __name__ == '__main__':
    sample_input = read_data.get_data_02_str_list('sample.txt')

    example_1 = solve_part_1(sample_input)
    example_2 = solve_part_2(sample_input)

    my_input = read_data.get_data_02_str_list('input.txt')

    part_1 = solve_part_1(my_input)
    part_2 = solve_part_2(my_input)

    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
