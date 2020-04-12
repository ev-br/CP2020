# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:16:59 2020

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt
rndm = np.random.RandomState(1)

############################################################################
def Jacobi(A, b, n_iter):
    diag_1d = np.diag(A)
    B = -A.copy()
    np.fill_diagonal(B, 0)
    invD = np.diag(1./diag_1d)
    BB = invD @ B 
    c = invD @ b
    y=[]
    x0 = np.ones(A.shape[0])
    x = x0
    n_max = 0 #шаг на котором метод сойдется
    while (abs(np.mean(A@x-b)) >= 0.01) and (n_max < n_iter):
        x = BB @ x + c
        y.append(np.mean(A@x-b)) #В качестве метода оценки сходимости буду брать среднеей значение Ax-b
        n_max += 1
    return x, y, n_max, np.linalg.norm(BB)

n = 10
n_iter= 50
A = rndm.uniform(size=(n, n)) + np.diagflat([15]*n)
b = rndm.uniform(size=n)

print('Метод Якоби: ', '\n')

print('Сходимость за ', Jacobi(A, b, n_iter)[2], 'шагов для диагонально доминирующей', '\n')

plt.figure()
plt.grid()

for i in range(1,6): #Посмотрим, на сколько строение матрицы влияет на сходимость: чем больше i, тем сильнее диагонализована матрица
    A = rndm.uniform(size=(n, n)) + np.diagflat([4*i]*n)
    t=np.linspace(0, Jacobi(A, b, n_iter)[2]-1, Jacobi(A, b, n_iter)[2])
    plt.title('Якоби')
    plt.xlabel('Количество шагов')
    plt.ylabel('$<Ax-b>$')
    plt.xlim(0,25)
    plt.plot(t, Jacobi(A, b, n_iter)[1], label=r'$||B|| = %s$' % round(np.linalg.norm(Jacobi(A, b, n_iter)[3]), 2))
    plt.legend()
    
#Как видно, если ||B||<1, то сходимость есть, иначе все улетает
############################################################################
def upper_mask(A): #Про функции np.tril и np.triu я узнал много позже, поэтому оставил так
    B=A.copy()
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if i<j:
                B[i,j]=1
            else:
                B[i,j]=0
    return B

def Seidel(A, b, n_iter):
    y=[]
    n_max = 0 #шаг на котором метод сойдется
    U = upper_mask(A) * A
    D = np.diag(np.diag(A))
    L = A - U - D
    x = np.ones(A.shape[0])
    while (abs(np.mean(A@x-b)) >= 0.01) and (n_max < n_iter):
        x = np.linalg.inv(L+D) @ (b - U @ x)
        y.append(np.mean(A@x-b)) #В качестве метода оценки сходимости буду брать среднеей значение Ax-b
        n_max += 1
    return x, y, n_max, np.linalg.norm(np.linalg.inv(L+D) @ U)

print('Метод Зейделя')

n = 10
n_iter= 50
A = rndm.uniform(size=(n, n)) + np.diagflat([12]*n)
b = rndm.uniform(size=n)

print('Сходимость за ', Seidel(A, b, n_iter)[2], 'шагов для треугольно доминирующей', '\n')

plt.figure()
plt.grid()

for i in range (1,6):
    A = rndm.uniform(size=(n, n)) + np.diagflat([4*i]*n)
    t=np.linspace(0, Seidel(A, b, n_iter)[2]-1, Seidel(A, b, n_iter)[2])
    plt.title('Зейдель')
    plt.xlabel('Количество шагов')
    plt.ylabel('$<Ax-b>$')
    plt.plot(t, Seidel(A, b, n_iter)[1], label=r'$||B|| = %s$' % round(np.linalg.norm(Seidel(A, b, n_iter)[3]), 2))
    plt.legend()
    
#Данный метод сходится даже при ||B||>1
#############################################################################

def minimum_residual(A, b, n_iter):
    r = np.zeros((n_iter, A.shape[0]))
    t = np.zeros_like(r)
    x0 = np.ones(A.shape[0])   
    xx = np.linalg.solve(A, b)
    dev = np.zeros_like(r)
    y = []
    for j in range(n_iter):
        r[j,:] = A @ x0 - b
        t[j,:] = (r[j,:].T @ (A @ r[j,:])) / np.linalg.norm(A @ r[j,:])**2
        x = x0 - t[j,:] * r[j,:]
        y.append(np.mean(A @ x - b))
        dev[j,:] = np.linalg.norm(xx - x)
        x0 = x
    return x, y, r, t, dev

n = 10
n_iter= 50
A = rndm.uniform(size=(n, n))
b = rndm.uniform(size=n)

plt.figure()
plt.grid()
plt.title('Схема минимальных остатков. Сходимость')
t = np.linspace(0, n_iter, n_iter)
plt.plot(t, minimum_residual(A, b, n_iter)[1], color = 'green')
plt.xlabel('Количество шагов')
plt.ylabel('$<Ax-b>$')

plt.figure()
plt.grid()
plt.title('Схема минимальных остатков. Параметр')
t = np.linspace(0, n_iter, n_iter)
plt.plot(t, minimum_residual(A, b, n_iter)[3][:,1], color = 'orange')
plt.xlabel('Количество шагов')
plt.ylabel(r'$\tau$')

plt.figure()
plt.grid()
plt.title('Схема минимальных остатков. Отклонение')
t = np.linspace(0, n_iter, n_iter)
plt.plot(t, minimum_residual(A, b, n_iter)[4][:,1], color = 'black')
plt.xlabel('Количество шагов')
plt.ylabel(r'$|x - x_{true}|$')

#Получилось так, что метод почти сходится, остается некоторая неустранимая постоянная ошибка
