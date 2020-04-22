import numpy as np


def is_zero(v):
    return abs(v) < np.finfo(float).eps
