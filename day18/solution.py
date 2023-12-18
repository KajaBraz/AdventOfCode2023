"""
Instructions: https://adventofcode.com/2023/day/18
"""

import itertools
from typing import Set, Tuple, List

from AdventOfCode2023 import read_data


def solve_part_1_v1(dig_plan: List[str], first_inner_point: Tuple[int, int]) -> int:
    dig_plan = parse_data(dig_plan)
    trench = get_border_points(dig_plan)
    return calculate_area(trench, first_inner_point)


def solve_part_1_v2(dig_plan: List[str]) -> int:
    dig_plan = parse_data(dig_plan)
    vertices = get_vertices(dig_plan)
    perimeter = sum(n for _, n, _ in dig_plan)
    return solve_area(vertices, perimeter)


def solve_part_2(dig_plan: List[str]) -> int:
    dig_plan = decode(parse_data(dig_plan))
    vertices = get_vertices(dig_plan)
    perimeter = sum(n for _, n, _ in dig_plan)
    return solve_area(vertices, perimeter)


def calculate_area(border_points: Set[Tuple[int, int]], first_inner_point: tuple[int, int]) -> int:
    seen, not_seen = set(), {first_inner_point}
    while not_seen:
        p = not_seen.pop()
        seen.add(p)
        if p in border_points:
            continue
        not_seen.update(get_neighbours(p[0], p[1]) - seen)
    return len(seen)


def shoelace(vertices: List[Tuple[int, int]]) -> int:
    area = 0
    for (p1, r1), (p2, r2) in itertools.pairwise(vertices):
        # for (p1, r1), (p2, r2) in itertools.pairwise(vertices):
        area += (p1 + p2) * (r1 - r2)
    return abs(area) // 2


def solve_area(vertices: List[Tuple[int, int]], perimeter: int) -> int:
    area = shoelace(vertices)
    return area + perimeter // 2 + 1


def get_neighbours(i: int, j: int) -> Set[Tuple[int, int]]:
    return {(i + m, j + n) for m in [-1, 0, 1] for n in [-1, 0, 1]}


def parse_data(data: List[str]) -> List[Tuple[str, int, str]]:
    rows = [row.split() for row in data]
    return [(row[0], int(row[1]), row[2][2:-1]) for row in rows]


def decode(plan: List[Tuple[str, int, str]]) -> List[Tuple[str, int, str]]:
    points = []
    dirs = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    for _, _, colour in plan:
        new_dist, new_dir = int(colour[:5], 16), int(colour[-1])
        new_dir = dirs[new_dir]
        points.append((new_dir, new_dist, ''))
    return points


def get_border_points(plan: List[Tuple[str, int, str]]) -> Set[Tuple[int, int]]:
    i, j = 0, 0
    border = set()
    dirs = {'R': (0, 1), 'L': (0, -1), 'D': (1, 0), 'U': (-1, 0)}
    for direction, meters, _ in plan:
        for m in range(meters):
            h, v = dirs[direction]
            i, j = i + h, j + v
            border.add((i, j))
    return border


def get_vertices(plan: List[Tuple[str, int, str]]) -> List[Tuple[int, int]]:
    i, j = 0, 0
    points = [(0, 0)]
    dirs = {'R': (0, 1), 'L': (0, -1), 'D': (1, 0), 'U': (-1, 0)}
    for direction, meters, colour in plan:
        i, j = i + meters * dirs[direction][0], j + meters * dirs[direction][1]
        points.append((i, j))
    return points


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1_v1(sample, (1, 1))
    part_1 = solve_part_1_v1(my_input, (-1, -1))
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_1 = solve_part_1_v2(sample)
    part_1 = solve_part_1_v2(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
