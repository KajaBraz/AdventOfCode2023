"""
Instructions: https://adventofcode.com/2023/day/7
"""

from collections import Counter
from typing import List, Tuple

from AdventOfCode2023 import read_data


def solve(data: List[str], joker: bool) -> int:
    hands = [data[i] for i in range(len(data)) if i % 2 == 0]
    bids = [int(data[i]) for i in range(len(data)) if i % 2 == 1]
    hands_bids = zip(bids, hands)
    strengths = [determine_strength(cards, joker) for cards in hands]
    cnts = Counter(strengths)
    hands_strengths = sorted(zip(strengths, hands_bids))
    ordered = update_ranks(hands_strengths, cnts, joker)
    return calculate(ordered)


def use_joker(cards: str) -> str:
    s = cards.replace('J', '')
    if s:
        longest = Counter(s).most_common()
        cards = cards.replace('J', longest[0][0])
    return cards


def determine_strength(cards: str, joker: bool) -> int:
    cards = use_joker(cards) if joker else cards
    cards_set = set(cards)
    set_len = len(cards_set)
    if set_len == 1:
        return 7
    if set_len == 2:
        a = cards_set.pop()
        if cards.count(a) in [1, 4]:
            return 6
        if cards.count(a) in [2, 3]:
            return 5
    if set_len == 3:
        if any(cards.count(card) == 3 for card in cards_set):
            return 4
        return 3
    if set_len == 4:
        return 2
    return 1


def calculate(hands: List[Tuple[int, str]]) -> int:
    return sum(hands[i][0] * (i + 1) for i in range(len(hands)))


def get_same_strength_hands(hands: List[Tuple[int, Tuple[int, str]]], strength: int) -> List[Tuple[int, str]]:
    return [hands[i][1] for i in range(len(hands)) if hands[i][0] == strength]


def get_card_value(card: str, joker: bool) -> int:
    chars_vals = {card: v for v, card in enumerate('AKQJT98765432' if not joker else 'AKQT98765432J')}
    return chars_vals[card]


def order_same_strengths(hands: List[Tuple[int, str]], joker: bool) -> List[Tuple[int, str]]:
    hands = [(hand, [get_card_value(card, joker) for card in hand[-1]]) for hand in hands]
    ordered = sorted(hands, key=lambda x: x[-1], reverse=True)
    return [hand[0] for hand in ordered]


def update_ranks(hands: List[Tuple[int, Tuple[int, str]]], counts: Counter, joker: bool) -> List[
    Tuple[int, str]]:
    ordered = []
    i = 0
    while i < len(hands):
        strength, hand = hands[i]
        if counts[strength] == 1:
            ordered.append(hand)
            i += 1
        else:
            same_strength_hands = get_same_strength_hands(hands, strength)
            ordered.extend(order_same_strengths(same_strength_hands, joker))
            i += len(same_strength_hands)
    return ordered


if __name__ == '__main__':
    sample_input = read_data.get_data_00('sample.txt').split()
    my_input = read_data.get_data_00('input.txt').split()

    example_1 = solve(sample_input, False)
    part_1 = solve(my_input, False)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    example_2 = solve(sample_input, True)
    part_2 = solve(my_input, True)
    print(f'Part 2\n\tExample: {example_2}\n\tSolution: {part_2}')
