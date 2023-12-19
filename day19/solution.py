"""
Instructions: https://adventofcode.com/2023/day/19
"""

import re
from typing import List, Dict, Tuple

from AdventOfCode2023 import read_data


def solve_part_1(data: List[str]) -> int:
    workflows, ratings = parse(data)
    ratings = [re.findall(r'\d+', p) for p in ratings]  # x m a s
    ratings = [[int(n) for n in r] for r in ratings]
    workflows = parse_workflows(workflows)
    print(workflows)
    r = 0
    for part in ratings:
        k = execute_part(part, workflows)
        if k == 'A':
            r += sum(part)
    return r


def execute_part(part: List[int], workflows: Dict[str, List[List[Tuple[str, str, int], str] | str]]) -> str:
    keys = {'x': 0, 'm': 1, 'a': 2, 's': 3}
    k = 'in'

    while k not in ['A', 'R']:
        x = workflows[k]
        for exp in x:
            if k in ['A', 'R']:
                return k
            if len(exp) == 1:
                k = exp[0]
            else:
                y, dest = exp
                operation = y[1]
                if operation == '>':
                    if part[keys[y[0]]] > y[-1]:
                        k = dest
                        break
                elif operation == '<':
                    if part[keys[y[0]]] < y[-1]:
                        k = dest
                        break
                else:
                    raise Exception('unreachabel')
    return k


def parse_workflow(workflow: str) -> Tuple[str, List[List[Tuple[str, str, int], str] | str]]:
    key, x = workflow.split('{', 1)
    exprs = x[:-1].split(',')
    cases = [expr.split(':') for expr in exprs]
    cases = [[(x[0][0], x[0][1], int(x[0][2:])), x[1]] if len(x) > 1 else x for x in cases]
    return key, cases


def parse_workflows(workflows) -> Dict[str, List[List[Tuple[str, str, int], str] | str]]:
    workflows_dict = {}
    for workflow in workflows:
        key, cases = parse_workflow(workflow)
        workflows_dict[key] = cases
    return workflows_dict


def parse(d: List[str]) -> List[List[str]]:
    r = [[]]
    for row in d:
        if row:
            r[-1].append(row)
        else:
            r.append([])
    return r
