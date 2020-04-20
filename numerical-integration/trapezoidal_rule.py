def integrate_by_trapezoids(fn, points):
    acc = 0
    for i in range(1, len(points)):
        h = points[i] - points[i - 1]

        acc += (fn(points[i]) + fn(points[i - 1])) * h
        
    return acc / 2
