# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 13:08:50 2020

@author: Тиннелла о Каллинике
"""

import numpy as np
from numpy.testing import assert_allclose

def householder(vec):
    y=np.zeros_like(vec)
    y[0]=np.linalg.norm(vec)
    u=(vec-y)/(np.linalg.norm(vec-y))
    c=np.empty((vec.shape[0], vec.shape[0]))
    for i in range(vec.shape[0]):
        for j in range(vec.shape[0]):
            c[i,j]=u[j]*u[i]
    H=np.eye(vec.shape[0])-2*c
    vec = np.asarray(vec, dtype=float)
    if vec.ndim != 1:
        raise ValueError("vec.ndim = %s, expected 1" % vec.ndim)
    return vec@H, H

rndm = np.random.RandomState(1234)

vec = rndm.uniform(size=7)
v1, h = householder(vec)

assert_allclose(np.dot(h, v1), vec)

def Hi(A, i):
    m, n = A.shape
    x = householder(A[i:,i]) 
    H=np.zeros_like(A)
    H[:i,:i]=np.eye(i)
    H[i:, i:]=x[1]
    return H

def qr_decomp(a):
    m, n = a.shape
    Q=np.empty((m,m))
    R=np.empty((m,n))
    H=Hi(a, 1)
    for i in range(2, n-1)
        Q=np.dot(H, Hi(a, i))
        H=Q
    R=Q.T@A
    reurn Q, R
    
np.set_printoptions(suppress=True)

rndm = np.random.RandomState(1234)
A=rndm.uniform(size=(5,5))
m, n = A.shape
print(A)
print(Hi(A, 2))
print(Hi(A, 2)@A)






        
        