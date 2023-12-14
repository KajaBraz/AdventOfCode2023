"""
Instructions: https://adventofcode.com/2023/day/13
"""

from typing import List

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> int:
    data = parse_input(data)
    h, v = 0, 0
    for t in data:
        h += reflect_horizontally(t)
        v += reflect_vertically(t)
    return calculate_result(h, v)


def calculate_result(h: int, v: int) -> int:
    return v + h * 100


def reflect_vertically(data: List[str]) -> int:
    transposed = transpose(data)
    return reflect_horizontally(transposed)


def reflect_horizontally(data: List[str]) -> int:
    for i in range(len(data) - 1):
        if data[i] == data[i + 1]:
            if reflects(data, i):
                return i + 1
    return 0


def reflects(data: List[str], i: int) -> bool:
    m = min(i + 1, len(data) - i - 1)
    for j in range(m):
        if data[i - j] != data[i + 1 + j]:
            return False
    return True


def transpose(data: List[str]) -> List[str]:
    columns = [''.join(data[i][j] for i in range(len(data))) for j in range(len(data[0]))]
    # columns = list(map(list, zip(*data)))
    return columns


def parse_input(data: List[str]) -> List[List[str]]:
    res = [[]]
    for row in data:
        if not row:
            res.append([])
        else:
            res[-1].append(row)
    return res


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('../day13_inprogress/sample.txt')
    my_input = read_data.get_data_02_str_list('../day13_inprogress/input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
