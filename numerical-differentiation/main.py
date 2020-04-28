import argparse
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

    table = PrettyTable([
        'fun',
        'f\'',
        'f\' (numerical)',
        'f\'\'',
        'f\'\' (numerical)',
        'f\'\'\'',
        'f\'\'\' (numerical)'
    ])

    for i in range(0, len(arg_table)):
        x = arg_table[i]

        table.add_row([
            val_table[i],
            first_derivative(x),
            diff_1(i),
            second_derivative(x),
            diff_2(i),
            third_derivative(x),
            diff_3(i)
        ])

    print(table)


def process_sensitivity(_args):
    pass


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
