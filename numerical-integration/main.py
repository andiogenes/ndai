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

    # Store YAML data n variables
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

    # Bind method names to corresponding functions
    methods = {
        'midpoint': integrate_by_midpoints,
        'trapezoid': integrate_by_trapezoids,
        'simpson': integrate_by_parabolas
    }

    points = np.arange(a, b + step, step)

    # Compile antiderivative to bytecode if it isn't None and compute a correct integral
    antiderivative_fun = compute_or_null(antiderivative, lambda x: wrap_code(x, modules))
    correct_integral = compute_or_null(antiderivative_fun, lambda x: x(b) - x(a))

    if auto_estimation:
        # Computations with automatic step
        table = PrettyTable(['method', 'eps', 'uniform steps count', 'steps count', 'correct', 'approximate', 'delta'])

        def append_row(_method_name, _method_fun):
            # Bind f(x) to quadrature
            method_integral = partial(_method_fun, fun)

            # Compute optimal grid for given integral with given precision
            grid = calculate_grid(method_integral, points, a, b, precision)

            # Compute integral numerically
            approximate_integral = _method_fun(fun, grid)

            # Add row to the table
            table.add_row([
                _method_name,  # Method of integration
                precision,  # Precision of table
                len(points) - 1,  # Count of segments in original grid
                len(grid) - 1,  # Count of segments in optimal grid
                correct_integral,  # Correct value of integral
                approximate_integral,  # Approximate value of integral
                compute_or_null(correct_integral, lambda x: abs(x - approximate_integral))  # | correct - approx |
            ])

        if method == 'all':
            # Calculate report for all methods
            for m in methods:
                append_row(m, methods[m])
        else:
            # Calculate report for one method
            append_row(method, methods[method])

        print(table)

    else:
        # Computation with constant step
        table = PrettyTable(['method', 'step', 'correct', 'approximate', 'delta'])

        def append_row(_method_name, _method_fun):
            # Compute integral numerically
            approximate_integral = _method_fun(fun, points)

            table.add_row([
                _method_name,  # Method of integration
                step,  # Grid step
                correct_integral,  # Correct value of integral
                approximate_integral,  # Approximate value of integral
                compute_or_null(correct_integral, lambda x: abs(x - approximate_integral))  # |correct - approx |
            ])

        if method == 'all':
            # Calculate reports for all methods
            for m in methods:
                append_row(m, methods[m])
        else:
            # Calculate report for one method
            append_row(method, methods[method])

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
