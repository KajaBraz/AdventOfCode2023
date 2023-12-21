"""
Instructions: https://adventofcode.com/2023/day/20
"""
import re

from AdventOfCode2023 import read_data


def parse(data):
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


def solve_part_1(data, presses=1000) -> int:
    send_to_dict, flip_flop_states, conjunction_pulses = parse(data)
    sent_pulses_cnt = {'low': 0, 'high': 0}
    for _ in range(presses):
        sent_pulses_cnt = process(send_to_dict, flip_flop_states, conjunction_pulses, sent_pulses_cnt)
    return sent_pulses_cnt['low'] * sent_pulses_cnt['high']


def flip_flop(receiver, flip_flop_dict, pulse, send_to_dict):
    if pulse == 'low':
        back_pulse = 'low' if flip_flop_dict[receiver] else 'high'
        flip_flop_dict[receiver] = not flip_flop_dict[receiver]
        return [(receiver, next_receiver, back_pulse) for next_receiver in send_to_dict[receiver]]
    return []


def conjunct(sender, receiver, conjunction_dict, pulse, send_to_dict):
    conjunction_dict[receiver][sender] = pulse
    if all(v == 'high' for v in conjunction_dict[receiver].values()):
        return [(receiver, next_receiver, 'low') for next_receiver in send_to_dict[receiver]]
    return [(receiver, next_receiver, 'high') for next_receiver in send_to_dict[receiver]]


def press(send_to_dict):
    return [('broadcaster', m, 'low') for m in send_to_dict['broadcaster']]


def process(send_to_dict, flip_flop_states, conjunction_pulses, sent_pulses_cnt):
    queue = press(send_to_dict)
    sent_pulses_cnt['low'] += 1
    while queue:
        sender, receiver, pulse = queue.pop(0)
        if receiver in flip_flop_states:
            queue.extend(flip_flop(receiver, flip_flop_states, pulse, send_to_dict))
        elif receiver in conjunction_pulses:
            queue.extend(conjunct(sender, receiver, conjunction_pulses, pulse, send_to_dict))
        sent_pulses_cnt[pulse] += 1
    return sent_pulses_cnt


if __name__ == '__main__':
    sample_1 = read_data.get_data_02_str_list('sample.txt')
    my_input_1 = read_data.get_data_02_str_list('input.txt')

    example_1 = solve_part_1(sample_1)
    part_1 = solve_part_1(my_input_1)
    print(f'Part 1\n\tExample: {example_1}\n\tSolution: {part_1}')
