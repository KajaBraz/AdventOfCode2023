"""
Instructions: https://adventofcode.com/2023/day/1
"""

from typing import List

from AdventOfCode2023 import read_data


def solve1(data: List[str]) -> int:
    s = 0
    for row in data:
        digits = remove_nondigits(row)
        n = int(digits[0] + digits[-1])
        s += n
    return s


def solve2(data: List[str]) -> int:
    for row in range(len(data)):
        data[row] = convert(data[row])
    return solve1(data)


def convert(row: str) -> str:
    nums = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    nums = {n: str(i + 1) for i, n in enumerate(nums)}
    i = 0
    digits = ''

    while i < len(row):
        k = i
        j = i + 1
        if row[i].isdigit():
            digits += row[k:j + 1]
        else:
            while j < len(row):
                if row[k:j + 1] in nums:
                    digits += nums[row[k:j + 1]]
                    k = j
                j += 1
        i += 1
    return digits


def remove_nondigits(s: str) -> str:
    return ''.join(ch for ch in s if ch.isdigit())


if __name__ == '__main__':
    sample_input1 = read_data.get_data_02_str_list('sample1.txt')
    sample_input2 = read_data.get_data_02_str_list('sample2.txt')
    example1 = solve1(sample_input1)
    example2 = solve2(sample_input2)

    my_input = read_data.get_data_02_str_list('input.txt')
    part1 = solve1(my_input)
    part2 = solve2(my_input)

    print(f'Part 1\n\tExample: {example1}\n\tSolution: {part1}')
    print(f'Part 2\n\tExample: {example2}\n\tSolution: {part2}')
