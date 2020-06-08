import numpy as np
from scipy.optimize import curve_fit

a = np.random.uniform(-1, 1, (2, 3))
b = np.zeros(3)

for i in range(2):
    b[i] += a[i, :] ** 2
print(b)