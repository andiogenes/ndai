from utils import is_zero


def first_derivative(fn, domain, h):
    def central(x):
        return (fn(x + h) - fn(x - h)) / (2 * h)

    def forward(x):
        return (fn(x + h) - fn(x)) / h

    def backward(x):
        return (fn(x) - fn(x - h)) / h

    def selection(x):
        if is_zero(abs(x - domain[0])):
            return forward(x)
        elif is_zero(abs(x - domain[1])):
            return backward(x)
        else:
            return central(x)

    return selection
