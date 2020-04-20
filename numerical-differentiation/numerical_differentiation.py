import numpy as np
import math
from derivatives import *

step = math.pi / 20
arg_table = list(np.arange(0, math.pi * 2, step))

val_table = list(map(math.sin, arg_table))

n = len(val_table)

diff_1 = FirstDerivative(val_table, step)
diff_2 = SecondDerivative(val_table, step)
diff_3 = ThirdDerivative(val_table, step)

print("x\t\tu(x)\t\tu'(x)\t\tu''(x)\t\tu'''(x)")
for i in range(0, n):
    d_1 = diff_1(i)
    d_2 = diff_2(i)
    d_3 = diff_3(i)
    print('{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}'.format(arg_table[i], val_table[i], d_1, d_2, d_3))
