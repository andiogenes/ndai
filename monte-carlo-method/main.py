import argparse

import matplotlib.pyplot as plt
import numpy as np
import yaml
from prettytable import PrettyTable

from differentiation.derivatives import first_derivative
from geometry import create_parametric_line
from integration.monte_carlo_method import integrate_by_monte_carlo, integrate_by_monte_carlo_geometrically
from integration.simpsons_rule import integrate_by_parabolas
from spline import CubicSpline
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

    # Store YAML data in variables
    fun = config.get('fun', {})
    x_fun = wrap_code(str(fun.get('x', '')), modules, param='t')
    y_fun = wrap_code(str(fun.get('y', '')), modules, param='t')

    domain = config.get('domain', {})
    a = wrap_code(str(domain.get('a', '0')), modules)(0)
    b = wrap_code(str(domain.get('b', '0')), modules)(0)

    differentiation = config.get('differentiation', {})
    differentiation_step = wrap_code(str(differentiation.get('step', '0')), modules)(0)

    simpson = config.get('simpson', {})
    step = wrap_code(str(simpson.get('step', '0')), modules)(0)

    monte_carlo = config.get('monte_carlo', {})
    count = wrap_code(str(monte_carlo.get('count', '0')), modules)(0)

    # Compute first derivative of x(t)
    x_dtv = first_derivative(x_fun, (a, b), differentiation_step)

    t = np.linspace(a, b, num=100)
    x = [x_fun(v) for v in t]
    y = [y_fun(v) for v in t]

    # Define splines for x(t), y(t)
    x_spline = CubicSpline(zip(t, x))
    y_spline = CubicSpline(zip(t, y))

    plot_domain = np.linspace(min(t), max(t), num=1000)
    plot_x_values = [x_spline(v) for v in plot_domain]
    plot_y_values = [y_spline(v) for v in plot_domain]

    # Plot region defined by x = x(t), y = y(t)
    fig, ax = plt.subplots()
    ax.plot(plot_x_values, plot_y_values, color='green')
    ax.grid()

    # Calculate integrals
    line_fun = create_parametric_line(x_spline, y_spline)
    contour = [line_fun(v) for v in np.linspace(a, b, num=1000)]

    monte_carlo_integral, monte_carlo_points_in, monte_carlo_points_out \
        = integrate_by_monte_carlo_geometrically(contour, count)
    simpson_integral = integrate_by_parabolas(lambda _t: y_fun(_t) * x_dtv(_t), np.arange(a, b + step, step))

    table = PrettyTable(['Simpson', 'Monte-Carlo'])
    table.add_row([abs(simpson_integral), abs(monte_carlo_integral)])
    print(table)

    # Scatter points from Monte Carlo method
    ax.scatter([p[0] for p in monte_carlo_points_in], [p[1] for p in monte_carlo_points_in], 2, 'red')
    ax.scatter([p[0] for p in monte_carlo_points_out], [p[1] for p in monte_carlo_points_out], 2, 'blue')
    plt.show()


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
