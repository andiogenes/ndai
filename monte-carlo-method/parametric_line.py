def create_parametric_line(x, y):
    def parametric_line(t):
        return x(t), y(t)

    return parametric_line
