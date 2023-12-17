"""
Instructions: https://adventofcode.com/2023/day/13
"""

from typing import Tuple, List

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> Tuple[int, List[Tuple[int, int]]]:
    pattern = parse_input(data)
    res = []
    h, v = 0, 0
    for t in pattern:
        h_reflection_line, v_reflection_line = reflect_horizontally(t)[0], 0
        if not h_reflection_line:
            v_reflection_line = reflect_vertically(t)[0]
        res.append((h_reflection_line, v_reflection_line))
        h += h_reflection_line
        v += v_reflection_line
    return calculate_result(h, v), res


def solve_part_2(data: List[str], smudge_0_indices) -> int:
    smudge = {'.': '#', '#': '.'}
    pattern = parse_input(data)
    h, v = 0, 0
    for i, t in enumerate(pattern):
        smudge_found = False
        for x in range(len(t)):
            for y in range(len(t[x])):
                t[x][y] = smudge[t[x][y]]
                h_reflection_lines = reflect_horizontally(t)
                v_reflections_lines = reflect_vertically(t)
                if h_reflection_lines and h_reflection_lines[0] != 0:
                    for h_reflection in h_reflection_lines:
                        if smudge_0_indices[i][0] != h_reflection:
                            h += h_reflection
                            smudge_found = True
                        if smudge_found:
                            break
                if not smudge_found and v_reflections_lines and v_reflections_lines[0] != 0:
                    for v_reflection in v_reflections_lines:
                        if smudge_0_indices[i][1] != v_reflection:
                            v += v_reflection
                            smudge_found = True
                        if smudge_found:
                            break
                if smudge_found:
                    break
                t[x][y] = smudge[t[x][y]]
            if smudge_found:
                break
    return calculate_result(h, v)


def calculate_result(h: int, v: int) -> int:
    return v + h * 100


def reflect_vertically(pattern: List[List[str]]) -> List[int]:
    transposed = transpose(pattern)
    return reflect_horizontally(transposed)


def reflect_horizontally(pattern: List[List[str]]) -> List[int]:
    reflections = []
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            if reflects(pattern, i):
                reflections.append(i + 1)
    return reflections if reflections else [0]


def reflects(pattern: List[List[str]], i: int) -> bool:
    m = min(i + 1, len(pattern) - i - 1)
    for j in range(m):
        if pattern[i - j] != pattern[i + 1 + j]:
            return False
    return True


def transpose(pattern: List[List[str]]) -> List[List[str]]:
    columns = list(map(list, zip(*pattern)))
    return columns


def parse_input(data: List[str]) -> List[List[str]]:
    res = [[]]
    for row in data:
        if not row:
            res.append([])
        else:
            res[-1].append([c for c in row])
    return res


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1, example_smudge_0_indices = solve_part_1(sample)
    part_1, input_smudge_0_indices = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample, example_smudge_0_indices)
    part_2 = solve_part_2(my_input, input_smudge_0_indices)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
