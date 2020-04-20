def integrate_by_trapezoids(points, fn, h):
    def with_constant_step():
        acc = 0
        for i in range(1, len(points)):
            acc += fn(points[i]) + fn(points[i - 1])
        return (acc / 2) * h

    def with_automatic_step():
        acc = 0
        for i in range(1, len(points)):
            acc += (fn(points[i]) + fn(points[i - 1])) * h[i - 1]
        return acc / 2

    if isinstance(h, list):
        return with_automatic_step()
    else:
        return with_constant_step()
