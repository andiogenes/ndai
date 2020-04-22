import math
import numpy as np

from differentiation.derivatives import first_derivative
from integration.monte_carlo_method import integrate_by_monte_carlo
from parametric_line import create_parametric_line
from integration.simpsons_rule import integrate_by_parabolas

x_fn = math.cos
y_fn = math.sin

circle = create_parametric_line(x_fn, y_fn)
step = math.pi / 1000

param_points = list(np.arange(0, math.pi * 2 + step, step))

x_derivative = first_derivative(x_fn, (0, math.pi * 2), step)
y_derivative = first_derivative(y_fn, (0, math.pi * 2), step)

ydx_integral = integrate_by_parabolas(lambda t: y_fn(t) * x_derivative(t), param_points)
xdy_integral = integrate_by_parabolas(lambda t: x_fn(t) * y_derivative(t), param_points)

print(abs(ydx_integral), abs(xdy_integral))

ydx_monte_carlo = integrate_by_monte_carlo(lambda t: y_fn(t) * x_derivative(t), param_points, 10000)
xdy_monte_carlo = integrate_by_monte_carlo(lambda t: x_fn(t) * y_derivative(t), param_points, 10000)

print(abs(ydx_monte_carlo), abs(xdy_monte_carlo), (abs(ydx_monte_carlo) + abs(xdy_monte_carlo))/2)

ydxs_est = (abs(abs(ydx_integral) - math.pi), 'ydx simpson')
xdys_est = (abs(abs(xdy_integral) - math.pi), 'xdy simpson')
ydxm_est = (abs(abs(ydx_monte_carlo) - math.pi), 'ydx monte carlo')
xdym_est = (abs(abs(xdy_monte_carlo) - math.pi), 'xdy monte carlo')
s_est = (abs((abs(ydx_integral) + abs(xdy_integral))/2 - math.pi), 'middle simpson')
m_est = (abs((abs(ydx_monte_carlo) + abs(xdy_monte_carlo))/2 - math.pi), 'middle monte carlo')

print(min(ydxs_est, xdys_est, ydxm_est, xdym_est, s_est, m_est, key=lambda v: v[0]))
