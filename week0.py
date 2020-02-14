# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 00:25:57 2020

@author: Тиннелла о Каллинике
"""

import sympy
import numpy as np
from numpy.testing import assert_allclose

x = sympy.Symbol('x')
N = 25
exact = [float(sympy.integrate(x**n * sympy.exp(1 - x), (x, 0, 1))) for n in range(N)]

atol=exact[24] #Абсолютная точность - характерное минимальное значение последовательности exact
rtol=atol/np.mean(exact) #Относительная точность - отношение абсолютной точности к среднему значению последовательности

def upwards_recursion(n): 
    I0=np.exp(1)-1
    if n==0:
        return I0
    else:
        return n*upwards_recursion(n-1)-1
    
values = [upwards_recursion(n) for n in range(N)]
print('Upwards recurtion:')
for value, exact_value in zip(values, exact):
    print(value, exact_value)
print('Success status: ', np.allclose(values, exact, rtol, atol)) #Success status - параемтр, показывающй совпадают ли элементы полученного массива с "истинными" значениями в пределах погрешности


def downwards_recursion(n):
        if n==24:
            return 0
        else:
            return (downwards_recursion(n+1)+1)/n

    
values1 = np.concatenate(([exact[0]], [downwards_recursion(n) for n in range(1,25)])) #Чтобы избеать деления на ноль в рекурсии, положим нулевым элементом известное значение I0
print('Downwards recurtion:')
for value, exact_value in zip(values1, exact):
    print(value, exact_value)
print('Success status: ', np.allclose(values1, exact, rtol, atol))

#Вывод: из-за того, что машина считает неточно, функция upwards_recursion уходит на -inf после того, как элементы последовательности
#становятся <0. Функция downwards_recurtion хорошо описывает сходимость элементов к "истинным" на больших n, но плохо определяет
#значения на малых

def mixed_recursion(n):
    if np.allclose([downwards_recursion(n)], [exact[n]], rtol, atol):
        if n==24:
            return 0
        else:
            return (downwards_recursion(n+1)+1)/n
    elif np.allclose([upwards_recursion(n)], [exact[n]], rtol, atol):
        if n==0:
            return np.exp(1)-1
        else:
            return n*upwards_recursion(n-1)-1
        
values2 = np.concatenate(([exact[0]], [mixed_recursion(n) for n in range(1,25)])) 
print('Mixed recurtion:')
for value, exact_value in zip(values2, exact):
    print(value, exact_value)
assert_allclose(values2, exact, rtol, atol)
print('Success status: ', np.allclose(values2, exact, rtol, atol))
print('rtol', rtol, 'atol', atol)