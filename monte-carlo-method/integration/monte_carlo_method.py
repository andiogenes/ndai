import random

from geometry import point_inside_polygon


def integrate_by_monte_carlo(fn, a, b, count):
    """
    Computes integral by Monte Carlo method.
    """
    segment_length = b - a

    points = []

    acc = 0
    for i in range(0, count):
        u = random.uniform(a, b)
        acc += fn(u)
        points.append(u)

    return (segment_length / count) * acc, points


def integrate_by_monte_carlo_geometrically(contour, count):
    """
    Computes integral by geometrical Monte Carlo method.
    """

    # Calculate bounds of integration rectangle
    left = min(contour, key=lambda _x: _x[0])[0]
    top = min(contour, key=lambda _x: _x[1])[1]
    right = max(contour, key=lambda _x: _x[0])[0]
    bottom = max(contour, key=lambda _x: _x[1])[1]

    width = right - left
    height = bottom - top

    points_in = []
    points_out = []
    for i in range(0, count):
        x = random.uniform(left, right)
        y = random.uniform(top, bottom)

        if point_inside_polygon(contour, (x, y)):
            points_in.append((x, y))
        else:
            points_out.append((x, y))

    area = len(points_in) / count * width * height

    return area, points_in, points_out
