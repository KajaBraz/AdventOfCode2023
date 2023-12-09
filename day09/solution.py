"""
Instructions: https://adventofcode.com/2023/day/9
"""

import operator
from typing import List

from AdventOfCode2023 import read_data


def solve_part_1(data: List[List[int]]) -> int:
    return solve(data, -1, operator.add)


def solve_part_2(data: List[List[int]]) -> int:
    return solve(data, 0, operator.sub)


def solve(data: List[List[int]], i: int, operation: operator) -> int:
    extrapolated_sum = 0
    for row in data:
        diffs = diff_nums(row)
        extrapolate(diffs, i, operation)
        extrapolated_sum += diffs[0][i]
    return extrapolated_sum


def get_diff(nums: List[int]) -> List[int]:
    return [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]


def diff_nums(nums: List[int]) -> List[List[int]]:
    cur_diff = get_diff(nums)
    diffs = [nums, cur_diff]
    while any(n != 0 for n in cur_diff):
        cur_diff = get_diff(cur_diff)
        diffs.append(cur_diff)
    return diffs


def get_extrapolate_val(diffs: List[List[int]], i: int, operation: operator) -> int:
    return operation(diffs[0][i], diffs[1][i])


def extrapolate(diffs: List[List[int]], i: int, operation: operator) -> None:
    for j in range(len(diffs) - 2, -1, -1):
        n = get_extrapolate_val(diffs[j:], i, operation)
        insert_i = i if i == 0 else len(diffs[j])
        diffs[j].insert(insert_i, n)


if __name__ == '__main__':
    sample = read_data.get_data_03_two_dim_int_list('sample.txt')
    my_input = read_data.get_data_03_two_dim_int_list('input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
