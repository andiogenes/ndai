def integrate_by_parabolas(fn, points):
    """
    Computes integral on given grid by Simpson's rule.
    """
    acc = 0
    for i in range(1, len(points)):
        mid = (points[i] + points[i - 1]) / 2
        h = points[i] - points[i - 1]

        acc += (fn(points[i - 1]) + 4 * fn(mid) + fn(points[i])) * h

    return acc / 6
