def integrate_by_midpoints(fn, points):
    """
    Computes integral on a given grid by midpoint rule
    """
    acc = 0
    for i in range(1, len(points)):
        mid = (points[i] + points[i - 1]) / 2
        h = points[i] - points[i - 1]

        acc += fn(mid) * h

    return acc
