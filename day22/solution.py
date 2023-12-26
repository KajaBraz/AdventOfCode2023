"""
Instructions: https://adventofcode.com/2023/day/22
"""

from typing import Tuple, Dict, Set

from AdventOfCode2023 import read_data


def solve(data) -> Tuple[int, int]:
    bricks_points_list, all_bricks_points = generate_points(data)
    bricks_points_list, all_bricks_points, all_ranges_dict = move_all_down(bricks_points_list, all_bricks_points)
    supporting_bricks_ranges = set()
    t_supported_bricks_ranges = {k: set() for k in all_ranges_dict}

    for bricks_points in bricks_points_list:
        supporting_ranges, t_supported_ranges = get_supporting_bricks(bricks_points, all_bricks_points)
        if supporting_ranges:
            supporting_bricks_ranges |= supporting_ranges
        for k, v in t_supported_ranges.items():
            t_supported_bricks_ranges[k].update(v)

    fallen_bricks_count = count_falling_bricks(supporting_bricks_ranges, t_supported_bricks_ranges, all_ranges_dict,
                                               all_bricks_points)

    return len(bricks_points_list) - len(supporting_bricks_ranges), fallen_bricks_count


def get_lower(brick_range, all_ranges_dict: Dict[Tuple, Set[Tuple[int, int, int]]], all_bricks_points):
    lower_bricks = set()
    for x, y, z in all_ranges_dict[brick_range]:
        if (x, y, z - 1) in all_bricks_points and all_bricks_points[(x, y, z - 1)] != brick_range:
            lower_bricks.add(all_bricks_points[(x, y, z - 1)])
    return lower_bricks


def count_falling_bricks(supporting_bricks_ranges, t_supported_bricks_ranges, all_ranges_dict, all_bricks_points):
    cnt = 0
    for supporting_brick in supporting_bricks_ranges:
        queue = list(t_supported_bricks_ranges[supporting_brick])
        dropped = set()
        while queue:
            cur = queue.pop(0)
            if cur in dropped:
                continue
            lower_bricks = get_lower(cur, all_ranges_dict, all_bricks_points)
            if len(lower_bricks) <= 1:
                queue.extend(list(t_supported_bricks_ranges[cur]))
                dropped.add(cur)
            elif len(lower_bricks) > 1 and all(lower_brick in dropped for lower_brick in lower_bricks):
                queue.extend(list(t_supported_bricks_ranges[cur]))
                dropped.add(cur)
        cnt += len(dropped)
    return cnt


def get_supporting_bricks(brick_points, all_bricks_points):
    original_brick_ranges = all_bricks_points[brick_points[0]]
    supporting_points = {(x, y, z - 1): (x, y, z) for (x, y, z) in brick_points if
                         (x, y, z - 1) in all_bricks_points and all_bricks_points[
                             (x, y, z - 1)] != original_brick_ranges}
    supporting_original_ranges = {all_bricks_points[k]: v for k, v in supporting_points.items()}

    supported_ranges = {}
    for k, v in supporting_original_ranges.items():
        r = all_bricks_points[v]
        if k in supported_ranges:
            supported_ranges[k].add(r)
        else:
            supported_ranges[k] = {r}

    supporting_original_ranges = set(supporting_original_ranges.keys())

    if len(supporting_original_ranges) != 1:
        return set(), supported_ranges
    return supporting_original_ranges, supported_ranges


def move_all_down(bricks_points_list, points_dict):
    settled_points = {}
    settled_ranges_dict = {}
    settled_bricks_points = []
    for brick_points in bricks_points_list:
        original_range = points_dict[brick_points[0]]
        move = 0
        while not any((x, y, z - move - 1) in settled_points for x, y, z in brick_points):
            if any(z - move - 1 < 1 for x, y, z in brick_points):
                break
            move += 1
        settled_points = settled_points | {(x, y, z - move): original_range for x, y, z in brick_points}
        settled_ranges_dict[original_range] = {(x, y, z - move) for x, y, z in brick_points}
        settled_bricks_points.append([(x, y, z - move) for x, y, z in brick_points])
    return settled_bricks_points, settled_points, settled_ranges_dict


def generate_points(points_coords):
    points_list = []
    points_dict = {}
    for point_min_max_coords in points_coords:
        brick_points = get_brick_points(point_min_max_coords)
        points_list.append(sorted(brick_points, key=lambda p: p[-1]))
        for p in brick_points:
            points_dict[p] = tuple(point_min_max_coords)
    return sorted(points_list, key=lambda p: p[0][-1]), points_dict


def get_brick_points(min_max_coords):
    x_start, y_start, z_start, x_end, y_end, z_end = min_max_coords
    points_in_range = set()
    for x in range(x_start, x_end + 1):
        for y in range(y_start, y_end + 1):
            for z in range(z_start, z_end + 1):
                points_in_range.add((x, y, z))
    return points_in_range


if __name__ == '__main__':
    sample = read_data.get_data_09_all_line_ints('sample.txt')
    my_input = read_data.get_data_09_all_line_ints('input.txt')

    example_1, example_2 = solve(sample)
    part_1, part_2 = solve(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
