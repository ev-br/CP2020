# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 14:18:04 2020

@author: user
"""
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *

#####################################################################

def newton_iteration(f, fder, x0, eps=1e-5, maxiter=1000):
    niter = 0
    while (abs(f(x0)) > eps) and (niter <= maxiter - 1):
        x0=x0-f(x0)/fder(x0)
        niter += 1
    return x0, niter

x0 = 10 #Начальное приближение
x = newton_iteration(lambda x: x**2-1, lambda x: 2*x, x0)[0]
num = newton_iteration(lambda x: x**2-1, lambda x: 2*x, x0)[1]

print('Метод Ньютона: ', '\n', 'Ответ ', x, 'получен за ', num, 'шагов', '\n')

def newton_iteration_modified(f, fder, m, x0, eps=1e-5, maxiter=10000):
    niter = 0
    while (abs(f(x0)) > eps) and (niter <= maxiter - 1):
        x0=x0-m*f(x0)/fder(x0)

        niter += 1
    return x0, niter

x0 = 10 #Начальное приближение
x = newton_iteration_modified(lambda x: (x**2-1)**2, lambda x: 4*x*(x**2-1), 2, x0)[0]
num = newton_iteration_modified(lambda x: (x**2-1)**2, lambda x: 4*x*(x**2-1), 2, x0)[1]

print('Модифицированный метод Ньютона: ', '\n', 'Ответ ', x, 'получен за ', num, 'шагов', '\n')


t = np.linspace(0, 10, 11)
y = np.zeros_like(t)
for i in range(0, t.shape[0]):
    y[i] = newton_iteration_modified(lambda x: (x**2-1)**2, lambda x: 4*x*(x**2-1), i, x0, eps=1e-5, maxiter=10000)[1]

#Изобразим сходмость метода в зависимости от параметра m, как видим, при
#m<1, m>3 нет сходимости

plt.figure()
plt.xlim(0, 6)
plt.ylim(0, 25)
plt.title('Метод Ньютона')
plt.xlabel('$m$')
plt.ylabel('$Niter$')
plt.plot(t, y, label = 'Сходимость метода в зависимости от $m$')
plt.plot(t, y, '*')
plt.legend()
plt.grid()

######################################################################
s=np.linspace(0, 5, 100)
plt.figure()
plt.plot(s, np.sqrt(s), label='sqrt(x)')
plt.plot(s, np.cos(s), label='cos(x)')
plt.grid()
plt.legend()
plt.xlabel('$x$')
plt.ylabel('$f(x)$')


def fixed(f, x0, eps=1e-5, maxiter=1e5):
    niter = 0
    while (abs(f(x0)) > eps) and (niter < maxiter):
        x0 = x0 - f(x0)
        niter += 1
    return x0, niter

x0 = 0.5
x = fixed(lambda x: np.sqrt(x)-np.cos(x), x0)[0]
num = fixed(lambda x: np.sqrt(x)-np.cos(x), x0)[1]

print('Метод фикс. точки: ', '\n', 'Ответ ', x, 'получен за ', num, 'шагов', '\n')

def fixed_modified(f, a, x0, eps=1e-5, maxiter=1e5):
    niter = 0
    while (abs(f(x0)) > eps) and (niter < maxiter):
        x0 = x0 - a*f(x0)
        niter += 1
    return x0, niter

x0 = 0.5
a=0.9
x = fixed_modified(lambda x: np.sqrt(abs(x))-np.cos(x), a, x0)[0]
num = fixed_modified(lambda x: np.sqrt(abs(x))-np.cos(x), a, x0)[1]

print('Модифиц. метод фикс. точки: ', '\n', 'Ответ ', x, 'получен за ', num, 'шагов', '\n')

t = np.linspace(0.1, 1.5, 100)
y = np.zeros_like(t)
for i in range(t.shape[0]):
    y[i] = fixed_modified(lambda x: np.sqrt(abs(x))-np.cos(x), t[i], x0)[1]

plt.figure()
plt.xlim(0, 1.7)
plt.ylim(0, 25)
plt.title('Метод фикс. точки')
plt.xlabel('$m$')
plt.ylabel('$Niter$')
plt.plot(t, y, label = 'Сходимость метода в зависимости от $m$')
plt.plot(t, y, '*')
plt.plot(t[np.argmin(y)], np.min(y), '*', lw=8, label='Оптимальная a')
plt.legend()
plt.grid()
######################################################################

def fractal(x0):
    x, n = newton_iteration_modified(lambda x: x**3-1, lambda x: 3*x**2, 1, x0, eps=1e-4, maxiter=10)
    y = np.zeros(3)
    for i in range(y.shape[0]):
        y[i] = abs(x - np.exp(1j * 2 * i * np.pi / 3))
    return np.argmin(abs(y)) #Назовем области с одинаковыми решениями "0, 1 и 2"
                        #тогда будем выдавать номер того решения, которому
                        #соответствует y=0, т.е. номер с минимальным элементом

# Для удобства хочу выводить отдельное окошко  
def command_clicked():
    global N
    global M
    N=int(EntryA.get())
    M=int(EntryB.get())
    root.destroy()
    root.quit()
    return N, N

root = Tk()
root.title("Фракталы")
root.geometry("600x250")
root.resizable(width=False, height=False)
Label(root, text='Введите желаемое количество фракталов ', width=17, font='Arial 12').place(x=10, y=10, width=350, height=50)
EntryA = Entry(root, width=7, font='Arial 16')
EntryA.place(x=30, y=70, width=200, height=50)
Label(root, text='Введите размер поля MxM ', width=17, font='Arial 12').place(x=370, y=10, width=200, height=50)
EntryB = Entry(root, width=7, font='Arial 16')
EntryB.place(x=370, y=70, width=200, height=50)
btn = Button(root, text='Ввести', font='Arial 16', width=3, command=command_clicked).place(x=250, y=150, width=100, height=50)
Label(root, text='Для красивой картинки количество фракталов > 30 ', width=17, font='Arial 6').place(x=370, y=200, width=200, height=50)
root.mainloop()

n, m = N, M
 
def plt_(n, m):
    plt.figure()
    x = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if j != n // 2 or i != n // 2:
                x[j, i] = fractal(-m + i * 2 * m / n + (-m + j * 2 * m / n)*1j)
    plt.imshow(x, cmap='seismic', extent=[-m, m, -m, m])
    plt.title('Фракталы')
    plt.xlabel('Re(x)')
    plt.ylabel('Im(x)')

plt_(n, m)