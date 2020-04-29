import argparse

import numpy as np
import yaml
from prettytable import PrettyTable

from rectangle_rule import integrate_by_midpoints
from simpsons_rule import integrate_by_parabolas
from trapezoidal_rule import integrate_by_trapezoids

from utils import wrap_code


def process_integration(_args):
    # Parse YAML file with input data
    with open(_args.source, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            return

    # Modules required by Python expressions in assignments
    modules = ['math']

    fun = wrap_code(str(config.get('fun', '')), modules)
    antiderivative = config.get('antiderivative', None)

    domain = config.get('domain', {})
    a = wrap_code(str(domain.get('a', 0)), modules)(0)
    b = wrap_code(str(domain.get('b', 0)), modules)(0)

    integration = config.get('integration', {})
    method = integration.get('method', 'midpoint')
    step = wrap_code(str(integration.get('step', '0')), modules)(0)

    estimation = integration.get('estimation', {})
    auto_estimation = estimation.get('auto', False)
    precision = wrap_code(str(estimation.get('precision', '0')), modules)(0)

    methods = {
        'midpoint': integrate_by_midpoints,
        'trapezoid': integrate_by_trapezoids,
        'simpson': integrate_by_parabolas
    }

    method_fun = methods[method]

    if auto_estimation:
        pass
    else:
        points = np.arange(a, b + step, step)

        ad_fun = wrap_code(antiderivative, modules) if antiderivative is not None else None
        correct_integral = ad_fun(b) - ad_fun(a) if ad_fun is not None else None

        approximate_integral = method_fun(fun, points)

        table = PrettyTable(['method', 'step', 'correct', 'approximate', 'delta'])
        table.add_row([
            method,
            step,
            correct_integral,
            approximate_integral,
            abs(correct_integral-approximate_integral) if correct_integral is not None else None
        ])

        print(table)


def parse_command_line():
    __parser = argparse.ArgumentParser(description='')
    __parser.add_argument('--source', dest='source', type=str, default='assignment.yml')
    __parser.set_defaults(func=process_integration)

    return __parser


if __name__ == "__main__":
    _parser = parse_command_line()
    args = _parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        _parser.parse_args(['--help'])
