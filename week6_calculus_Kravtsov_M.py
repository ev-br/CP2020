# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:21:22 2020

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt
from math import log
import scipy.integrate as integrate

def deriv(f, x, h): 
    return (f(x+h)-f(x)) / h

x = 0
print('h        --   err')
for h in [1e-2, 1e-3, 1e-4, 1e-5]:
    err = deriv(lambda x: x**3, x, h)
    print("%5f -- %7.4g" % (h, err))

print('\n', 'Как и ожидалось, при уменьшении h в диапазоне [1e-2, 1e-5] ошибка стремится к нулю', '\n')

def three_point(f, x, h):
        return (-1.5 * f(x) + 2 * f(x + h) - 0.5 * f(x+2*h)) / h

def fu():
    return lambda x: np.piecewise(x, [x == 0, x > 0], [0, lambda x: x**2 * np.log(x)])

x = 1
y = 0
err_deriv = []
err_3_point = []
t = []

for i in range(20):
    h = 10**(-i)
    t.append(h)
    err_deriv.append(abs(1-deriv(fu(), x, h)))
    err_3_point.append(abs(1-three_point(fu(), x, h)))
    
plt.figure()
plt.title(r'$x^2 \ln{x},  x=1$')
plt.loglog(t, err_deriv, 'o-b', label='two points rule', color = 'blue')
plt.loglog(t, err_3_point, 'o-b', label='three points rule', color = 'crimson')
plt.xlabel(r'$h$')
plt.ylabel(r'error')
plt.legend()
plt.grid()
plt.show()
print('Используя "two points rule" ошибка убывает линейно до некоего момента, а, используя "three points rule" - квадратично. После некоторой точки h становится пренебрежима мала по сравнению с x и ошибка начинает осциллировать')
##########################################################################################################
y = 0
err_deriv = []
err_3_point = []
t = []

for i in range(1, 20):
    h = 10**(-i)
    t.append(h)
    err_deriv.append(abs(0-deriv(fu(), y, h)))
    err_3_point.append(abs(0-three_point(fu(), y, h)))
    
plt.figure()
plt.title(r'$x^2 \ln{x},  x=0$')
plt.loglog(t, err_deriv, 'o-b', label='two points rule', color = 'blue')
plt.loglog(t, err_3_point, 'o-b', label='three points rule', color = 'crimson')
plt.xlabel(r'$h$')
plt.ylabel(r'error')
plt.grid()
plt.legend()
plt.show()
###########################################################################################################
def func(x):
    return x**3 + 5 * x**4

a = 0.6
b = 0.8
eps = 1e-4

I = integrate.quad(lambda x: x**3 + 5 * x**4, 0.6, 0.8)

def midpoint_rule(f, a, b, eps):
    Q1 = 0
    Q2 = eps
    k1 = []
    k2 = []
    N = 2
    while (abs(Q1 - Q2) >= eps) and (N < 500):
        Q1 = 0
        Q2 = eps
        t1 = np.linspace(a, b, N)
        t2 = np.linspace(a, b, 2 * N)
        for i in range(1, t1.shape[0]):
            Q1 += (t1[i] - t1[i-1]) * f((t1[i-1] + t1[i])/2)
        for i in range(1, t2.shape[0]):
            Q2 += (t2[i] - t2[i-1]) * f((t2[i-1] + t2[i])/2)
        Q2 -= eps
        k1.append(Q1)
        k2.append(Q2)
        N += 1
    return Q2, N

N_opt = midpoint_rule(lambda x: x**3 + 5 * x**4, a, b, eps)[1]
t = np.linspace(a, b, N_opt)

plt.figure()
plt.title(r'Midpoint rule')
plt.plot(t, func(t), label = r'$x^3 + 5x^4$', color = 'midnightblue', lw = 3)
for i in range(1, N_opt):
    plt.plot([t[i-1], t[i-1]], [func((t[i-1] + t[i])/2), 0], '-', alpha = 0.5, color = 'crimson')
    plt.plot([t[i-1], t[i]], [func((t[i-1] + t[i])/2), func((t[i-1] + t[i])/2)], '-', color = 'crimson')
    plt.plot([t[i], t[i]], [func((t[i-1] + t[i])/2), 0], '-', alpha = 0.5, color = 'crimson')
    plt.plot([t[i-1], t[i]], [0, 0], '-', color = 'crimson')
plt.legend()
plt.grid()
plt.show()

np.allclose(midpoint_rule(lambda x: x**3 * 5 * x**4, 0.6, 0.8, 1e-4), I, 1e-4)
print(r'Error -- ', abs(midpoint_rule(lambda x: x**3 + 5 * x**4, 0.6, 0.8, 1e-4)[0] - I[0]), '\n', r'N -- ', N_opt)

###########################################################################################################

I2 = integrate.quad(lambda x: np.sin(x**0.5) / x, 0, 1)

Q_straight = midpoint_rule(lambda x: np.sin(x**0.5) / x, 0, 1, 1e-4)[0]
N_straight = midpoint_rule(lambda x: np.sin(x**0.5) / x, 0, 1, 1e-4)[1]

print('\n','\n', 'Straight midpoint rule:', '\n', 'Error -- ', abs(I2[0] - Q_straight), '\n', 'N = ', N_straight)


Q_sing = midpoint_rule(lambda x: np.sin(x**0.5) / x - 1 / np.sqrt(x), 0, 1, 1e-4)[0] + 2
N_sing = midpoint_rule(lambda x: np.sin(x**0.5) / x - 1 / np.sqrt(x), 0, 1, 1e-4)[1] 

np.allclose(I2, Q_sing)

def funcc(x):
    return np.sin(np.sqrt(x)) / x - 1 / np.sqrt(x)

s = np.linspace(eps, 1, N_sing)

plt.figure()
plt.title(r'Midpoint rule')
plt.plot(s, funcc(s), label = r'$\frac{\sin{\sqrt{x}}}{x} - \frac{1}{\sqrt{x}}$', color = 'midnightblue', lw = 3)
for i in range(1, N_sing):
    plt.plot([s[i-1], s[i-1]], [funcc((s[i-1] + s[i])/2), 0], '-', alpha = 0.5, color = 'crimson')
    plt.plot([s[i-1], s[i]], [funcc((s[i-1] + s[i])/2), funcc((s[i-1] + s[i])/2)], '-', color = 'crimson')
    plt.plot([s[i], s[i]], [funcc((s[i-1] + s[i])/2), 0], '-', alpha = 0.5, color = 'crimson')
    plt.plot([s[i-1], s[i]], [0, 0], '-', color = 'crimson')
plt.legend(fontsize = 'xx-large')
plt.grid()
plt.show()

print('Modified midpoint rule:', '\n', 'Error -- ', abs(I2[0] - Q_sing), '\n', 'N = ', N_sing)
