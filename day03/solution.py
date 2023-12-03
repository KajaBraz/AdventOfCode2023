from collections import defaultdict
from typing import Tuple, List, Dict, Set

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> int:
    symbols, symbols_coords = get_symbols_coords(data)
    nums = get_nums_coords(data)
    parts = 0
    for num, (row, col_range) in nums:
        if has_adjacent_symbol(symbols_coords, row, col_range, data):
            parts += num
    return parts


def solve_part_2(data: List[str]) -> int:
    symbols, symbols_coords = get_symbols_coords(data)
    nums = get_nums_coords(data)
    gear_ratios = get_gear_ratios(nums, symbols['*'], data)
    return sum(gear_ratios)


def get_cur_num(row: str, start: int) -> Tuple[int, Tuple[int, int]]:
    digit = row[start]
    i = start + 1
    while i < len(row) and row[i].isdigit():
        digit += row[i]
        i += 1
    return int(digit), (start, i)


def get_symbols_coords(data: List[str]) -> Tuple[Dict[str, Set], Set]:
    symbols = defaultdict(set)
    symbols_coords = set()
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] != '.' and not data[row][col].isdigit():
                symbols[data[row][col]].add((row, col))
                symbols_coords.add((row, col))
    return symbols, symbols_coords


def get_nums_coords(data: List[str]) -> List[Tuple[int, Tuple[int, Tuple[int, int]]]]:
    nums = []
    for i in range(len(data)):
        j = 0
        while j < len(data[i]):
            if data[i][j].isdigit():
                num, num_coords = get_cur_num(data[i], j)
                nums.append((num, (i, num_coords)))
                j = num_coords[1] + 1
            else:
                j += 1
    return nums


def get_neighbours(i: int, j_range: Tuple[int, int], max_i: int, max_j: int) -> Set[Tuple[int, int]]:
    neighs = set()
    for j in range(j_range[0], j_range[-1]):
        neighs.update(
            [(i + m, j + n) for m in [-1, 0, 1] for n in [-1, 0, 1] if 0 <= i + m < max_i and 0 <= j + n < max_j])
    return neighs


def has_adjacent_symbol(symbols_coords: Set[Tuple[int, int]], num_i: int, num_j_range: Tuple[int, int],
                        data: List[str]) -> bool:
    neighs = get_neighbours(num_i, num_j_range, len(data), len(data[0]))
    for neigh in neighs:
        if neigh in symbols_coords:
            return True
    return False


def convert_num_coords(num_coords: Tuple[int, Tuple[int, int]]) -> Set[Tuple[int, int]]:
    num_all_coords = set()
    i, j_range = num_coords
    num_all_coords.update([(i, j) for j in range(j_range[0], j_range[1])])
    return num_all_coords


def get_adjacent_nums(gear_neighs: Set[Tuple[int, int]], nums_data: List[Tuple[int, Tuple[int, Tuple[int, int]]]]) -> \
        List[int]:
    adjacent_nums = []
    for num, num_coords in nums_data:
        num_all_coords = convert_num_coords(num_coords)
        common = gear_neighs.intersection(num_all_coords)
        if len(common) > 0:
            adjacent_nums.append(num)
    return adjacent_nums if len(adjacent_nums) >= 2 else []


def get_gear_ratios(nums_data: List[Tuple[int, Tuple[int, Tuple[int, int]]]], gears_coords, data: List[str]) -> \
        List[int]:
    gear_nums = []
    for row, col in gears_coords:
        neighs = get_neighbours(row, (col, col + 1), len(data), len(data[0]))
        adjacent_nums = get_adjacent_nums(neighs, nums_data)
        if len(adjacent_nums) >= 2:
            gear_nums.append(adjacent_nums[0] * adjacent_nums[1])
    return gear_nums


if __name__ == '__main__':
    sample_input = read_data.get_data_02_str_list('sample.txt')

    example_1 = solve_part_1(sample_input)
    example_2 = solve_part_2(sample_input)

    my_input = read_data.get_data_02_str_list('input.txt')

    part_1 = solve_part_1(my_input)
    part_2 = solve_part_2(my_input)

    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
