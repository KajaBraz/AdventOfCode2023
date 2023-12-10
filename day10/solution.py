"""
Instructions: https://adventofcode.com/2023/day/10
"""

from typing import List, Tuple, Set

from AdventOfCode2023 import read_data


def solve_part_1(maze: List[str], initial_pipe: str) -> int:
    return solve(maze, initial_pipe)[0]


def solve_part_2(original_maze: List[str], initial_pipe: str) -> int:
    _, pipes_path = solve(original_maze, initial_pipe)
    start_i, start_j = get_s(original_maze)
    original_maze = [list(row) for row in original_maze]
    original_maze[start_i][start_j] = initial_pipe
    expanded_maze = get_expanded_blank_maze(original_maze)
    remove_extra_pipes(original_maze, pipes_path)
    fill_expanded_maze(original_maze, expanded_maze)
    remove_outer_ground(expanded_maze)
    return count_enclosed(original_maze, expanded_maze)


def solve(original_maze: List[str], initial_pipe: str) -> Tuple[int, Set[Tuple[int, int]]]:
    start_i, start_j = get_s(original_maze)
    visited = {(start_i, start_j)}
    queue = [get_adhering_pipes(original_maze, start_i, start_j, initial_pipe, visited)]
    steps = 0
    while queue:
        adhering = queue.pop(0)
        subqueue = set()
        for i, j in adhering:
            subqueue.update(get_adhering_pipes(original_maze, i, j, original_maze[i][j], visited))
            visited.add((i, j))
        steps += 1
        if subqueue:
            queue.append(subqueue)
    return steps, visited


def get_s(maze: List[str]) -> Tuple[int, int]:
    for i in range(len(maze)):
        if 'S' in set(maze[i]):
            return i, maze[i].index('S')


def get_adhering_pipes(maze: List[str], i: int, j: int, pipe: str, visited: Set[Tuple[int, int]]) -> List[
    Tuple[int, int]]:
    neighbours = {'|': [(i - 1, j), (i + 1, j)],
                  '-': [(i, j - 1), (i, j + 1)],
                  'L': [(i - 1, j), (i, j + 1)],
                  'J': [(i - 1, j), (i, j - 1)],
                  '7': [(i + 1, j), (i, j - 1)],
                  'F': [(i + 1, j), (i, j + 1)],
                  '.': []}
    neighbouring = [neighbour for neighbour in neighbours[pipe] if
                    neighbour not in visited and 0 <= neighbour[0] < len(maze) and 0 <= neighbour[1] < len(maze[0])]
    return neighbouring


def get_expanded_blank_maze(original_maze: List[List[str]]) -> List[List[str]]:
    expanded_blank_maze = [[' ' for _ in range(len(original_maze[0]) * 3)] for _ in range(len(original_maze) * 3)]
    return expanded_blank_maze


def fill_expanded_maze(original_maze: List[List[str]], expanded_maze: List[List[str]]) -> None:
    expanded_pipes_mapping = {"|": ".#..#..#.",
                              "-": "...###...",
                              "L": ".#..##...",
                              "J": ".#.##....",
                              "7": "...##..#.",
                              "F": "....##.#.",
                              ".": "........."}
    for r in range(len(original_maze)):
        for c in range(len(original_maze[0])):
            for dr in range(3):
                expanded_maze[r * 3 + dr][c * 3: c * 3 + 3] = expanded_pipes_mapping[original_maze[r][c]][
                                                              dr * 3:dr * 3 + 3]


def remove_extra_pipes(original_maze: List[List[str]], pipes_path: Set[Tuple[int, int]]) -> None:
    for i in range(len(original_maze)):
        for j in range(len(original_maze[0])):
            if (i, j) not in pipes_path:
                original_maze[i][j] = '.'


def get_neighbours(i: int, j: int, data: List[List[str]]) -> List[Tuple[int, int]]:
    return [(i + m, j + n) for m in [-1, 0, 1] for n in [-1, 0, 1] if
            0 <= i + m < len(data) and 0 <= j + n < len(data[0])]


def remove_outer_ground(expanded_maze: List[List[str]]) -> None:
    visited = set()
    queue = [(0, 0)]
    while queue:
        i, j = queue.pop()
        expanded_maze[i][j] = ' '

        for neigh in get_neighbours(i, j, expanded_maze):
            if neigh not in visited and expanded_maze[neigh[0]][neigh[1]] == ".":
                queue.append(neigh)
                visited.add(neigh)


def count_enclosed(original_maze: List[List[str]], expanded_maze: List[List[str]]) -> int:
    res = 0
    for i in range(len(original_maze)):
        for j in range(len(original_maze[0])):
            res += 1 if all(expanded_maze[i * 3 + k][j * 3:j * 3 + 3] == ['.', '.', '.'] for k in range(3)) else 0
    return res


if __name__ == '__main__':
    sample_1 = read_data.get_data_02_str_list('sample_1.txt')
    sample_2 = read_data.get_data_02_str_list('sample_2.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    sample_initial_pipe = 'F'
    input_initial_pipe = '|'

    example_1 = solve_part_1(sample_1, sample_initial_pipe)
    part_1 = solve_part_1(my_input, input_initial_pipe)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample_2, sample_initial_pipe)
    part_2 = solve_part_2(my_input, input_initial_pipe)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
