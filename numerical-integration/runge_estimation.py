from functools import partial
from rectangle_rule import integrate_by_midpoints
from trapezoidal_rule import integrate_by_trapezoids
from simpsons_rule import integrate_by_parabolas
import math
import numpy as np


def partition(points):
    partitioned_points = []
    for i in range(1, len(points)):
        mid = (points[i] + points[i - 1]) / 2

        partitioned_points.extend([points[i - 1], mid, points[i]])

    return partitioned_points


def calculate_grid(integral, a, b, eps):
    points = list(np.linspace(a, b))
    result_grid = []

    for i in range(1, len(points)):
        h = points[i] - points[i - 1]
        borders = [points[i - 1], points[i]]

        partitioned = borders
        partitioned_estimation = partition(borders)

        integrated_segment = integral(borders)

        while True:
            integrated_partition = integral(partitioned_estimation)

            if abs(integrated_segment - integrated_partition) <= (eps * h) / (b - a):
                break
            else:
                partitioned = partitioned_estimation
                partitioned_estimation = partition(partitioned_estimation)

                integrated_segment = integrated_partition

        if len(result_grid) > 0:
            partitioned = partitioned[1:]

        result_grid.extend(partitioned)

    return result_grid


sin_integral = partial(integrate_by_midpoints, math.sin)

poinz = calculate_grid(sin_integral, 0, math.pi, 0.0001)

print(sin_integral(poinz), sin_integral(np.linspace(0, math.pi)))
