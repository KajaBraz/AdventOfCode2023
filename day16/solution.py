"""
Instructions: https://adventofcode.com/2023/day/16
"""

from typing import Tuple, List, Callable, Set

from AdventOfCode2023 import read_data


def solve_part_1(grid: List[str]) -> int:
    return count_energized(grid, 0, 0, '-R', beam_right)


def solve_part_2(grid: List[str]) -> int:
    start_top = [(0, j, '|D', beam_down) for j in range(len(grid[0]))]
    start_bottom = [(len(grid) - 1, j, '|U', beam_up) for j in range(len(grid[0]))]
    start_left = [(i, 0, '-R', beam_right) for i in range(len(grid))]
    start_right = [(i, len(grid) - 1, '-L', beam_left) for i in range(len(grid))]
    max_energy = 0
    for start_lines in [start_top, start_bottom, start_left, start_right]:
        for start_conf in start_lines:
            max_energy = max(max_energy, count_energized(grid, *start_conf))
    return max_energy


def count_energized(grid: List[str], start_i: int, start_j: int, direction: str, f: Callable) -> int:
    grid_copy = [[c for c in row] for row in grid]
    togo = [(start_i, start_j, direction, f)]
    visited = set()
    while togo:
        i, j, ch, f = togo.pop(0)
        f(grid_copy, i, j, ch, togo, visited)
    return len({(i, j) for i, j, d in visited})


def beam_down(grid: List[List[str]], i: int, j: int, direction: str, togo: List[Tuple[int, int, str, Callable]],
              visited: Set[Tuple[int, int, str]]) -> None:
    while i < len(grid) and (i, j, 'D') not in visited:
        visited.add((i, j, 'D'))
        if grid[i][j] == '.':
            grid[i][j] = '#'
            i += 1
        elif grid[i][j] in [direction[0], '#']:
            i += 1
        elif grid[i][j] != '#':
            update_dir(direction, grid[i][j], i, j, togo)
            return
        else:
            return


def beam_up(grid: List[List[str]], i: int, j: int, direction: str, togo: List[Tuple[int, int, str, Callable]],
            visited: Set[Tuple[int, int, str]]) -> None:
    while i >= 0 and (i, j, 'U') not in visited:
        visited.add((i, j, 'U'))
        if grid[i][j] == '.':
            grid[i][j] = '#'
            i -= 1
        elif grid[i][j] in [direction[0], '#']:
            i -= 1
        elif grid[i][j] != '#':
            update_dir(direction, grid[i][j], i, j, togo)
            return
        else:
            return


def beam_right(grid: List[List[str]], i: int, j: int, direction: str, togo: List[Tuple[int, int, str, Callable]],
               visited: Set[Tuple[int, int, str]]) -> None:
    while j < len(grid[0]) and (i, j, 'R') not in visited:
        visited.add((i, j, 'R'))
        if grid[i][j] == '.':
            grid[i][j] = '#'
            j += 1
        elif grid[i][j] in [direction[0], '#']:
            j += 1
        elif grid[i][j] != '#':
            update_dir(direction, grid[i][j], i, j, togo)
            return
        else:
            return


def beam_left(grid: List[List[str]], i: int, j: int, direction: str, togo: List[Tuple[int, int, str, Callable]],
              visited: Set[Tuple[int, int, str]]) -> None:
    while j >= 0 and (i, j, 'L') not in visited:
        visited.add((i, j, 'L'))
        if grid[i][j] == '.':
            grid[i][j] = '#'
            j -= 1
        elif grid[i][j] in [direction[0], '#']:
            j -= 1
        elif grid[i][j] != '#':
            update_dir(direction, grid[i][j], i, j, togo)
            return
        else:
            return


def update_dir(direction: str, ch: str, i: int, j: int, togo: List[Tuple[int, int, str, Callable]]) -> None:
    if direction == '|U' and ch == '/':
        togo.append((i, j + 1, '-R', beam_right))
    if direction == '|D' and ch == '/':
        togo.append((i, j - 1, '-L', beam_left))
    if direction == '-R' and ch == '/':
        togo.append((i - 1, j, '|U', beam_up))
    if direction == '-L' and ch == '/':
        togo.append((i + 1, j, '|D', beam_down))
    if direction == '|U' and ch == '\\':
        togo.append((i, j - 1, '-L', beam_left))
    if direction == '|D' and ch == '\\':
        togo.append((i, j + 1, '-R', beam_right))
    if direction == '-R' and ch == '\\':
        togo.append((i + 1, j, '|D', beam_down))
    if direction == '-L' and ch == '\\':
        togo.append((i - 1, j, '|U', beam_up))
    if direction[0] == '|' and ch[0] == '-':
        togo.append((i, j + 1, '-R', beam_right))
        togo.append((i, j - 1, '-L', beam_left))
    if direction[0] == '-' and ch[0] == '|':
        togo.append((i + 1, j, '|D', beam_down))
        togo.append((i - 1, j, '|U', beam_up))


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
