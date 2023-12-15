"""
Instructions: https://adventofcode.com/2023/day/14
"""

from typing import List

from AdventOfCode2023 import read_data


def solve_part_1(platform: List[str]) -> int:
    platform = [[c for c in row] for row in platform]
    move_nord(platform)
    return calculate_load(platform)


def solve_part_2(platform: List[str]) -> int:
    platform = [[c for c in row] for row in platform]
    n_cycles = 1_000_000_000
    platform_states = set()

    roll_cycle(platform)
    t = tuple(c for row in platform for c in row)
    cycle_1 = 1

    while t not in platform_states:
        platform_states.add(t)
        roll_cycle(platform)
        t = tuple(tuple(row) for row in platform)
        cycle_1 += 1

    platform_states = {t}
    roll_cycle(platform)
    t = tuple(tuple(row) for row in platform)
    cycle_2 = 1

    while t not in platform_states:
        platform_states.add(t)
        roll_cycle(platform)
        t = tuple(tuple(row) for row in platform)
        cycle_2 += 1

    tail_cycles = (n_cycles - cycle_1) % cycle_2

    for _ in range(tail_cycles):
        roll_cycle(platform)

    return calculate_load(platform)


def calculate_load(platform: List[List[str]]) -> int:
    return sum(platform[row].count('O') * (len(platform) - row) for row in range(len(platform)))


def roll_cycle(platform: List[List[str]]) -> None:
    move_nord(platform)
    move_west(platform)
    move_south(platform)
    move_east(platform)


def move_nord(platform: List[List[str]]) -> None:
    for column_i in range(len(platform[0])):
        column = ''.join(get_column(platform, column_i))
        column_parts = column.split('#')
        column = '#'.join([''.join(sorted(part, reverse=True)) for part in column_parts])
        update_column_rows(platform, column, column_i)


def move_south(platform: List[List[str]]) -> None:
    for column_i in range(len(platform[0])):
        column = ''.join(get_column(platform, column_i))
        column_parts = column.split('#')
        column = '#'.join([''.join(sorted(part)) for part in column_parts])
        update_column_rows(platform, column, column_i)


def move_east(platform: List[List[str]]) -> None:
    for row_i in range(len(platform)):
        row = ''.join(platform[row_i])
        row_parts = row.split('#')
        row = '#'.join([''.join(sorted(part)) for part in row_parts])
        platform[row_i] = [item for item in row]


def move_west(platform: List[List[str]]) -> None:
    for row_i in range(len(platform)):
        row = ''.join(platform[row_i])
        row_parts = row.split('#')
        row = '#'.join([''.join(sorted(part, reverse=True)) for part in row_parts])
        platform[row_i] = [item for item in row]


def update_column_rows(platform: List[List[str]], column: str, column_i: int) -> None:
    for row_i in range(len(platform)):
        platform[row_i][column_i] = column[row_i]


def get_column(platform: List[List[str]], j: int) -> List[str]:
    return [row[j] for row in platform]


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
