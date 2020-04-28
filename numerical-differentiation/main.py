import argparse
import random

from derivatives import *

import numpy as np
import yaml
from prettytable import PrettyTable

from utils import wrap_code


def process_function(_args):
    with open(_args.source, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            return

    modules = ['math']

    fun = wrap_code(config.get('fun', ''), modules)

    derivatives = config.get('derivatives', {})
    first_derivative = wrap_code(derivatives.get('first', ''), modules)
    second_derivative = wrap_code(derivatives.get('second', ''), modules)
    third_derivative = wrap_code(derivatives.get('third', ''), modules)

    domain = config.get('domain', {})
    inclusive = domain.get('inclusive', False)

    a = wrap_code(str(domain.get('a', 0)), modules)(0)
    b = wrap_code(str(domain.get('b', 0)), modules)(0)

    step = wrap_code(str(config.get('step', 0)), modules)(0)
    if inclusive:
        b += step

    arg_table = list(np.arange(a, b, step))
    val_table = list(map(fun, arg_table))

    diff_1 = FirstDerivative(val_table, step)
    diff_2 = SecondDerivative(val_table, step)
    diff_3 = ThirdDerivative(val_table, step)

    d_1_real = [first_derivative(x) for x in arg_table]
    d_2_real = [second_derivative(x) for x in arg_table]
    d_3_real = [third_derivative(x) for x in arg_table]

    d_1_numerical = [diff_1(i) for i in range(0, len(arg_table))]
    d_2_numerical = [diff_2(i) for i in range(0, len(arg_table))]
    d_3_numerical = [diff_3(i) for i in range(0, len(arg_table))]

    # Assertions
    # for i in range(0, len(arg_table)):
    #     first_second_step = (step if i == 0 or i == len(arg_table) - 1 else step ** 2) * 10
    #     third_step = (step ** 2 if 1 < i < len(arg_table) - 2 else step) * 10
    #
    #     assert abs(d_1_real[i] - d_1_numerical[i]) < first_second_step
    #     assert abs(d_2_real[i] - d_2_numerical[i]) < first_second_step
    #     assert abs(d_3_real[i] - d_3_numerical[i]) < third_step

    table_1 = PrettyTable([
        'x',
        'f(x)',
        'f\'(x)',
        'f\'(x) (numerical)',
        'Δ\''
    ])

    table_2 = PrettyTable([
        'f\'\'(x)',
        'f\'\'(x) (numerical)',
        'Δ\'\'',
        'f\'\'\'(x)',
        'f\'\'\'(x) (numerical)',
        'Δ\'\'\''
    ])

    for i in range(0, len(arg_table)):
        table_1.add_row([
            arg_table[i],
            val_table[i],
            d_1_real[i],
            d_1_numerical[i],
            abs(d_1_real[i] - d_1_numerical[i])
        ])

        table_2.add_row([
            d_2_real[i],
            d_2_numerical[i],
            abs(d_2_real[i] - d_2_numerical[i]),
            d_3_real[i],
            d_3_numerical[i],
            abs(d_3_real[i] - d_3_numerical[i])
        ])

    print(table_1)
    print(table_2)


def process_sensitivity(_args):
    with open(_args.source, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            return

    modules = ['math']

    fun = wrap_code(config.get('fun', ''), modules)

    derivatives = config.get('derivatives', {})
    first_derivative = wrap_code(derivatives.get('first', ''), modules)
    second_derivative = wrap_code(derivatives.get('second', ''), modules)
    third_derivative = wrap_code(derivatives.get('third', ''), modules)

    domain = config.get('domain', {})
    inclusive = domain.get('inclusive', False)

    a = wrap_code(str(domain.get('a', 0)), modules)(0)
    b = wrap_code(str(domain.get('b', 0)), modules)(0)

    step = wrap_code(str(config.get('step', 0)), modules)(0)
    if inclusive:
        b += step

    perturbation = config.get('perturbation', {})
    delta = wrap_code(str(perturbation.get('delta', 0)), modules)(0)

    arg_table = list(np.arange(a, b, step))
    val_table = list(map(lambda x: fun(x) + random.uniform(-delta, delta), arg_table))

    diff_1 = FirstDerivative(val_table, step)
    diff_2 = SecondDerivative(val_table, step)
    diff_3 = ThirdDerivative(val_table, step)

    d_1_real = [first_derivative(x) for x in arg_table]
    d_2_real = [second_derivative(x) for x in arg_table]
    d_3_real = [third_derivative(x) for x in arg_table]

    d_1_numerical = [diff_1(i) for i in range(0, len(arg_table))]
    d_2_numerical = [diff_2(i) for i in range(0, len(arg_table))]
    d_3_numerical = [diff_3(i) for i in range(0, len(arg_table))]

    table_1 = PrettyTable([
        'x',
        'f(x)',
        'f\'(x)',
        'f\'(x) (numerical)',
        'Δ\''
    ])

    table_2 = PrettyTable([
        'f\'\'(x)',
        'f\'\'(x) (numerical)',
        'Δ\'\'',
        'f\'\'\'(x)',
        'f\'\'\'(x) (numerical)',
        'Δ\'\'\''
    ])

    for i in range(0, len(arg_table)):
        table_1.add_row([
            arg_table[i],
            val_table[i],
            d_1_real[i],
            d_1_numerical[i],
            abs(d_1_real[i] - d_1_numerical[i])
        ])

        table_2.add_row([
            d_2_real[i],
            d_2_numerical[i],
            abs(d_2_real[i] - d_2_numerical[i]),
            d_3_real[i],
            d_3_numerical[i],
            abs(d_3_real[i] - d_3_numerical[i])
        ])

    print(table_1)
    print(table_2)


def parse_command_line():
    __parser = argparse.ArgumentParser(description='')
    subparsers = __parser.add_subparsers(help='sub-command help')

    function_parser = subparsers.add_parser('function')
    function_parser.add_argument('--source', dest='source', type=str, default='assignment.yml')
    function_parser.set_defaults(func=process_function)

    sensitivity_parser = subparsers.add_parser('sensitivity')
    sensitivity_parser.add_argument('--source', dest='source', type=str, default='assignment.yml')
    sensitivity_parser.set_defaults(func=process_sensitivity)

    return __parser


if __name__ == "__main__":
    _parser = parse_command_line()
    args = _parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        _parser.parse_args(['--help'])
