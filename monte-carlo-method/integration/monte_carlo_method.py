import random


def integrate_by_monte_carlo(fn, points, count):
    segment_length = points[len(points) - 1] - points[0]

    acc = 0
    for i in range(0, count):
        u = points[random.randint(0, len(points) - 1)]
        acc += fn(u)

    return (segment_length / count) * acc
