import math
import numpy as np

from derivatives import first_derivative
from parametric_line import create_parametric_line
from simpsons_rule import integrate_by_parabolas

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
