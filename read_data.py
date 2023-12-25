import re


def get_data_00(path: str) -> str:
    with open(path) as f:
        content = f.read()
    return content.strip()


def get_data_01_int_list(path: str) -> list[int]:
    """
    File content example:

    173
    178
    179

    Return example: [173, 178, 179]
    """

    data = open(path, 'r').read()
    numbers = [int(number) for number in data.split()]
    return numbers


def get_data_02_str_list(path: str) -> list[str]:
    """
    File content example:

    217, 490 -> 217, 764
    44, 270 -> 373, 599

    Return example: ['217,490 -> 217,764', '44,270 -> 373,599', '440,139 -> 440,303']
    """

    with open(path) as f:
        input_lines = [line.rstrip() for line in f]
    return input_lines


def get_data_03_two_dim_int_list(path: str) -> list[list[int]]:
    """
    File content example:

    91 60 70 64 83
    35 41 79 55 31
     7 58 25  3 47

    Return example: [[91, 60, 70, 64, 83], [35, 41, 79, 55, 31], [7, 58, 25, 3, 47]]
    """

    input_data = [num.strip() for num in open(path, 'r').read().split('\n')]
    input_data = [[int(num) for num in row.split()] for row in input_data if len(row) > 0]
    return input_data


def get_data_04_two_dim_str_list(path: str) -> list[list[str]]:
    """
    File content example:

    A Y
    B X
    C Z

    Return example: [['A', 'Y'], ['B', 'X'], ['C', 'Z']]
    """

    with open(path) as f:
        input_lines = [line.strip() for line in f]
    return [line.split() for line in input_lines]


def get_data_05_str_int_two_cols(path: str) -> list[tuple[str, int]]:
    """
    File content example:

    R 4
    U 4
    L 3

    Return example: [('A', 4), ('U', 4), ('L', 3)]
    """

    return [(c[0], int(c[1])) if len(c) == 2 else (c[0],) for c in [row.split() for row in open(path, 'r').readlines()]]


def get_data_06_alternate_rows_lists(path: str) -> tuple[list[str], list[int]]:
    """
    File content example:

    forward
    2
    forward
    6
    forward
    8

    Return example: (['forward', 'forward', 'forward'], [2, 6, 8])
    """

    data = open(path, 'r').read().split()
    directions = [data[i] for i in range(len(data)) if i % 2 == 0]
    values = [int(data[i]) for i in range(len(data)) if i % 2 == 1]

    return directions, values


def get_data_07(path: str) -> tuple[set[tuple[int, int]], list[tuple[str, int]]]:
    """
    File content example:

    323,511
    1240,588
    1210,140
    fold along x = 655
    fold along y = 447
    fold along x = 327

    Return example: ({(335, 767), (13, 753), (843, 289)}, [('x', 655), ('y', 447), ('x', 327)])
    """

    point_pattern = re.compile(r'\d*,\d*')
    instrucrtions_pattern = re.compile(r'[xy]=\d*')
    points = set()
    with open(path) as f:
        s = f.read()
        pairs = point_pattern.findall(s)
        instructions = [i.split('=') for i in instrucrtions_pattern.findall(s)]
    pairs = [pair.split(',') for pair in pairs]
    points.update([(int(x), int(y)) for x, y in pairs])
    instructions = [(i[0], int(i[1])) for i in instructions]
    return points, instructions


def get_data_08(path: str) -> tuple[str, dict[str, str]]:
    """
    File content example:

    HBHVVNPCNFPSVKBPPCBH
    HV -> B
    KS -> F
    NH -> P

    Return example: (HBHVVNPCNFPSVKBPPCBH, {'HV': 'B', 'KS': 'F', 'NH': 'P'})
    """

    with open(path, 'r') as f:
        lines = f.read()
    input_rules = lines.split()
    start = input_rules[0]
    input_rules = {input_rules[a]: input_rules[a + 2] for a in range(1, len(input_rules) - 1) if (a - 1) % 3 == 0}
    return start, input_rules


def get_data_09_all_line_ints(path: str) -> list[list[int]]:
    """
    File content example:

    2-4,6-8
    2-3,4-5
    5-7,7-9

    Return example: [[2, 4, 6, 8], [2, 3, 4, 5], [5, 7, 7, 9]]
    """

    data = get_data_02_str_list(path)
    return [[int(n) for n in gr] for gr in [re.findall(r'-?\d+', row) for row in data]]


