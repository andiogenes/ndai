def integrate_by_midpoints(midpoints, fn, h):
    def with_constant_step():
        acc = 0
        for v in midpoints:
            acc += fn(v) * h
        return acc

    def with_automatic_step():
        assert len(midpoints) == len(h)

        acc = 0
        for i, v in enumerate(midpoints):
            acc += fn(v) * h[i]
        return acc

    if isinstance(h, list):
        return with_automatic_step()
    else:
        return with_constant_step()
