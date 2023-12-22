"""
Instructions: https://adventofcode.com/2023/day/20
"""

import math
import re
from typing import List, Dict, Tuple

from AdventOfCode2023 import read_data


def parse(data: List[str]) -> Tuple[Dict[str, List[str]], Dict[str, bool], Dict[str, Dict[str, str]]]:
    d, dd = {}, {}
    for row in data:
        k, v = row.split(' -> ')
        d[k] = v
    d = {k: [vv for vv in re.split(r'[\s,]', v) if vv] for k, v in d.items()}
    flip_flop_states = {k[1:]: False for k in d.keys() if k[0] == '%'}
    conjunction_pulses = {k[1:]: {} for k in d.keys() if k[0] == '&'}
    for k in conjunction_pulses:
        for kk, vv in d.items():
            if k in vv:
                conjunction_pulses[k][kk[1:]] = 'low'
    for k, v in d.items():
        if k != 'broadcaster':
            k = k[1:]
        dd[k] = v
    return dd, flip_flop_states, conjunction_pulses


def solve_part_1(data: List[str]) -> int:
    senders_receivers_dict, flip_flop_states, conjunction_pulses = parse(data)
    sent_pulses_cnt = {'low': 0, 'high': 0}
    for _ in range(1000):
        sent_pulses_cnt, _ = process(senders_receivers_dict, flip_flop_states, conjunction_pulses, sent_pulses_cnt)
    return sent_pulses_cnt['low'] * sent_pulses_cnt['high']


def solve_part_2(data: List[str], target_high_pulse_modules: Dict[str, int]) -> int:
    senders_receivers_dict, flip_flop_states, conjunction_pulses = parse(data)
    sent_pulses_cnt = {'low': 0, 'high': 0}
    button_press_cnt = 1
    while any(v == 0 for v in target_high_pulse_modules.values()):
        sent_pulses_cnt, target_high_pulse_modules = process(senders_receivers_dict, flip_flop_states,
                                                             conjunction_pulses,
                                                             sent_pulses_cnt, button_press_cnt,
                                                             target_high_pulse_modules)
        button_press_cnt += 1
    return lcm_multiple_nums(target_high_pulse_modules.values())


def flip_flop(receiver: str, flip_flop_dict: Dict[str, bool], pulse: str,
              senders_receivers_dict: Dict[str, List[str]]) -> List[Tuple[str, str, str]]:
    if pulse == 'low':
        back_pulse = 'low' if flip_flop_dict[receiver] else 'high'
        flip_flop_dict[receiver] = not flip_flop_dict[receiver]
        return [(receiver, next_receiver, back_pulse) for next_receiver in senders_receivers_dict[receiver]]
    return []


def conjunct(sender: str, receiver: str, conjunction_dict: Dict[str, Dict[str, str]], pulse: str,
             senders_receivers_dict: Dict[str, List[str]]) -> List[Tuple[str, str, str]]:
    conjunction_dict[receiver][sender] = pulse
    if all(v == 'high' for v in conjunction_dict[receiver].values()):
        return [(receiver, next_receiver, 'low') for next_receiver in senders_receivers_dict[receiver]]
    return [(receiver, next_receiver, 'high') for next_receiver in senders_receivers_dict[receiver]]


def press(senders_receivers_dict: Dict[str, List[str]]) -> List[Tuple[str, str, str]]:
    return [('broadcaster', m, 'low') for m in senders_receivers_dict['broadcaster']]


def process(senders_receivers_dict: Dict[str, List[str]], flip_flop_states: Dict[str, bool],
            conjunction_pulses: Dict[str, Dict[str, str]], sent_pulses_cnt: Dict[str, int], button_press_cnt: int = 0,
            target_high_pulse_modules: Dict[str, int] = None) -> Tuple[Dict[str, int], Dict[str, int]]:
    queue = press(senders_receivers_dict)
    sent_pulses_cnt['low'] += 1
    while queue:
        sender, receiver, pulse = queue.pop(0)
        if target_high_pulse_modules and button_press_cnt and sender in target_high_pulse_modules and pulse == 'high':
            target_high_pulse_modules[sender] = button_press_cnt
        if receiver in flip_flop_states:
            queue.extend(flip_flop(receiver, flip_flop_states, pulse, senders_receivers_dict))
        elif receiver in conjunction_pulses:
            queue.extend(conjunct(sender, receiver, conjunction_pulses, pulse, senders_receivers_dict))
        sent_pulses_cnt[pulse] += 1
    return sent_pulses_cnt, target_high_pulse_modules


def parse_part_2(raw_data: str, flip_flop_states: Dict[str, bool],
                 conjunction_pulses: Dict[str, Dict[str, str]]) -> None:
    data = raw_data.split('\n')
    data = [row.split(' -> ') for row in data]
    for row in data:
        for x in row[1].split(', '):
            if x in flip_flop_states:
                print(row[0], f'%{x}')
            elif x in conjunction_pulses:
                print(row[0], f'&{x}')
            else:
                print(row[0], x)


def lcm_multiple_nums(nums: List[int] | Dict.values) -> int:
    res = 1
    for n in nums:
        res = math.lcm(res, n)
    # return a * b // math.gcd(a, b)
    return res


if __name__ == '__main__':
    sample = read_data.get_data_02_str_list('sample.txt')
    my_input = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1(sample)
    part_1 = solve_part_1(my_input)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')

    # Discover the target modules (by visualising the nodes as a graph)
    # Initialise the rounds in which they send 'high' pulse (set them to 0)
    target_high_pulse_modules_input = {'dc': 0, 'vp': 0, 'cq': 0, 'rv': 0}
    part_2 = solve_part_2(my_input, target_high_pulse_modules_input)

    print(f'Part 2\n\tSolution: {part_2}')
