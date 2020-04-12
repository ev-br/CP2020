# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 20:51:54 2020

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt

x = [-1, -0.7, -0.43, -0.14, -0.14, 0.43, 0.71, 1, 1.29, 1.57, 1.86, 2.14, 2.43, 2.71, 3]
y = [-2.25, -0.77, 0.21, 0.44, 0.64, 0.03, -0.22, -0.84, -1.2, -1.03, -0.37, 0.61, 2.67, 5.04, 8.90]

x = np.array(x)
y = np.array(y)

n = x.shape[0]
m = 3

def phi(x,k):
    return x**k

def MNK(x, y, m):
    n = x.shape[0]
    A = np.zeros((n, m+1))
    for j in range(m+1):
        A[:,j] = phi(x,j)
    A_ = (np.linalg.inv(A.T @ A)) @ A.T #Псевдообратная матрица
    a = A_ @ y
    return a, A 

###########################################################################
def approx(x, y, a, m): #Pm(x) - полином с найденными параметрами
    yy = np.zeros_like(y)
    for i in range(yy.shape[0]):
        yy[i]=MNK(x, y, m)[1][i, :] @ a
    return yy

def sigma(m, Pm, y): #Квадрат отклонения
    sigma_q = 0
    summ = 0
    for k in range(n):
        summ += (Pm[k]-y[k])**2
    sigma_q = summ/(n-m+1)
    return sigma_q

sig = []
for i in range(x.shape[0]-1):
    sig.append(sigma(i, approx(x, y, MNK(x, y, i)[0], i), y)) 
sig = np.sqrt(np.array(sig)) #Массив отклонений для разных степеней полинома

plt.figure()
plt.title('Отклонение')
t = np.arange(x.shape[0]-1)
plt.ylim(0, 3.5) 
plt.xlim(0, 10)
plt.grid()
plt.plot(t, sig, label=r'$\sigma (m)$')  
plt.legend()  

m = 3 #Оптимальное отклонение из графика

plt.figure()
plt.title('Псевдообратная матрица')
plt.plot(x,y, 'o-', label='Данные', lw = 3, color = 'crimson')
plt.plot(x, (approx(x, y, MNK(x, y, m)[0], m)), label=r'Полином степени %s' % m, lw = 2)
plt.legend()
plt.grid()
###########################################################################    
plt.figure()
plt.title('Разложение QR')
plt.plot(x,y, 'o', label='Данные', lw = 3, color = 'crimson')
for i in range(1,4): #Все как в лекции
    Q, R = np.linalg.qr(MNK(x, y, i)[1])
    R1 = R[:,:i+1]
    f = (Q.T @ y)[:i+1]
    b = np.linalg.solve(R1, f)
    plt.plot(x, (approx(x, y, b, i)), label=r'Полином степени %s' % i, lw = 2)
plt.legend()
plt.grid()
###########################################################################

def funcc(t):
    return t**2 * np.cos(t)

n = 5

x = np.linspace(0.5*np.pi, np.pi, n)
t = np.linspace(0.5*np.pi, np.pi, 100)
y = funcc(x)
m = x.shape[0]

def l_i(t, x, i, m):
    l_ = 1
    for j in range(m):
        if j != i:
            l_ = l_ * (t - x[j]) / (x[i] - x[j])
    return l_

def L(y, t, x, m): #L(x)=y(x), причем единственно
    L_ = 0
    for j in range(m):
        L_ += y[j] * l_i(t, x, j, m)
    if m != 1:
        return L_
    else: 
        return L_ * np.ones_like(t)

plt.figure()
plt.plot(x, y, 'o', label=r'$x^2 \cos{x}$')
plt.title('Многочлены Лагранжа')
for i in range(1,6):
    plt.plot(t, L(y, t, x, i), '-', label=r'Интерполяция степени %s' % i)
plt.grid()
plt.legend()

##########################################################################

#Узлы определяю из уравнения cos(n*arccos(x))=0

for n in range(1,5):
    plt.figure()
    plt.title('Многочлены Чебышева')
    plt.plot(t, funcc(t), '-', label=r'$x^2 \cos{x}$')
    x_cheb = np.sort(np.cos(np.pi / n * (1/2 + np.arange(n))))
    #Отражение работает так: нормирую интервал [-1,1] на себя, домножаю на длину [pi/2, pi], смещаю 
    x_cheb_refl = (np.max(x) - np.min(x)) / 2 * x_cheb + (np.max(x) + np.min(x)) / 2
    y_cheb_refl = funcc(x_cheb_refl)
    plt.plot(x_cheb_refl, y_cheb_refl, 'o', label=r'Узлы, степень %s' % n)
    plt.plot(t, L(y_cheb_refl, t, x_cheb_refl, n), '-', lw = 4, color = 'crimson', alpha = 0.4, label=r'Интерполяция степени %s' % n)    
    plt.grid()
    plt.legend()

#Как видно, интерполяция по сетке Чебышева работает лучше