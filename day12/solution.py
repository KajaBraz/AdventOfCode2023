"""
Instructions: https://adventofcode.com/2023/day11
"""

import operator
import re
from typing import List

from AdventOfCode2023 import read_data


def solve_part_1(data, multiplier) -> int:
    rows_expanded = double_rows(data)
    cols_expanded = double_columns(data)
    galaxeis = find_galaxies(data)

    dists = set()
    for g1 in galaxeis:
        for g2 in galaxeis:
            if g1 != g2:
                dist = calculate_dist(g1,g2,data,rows_expanded,cols_expanded,multiplier)
                dists.add((g1,g2,dist))
    return sum([item[-1] for item in dists])//2

def contains_expanded(g1,g2,expanded, mlt):
    cnt = 0
    for expanded_row in expanded:
        if min(g1[0],g2[0]) <= expanded_row < max(g1[0],g2[0]):
            cnt+=(mlt-1)
        # print('   ', g1, g2, cnt)
    return cnt
def contains_expanded_c(g1,g2,expanded, mlt):
    cnt = 0
    for expanded_col in expanded:
        if min(g1[1],g2[1]) <= expanded_col < max(g1[1],g2[1]):
            # print('   ')
            cnt+=(mlt-1)
    return cnt

def solve_part_2(data) -> int:
    rows_expanded = double_rows(data)
    cols_expanded = double_columns(data)
    galaxeis = find_galaxies(data)

    dists = set()
    for g1 in galaxeis:
        for g2 in galaxeis:
            if g1 != g2:
                dist = calculate_dist(g1,g2,data,rows_expanded,cols_expanded,1000000)
                dists.add((g1,g2,dist))
    return sum([item[-1] for item in dists])//2


def double_rows(data):
    return double(data)

def double_columns(data):
    columns = [''.join([data[i][j] for i in range(len(data))]) for j in range(len(data[0]))]
    to_expand = double(columns)
    return to_expand

def double(data):
    to_expand = []
    for i in range(len(data)):
        if len(set(data[i])) == 1 and data[i][0] == '.':
            to_expand.append(i)
    return to_expand

def find_galaxies(data):
    galaxies = []
    for i in range(len(data)):
        galaxies_cols = [m.start() for m in re.finditer('#', data[i])]
        galaxies.extend([(i, column) for column in galaxies_cols])
    return galaxies

def calculate_dist(galaxy_1, galaxy_2, data, exp_rows,exp_cols,mlt):
    return abs(galaxy_2[0]-galaxy_1[0]) + contains_expanded(galaxy_1,galaxy_2,exp_rows,mlt)+abs(galaxy_2[1]-galaxy_1[1])+contains_expanded_c(galaxy_1,galaxy_2,exp_cols,mlt)

def solve(data) -> int:
    return



if __name__ == '__main__':
    part_1,part_2,example_1,example_2=0,0,0,0
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1(sample, 2)
    part_1 = solve_part_1(my_input,2)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve_part_1(sample, 1000000)
    part_2 = solve_part_1(my_input,1000000)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
