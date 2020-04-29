import argparse
from functools import partial

import numpy as np
import yaml
from prettytable import PrettyTable

from rectangle_rule import integrate_by_midpoints
from runge_estimation import calculate_grid
from simpsons_rule import integrate_by_parabolas
from trapezoidal_rule import integrate_by_trapezoids

from utils import wrap_code, compute_or_null


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

    points = np.arange(a, b + step, step)

    ad_fun = compute_or_null(antiderivative, lambda x: wrap_code(x, modules))
    correct_integral = compute_or_null(ad_fun, lambda x: x(b) - x(a))

    if auto_estimation:
        table = PrettyTable(['method', 'eps', 'uniform steps count', 'steps count', 'correct', 'approximate', 'delta'])

        def fill_table(_method_name, _method_fun):
            method_integral = partial(_method_fun, fun)
            grid = calculate_grid(method_integral, points, a, b, precision)

            approximate_integral = _method_fun(fun, grid)

            table.add_row([
                _method_name,
                precision,
                len(points)-1,
                len(grid)-1,
                correct_integral,
                approximate_integral,
                compute_or_null(correct_integral, lambda x: abs(x - approximate_integral))
            ])

        if method == 'all':
            for m in methods:
                fill_table(m, methods[m])
        else:
            fill_table(method, methods[method])

        print(table)

    else:
        table = PrettyTable(['method', 'step', 'correct', 'approximate', 'delta'])

        def fill_table(_method_name, _method_fun):
            approximate_integral = _method_fun(fun, points)

            table.add_row([
                _method_name,
                step,
                correct_integral,
                approximate_integral,
                compute_or_null(correct_integral, lambda x: abs(x - approximate_integral))
            ])

        if method == 'all':
            for m in methods:
                fill_table(m, methods[m])
        else:
            fill_table(method, methods[method])

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
