"""
Instructions: https://adventofcode.com/2023/day/4
"""

import re
from typing import Tuple, List, Set

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> int:
    cards = get_cards(data)
    cnt = 0
    for winning_set, nums in cards:
        won = count_winning(winning_set, nums)
        cnt += get_score(won)
    return cnt


def solve_part_2(data: List[str]) -> int:
    cards = get_cards(data)
    instances = {x: 1 for x in range(len(cards))}
    cur = 0
    for i in range(len(cards)):
        winning_set, nums = cards[i]
        won_cards = count_winning(winning_set, nums)
        for won in range(cur + 1, cur + won_cards + 1):
            instances[won] += instances[cur]
        cur += 1
    return sum(instances.values())


def get_cards(data: List[str]) -> List[Tuple[Set[int], Set[int]]]:
    cards = []
    for card in data:
        _, valid = card.split(':')
        winning, nums = valid.split('|')
        winning = re.findall(r'\d+', winning)
        nums = re.findall(r'\d+', nums)
        cards.append((set(winning), set(nums)))
    return cards


def count_winning(winning: Set[int], nums: Set[int]) -> int:
    return len(winning.intersection(nums))


def get_score(cnt: int) -> int:
    return 2 ** (cnt - 1) if cnt else 0


if __name__ == '__main__':
    sample_input = read_data.get_data_02_str_list('sample.txt')

    example_1 = solve_part_1(sample_input)
    example_2 = solve_part_2(sample_input)

    my_input = read_data.get_data_02_str_list('input.txt')

    part_1 = solve_part_1(my_input)
    part_2 = solve_part_2(my_input)

    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
