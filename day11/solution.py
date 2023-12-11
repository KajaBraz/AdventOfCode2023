"""
Instructions: https://adventofcode.com/2023/day11
"""

import re
from typing import List, Tuple, Set

from AdventOfCode2023 import read_data


def solve(universe: List[str], multiplier: int) -> int:
    rows_expanded = double_rows(universe)
    cols_expanded = double_columns(universe)
    galaxies = find_galaxies(universe)

    dists = set()
    for g1 in galaxies:
        for g2 in galaxies:
            if g1 != g2:
                dist = calculate_dist(g1, g2, rows_expanded, cols_expanded, multiplier)
                dists.add((g1, g2, dist))

    return sum([item[-1] for item in dists]) // 2


def count_inbetween_expanded(g1: Tuple[int, int], g2: Tuple[int, int], expanded: Set[int], mlt: int, rows=True) -> int:
    i = 0 if rows else -1
    cnt = 0
    for expanded_i in expanded:
        if min(g1[i], g2[i]) <= expanded_i < max(g1[i], g2[i]):
            cnt += (mlt - 1)
    return cnt


def double_rows(data: List[str]) -> Set[int]:
    return double(data)


def double_columns(data: List[str]) -> Set[int]:
    columns = [''.join([data[i][j] for i in range(len(data))]) for j in range(len(data[0]))]
    to_expand = double(columns)
    return to_expand


def double(data: List[str]) -> Set[int]:
    to_expand = set()
    for i in range(len(data)):
        if len(set(data[i])) == 1 and data[i][0] == '.':
            to_expand.add(i)
    return to_expand


def find_galaxies(data: List[str]) -> Set[Tuple[int, int]]:
    galaxies = set()
    for i in range(len(data)):
        galaxies_cols = [m.start() for m in re.finditer('#', data[i])]
        galaxies.update([(i, column) for column in galaxies_cols])
    return galaxies


def calculate_dist(galaxy_1: Tuple[int, int], galaxy_2: Tuple[int, int], exp_rows: Set[int], exp_cols: Set[int],
                   mlt: int) -> int:
    return abs(galaxy_2[0] - galaxy_1[0]) + count_inbetween_expanded(galaxy_1, galaxy_2, exp_rows, mlt) + abs(
        galaxy_2[1] - galaxy_1[1]) + count_inbetween_expanded(galaxy_1, galaxy_2, exp_cols, mlt, False)


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve(sample, 2)
    part_1 = solve(my_input, 2)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve(sample, 1000000)
    part_2 = solve(my_input, 1000000)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
