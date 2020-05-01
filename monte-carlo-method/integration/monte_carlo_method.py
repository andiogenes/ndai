import random


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
