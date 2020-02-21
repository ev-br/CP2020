# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:30:05 2020

@author: Тиннелла о Каллинике
"""
import numpy as np

N = 6
a = np.zeros((N, N), dtype=float)
for i in range(N):
    for j in range(N):
        a[i, j] = 3. / (0.6*i*j + 1)

a1 = a.copy()
a1[1, 1] = 3

np.set_printoptions(precision=3)

def diy_lu(A):
    N = a.shape[0]
    u = a.copy()
    L = np.eye(N)
    for j in range(N-1):
        lam = np.eye(N)
        gamma = u[j+1:, j] / u[j, j]
        lam[j+1:, j] = -gamma
        u = lam @ u

        lam[j+1:, j] = gamma
        L = L @ lam
        
    P = np.eye(N) #Начальная матрица перестановок - единичная матрица
    for j in range(N-1):
        max_index = np.argmax(abs(u[j:N,j]))+j #Ищем индекс максимального элемента
        u[:,0] = u[:,max_index] #Переставляетм столбец с максимальным элементом в начало
        P[:,0] = P[:, max_index]

    return L, u, P

def compose(a,b):
    c=np.zeros_like(a)
    for i in range(a[0,:].shape[0]):
        for j in range(b[:,0].shape[0]):
            c[i,j]=np.sum(a[i,:]*b[:,j])
    return c

print ('AP =')
print(compose(a,diy_lu(a)[2]))
print('')
print ('LU =')
print(compose(diy_lu(a)[0], diy_lu(a)[1]))