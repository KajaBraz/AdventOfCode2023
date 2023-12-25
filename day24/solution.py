"""
Instructions: https://adventofcode.com/2023/day/24
"""

from typing import List, Tuple

import sympy as sym

from AdventOfCode2023 import read_data


def solve_part_1(data: List[List[int]], limit_min: int, limit_max: int) -> int:
    result = 0

    for i in range(len(data)):
        x, y, z, velocity_x, velocity_y, velocity_z = data[i]
        for xx, yy, zz, velocity_xx, velocity_yy, velocity_zz in data[i + 1:]:
            x2, y2 = get_next_point(x, y, velocity_x, velocity_y)
            a1, b1 = get_formula((x, y), (x2, y2))
            xx2, yy2 = get_next_point(xx, yy, velocity_xx, velocity_yy)
            a2, b2 = get_formula((xx, yy), (xx2, yy2))

            intersection_point = get_intersection(a1, b1, a2, b2)

            if intersection_point:
                if limit_min <= intersection_point[0] <= limit_max and limit_min <= intersection_point[1] <= limit_max:
                    ok_p1 = validate_intersection((x, y), intersection_point, velocity_x, velocity_y)
                    ok_p2 = validate_intersection((xx, yy), intersection_point, velocity_xx, velocity_yy)

                    if ok_p1 and ok_p2:
                        result += 1
    return result


def solve_part_2(data: List[List[int]]) -> int:
    Px, Py, Pz, velocity_Px, velocity_Py, velocity_Pz = data[0]
    Qx, Qy, Qz, velocity_Qx, velocity_Qy, velocity_Qz = data[1]
    Rx, Ry, Rz, velocity_Rx, velocity_Ry, velocity_Rz = data[2]

    Ix, Iy, Iz, v_Ix, v_Iy, v_Iz, t1, t2, t3 = sym.symbols('Ix,Iy,Iz,v_Ix,v_Iy,v_Iz,t1,t2,t3')
    symbols = [Ix, Iy, Iz, v_Ix, v_Iy, v_Iz, t1, t2, t3]

    eqPIx = sym.Eq(Ix + t1 * v_Ix, Px + t1 * velocity_Px)
    eqPIy = sym.Eq(Iy + t1 * v_Iy, Py + t1 * velocity_Py)
    eqPIz = sym.Eq(Iz + t1 * v_Iz, Pz + t1 * velocity_Pz)

    eqQIx = sym.Eq(Ix + t2 * v_Ix, Qx + t2 * velocity_Qx)
    eqQIy = sym.Eq(Iy + t2 * v_Iy, Qy + t2 * velocity_Qy)
    eqQIz = sym.Eq(Iz + t2 * v_Iz, Qz + t2 * velocity_Qz)

    eqRIx = sym.Eq(Ix + t3 * v_Ix, Rx + t3 * velocity_Rx)
    eqRIy = sym.Eq(Iy + t3 * v_Iy, Ry + t3 * velocity_Ry)
    eqRIz = sym.Eq(Iz + t3 * v_Iz, Rz + t3 * velocity_Rz)

    equations = [eqPIx, eqPIy, eqPIz, eqQIx, eqQIy, eqQIz, eqRIx, eqRIy, eqRIz]
    result = sym.solve(equations, symbols)
    return sum(result[0][:3])


def get_next_point(x: int, y: int, velocity_x: int, velocity_y: int) -> Tuple[int, int]:
    return x + velocity_x, y + velocity_y


def get_formula(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[float, float]:
    # y = ax + b
    a = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - a * p1[0]
    return a, b


def get_intersection(a1: float, b1: float, a2: float, b2: float) -> Tuple[float, float] | None:
    if a1 == a2:
        return None
    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    return x, y


def validate_intersection(point: Tuple[int, int], intersection_point: Tuple[float, float], velocity_x: int,
                          velocity_y: int) -> bool:
    if (intersection_point[0] - point[0] < 0 and velocity_x < 0) or (
            intersection_point[0] - point[0] >= 0 and velocity_x >= 0):
        if (intersection_point[1] - point[1] < 0 and velocity_y < 0) or (
                intersection_point[1] - point[1] >= 0 and velocity_y >= 0):
            return True
    return False


if __name__ == '__main__':
    sample = read_data.get_data_09_all_line_ints('sample.txt')
    my_input = read_data.get_data_09_all_line_ints('input.txt')

    example_1 = solve_part_1(sample, 7, 27)
    part_1 = solve_part_1(my_input, 200000000000000, 400000000000000)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_2(sample)
    part_2 = solve_part_2(my_input)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
