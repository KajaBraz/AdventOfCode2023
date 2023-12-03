"""
Instructions: https://adventofcode.com/2023/day/2
"""

from typing import List

from AdventOfCode2023 import read_data


def handle_input(data: List[str]) -> List[List[str | int]]:
    rows = [row.replace(',', '').replace(';', '').split()[2:] for row in data]
    return [[int(row[i]) if i % 2 == 0 else row[i] for i in range(len(row))] for row in rows]


def solve_part_1(data: List[List[str | int]]) -> int:
    config = {'red': 12, 'green': 13, 'blue': 14}
    valid = 0
    for i in range(len(data)):
        invalid = False
        for j in range(1, len(data[i]), 2):
            colour = data[i][j]
            cnt = config[colour]
            if data[i][j - 1] > cnt:
                invalid = True
        if not invalid:
            valid += (i + 1)
    return valid


def solve_part_2(data: List[List[str | int]]) -> int:
    rounds_powers = 0
    for i in range(len(data)):
        necessary = {'red': 0, 'green': 0, 'blue': 0}
        for j in range(1, len(data[i]), 2):
            colour = data[i][j]
            cur_cnt = necessary[colour]
            if data[i][j - 1] > cur_cnt:
                necessary[colour] = int(data[i][j - 1])
        m = 1
        for v in necessary.values():
            m *= v
        rounds_powers += m
    return rounds_powers


if __name__ == '__main__':
    sample_input = read_data.get_data_02_str_list('sample.txt')
    sample_input = handle_input(sample_input)

    example_1 = solve_part_1(sample_input)
    example_2 = solve_part_2(sample_input)

    my_input = read_data.get_data_02_str_list('input.txt')
    my_input = handle_input(my_input)

    part1 = solve_part_1(my_input)
    part2 = solve_part_2(my_input)

    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part1}')
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part2}')
