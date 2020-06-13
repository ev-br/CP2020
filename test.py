import numpy as np
from scipy.optimize import curve_fit

def ddbas(x,n):
    if n==0:
        return 0.
    else:
        return (-2 + n)*(-1 + n)*(-2 + x)*(-1 + x)*(-1 + 1/n + x)**(-3 + n) + 2*(-1 + 1/n + x)**(-1 + n) + 2*(-1 + n)*(-1 + 1/n + x)**(-2 + n)*(-3 + 2*x)

def dif_dif_basis(x, n):
    if n == 0:
        return 0
    else:
        return (x - 2) * (x - 1) * (n - 1) * (n - 2) * (x - 1 + 1 / n) ** (n - 3) + 2 * (x - 1 + 1 / n) ** (n - 1) + (n - 1) * (x - 1 + 1 / n) ** (n - 2) * (2 * x - 3)
    
print(np.linalg.norm(ddbas(np.linspace(0, 1, 100), 5) - dif_dif_basis(np.linspace(0, 1, 100), 5)))