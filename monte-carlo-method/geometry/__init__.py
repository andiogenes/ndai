def point_inside_polygon(contour, point):
    num_intersections = 0
    for i in range(0, len(contour)):
        min_point = contour[i]
        max_point = contour[(i + 1) % len(contour)]

        if min_point[1] > max_point[1]:
            min_point, max_point = max_point, min_point

        if max_point[1] <= point[1] or min_point[1] > point[1]:
            continue

        orient = orientation(min_point, max_point, point)
        if orient == 0:
            return True
        if orient > 0:
            num_intersections += 1

    return bool(num_intersections % 2)


def orientation(a, b, c):
    v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if v < 0:
        return -1
    if v > 0:
        return 1
    return 0


def create_parametric_line(x, y):
    def parametric_line(t):
        return x(t), y(t)

    return parametric_line
