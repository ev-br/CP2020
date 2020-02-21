# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 16:00:39 2020

@author: Тиннелла о Каллинике
"""

import numpy as np
from numpy import allclose
import cmath as cm

def solve_quad(b,c):
    if  b >= 0:
        x1=-b/2-cm.sqrt((b/2)**2-c) #я теряю немного точности, вычитая маленькое число из большого, но, оставляя перед корнем противоположный знак b я не накапливаю большую ошибку
        return x1, c/x1 #второй корень считаю по Виетту
    else:
        x2=-b/2+cm.sqrt((b/2)**2-c) #cmath автоматически работает с мнимой единицей так, чтобы за этим не следить
        return c/x2, x2
    
variants = [{'b': 4.0, 'c': 3.0},
            {'b': 2.0, 'c': 1.0},
            {'b': 0.5, 'c': 4.0},
            {'b': 1e10, 'c': 3.0},
            {'b': -1e10, 'c': 4.0},]

for var in variants:
    x1, x2 = solve_quad(**var)
    print(allclose(x1*x2, var['c']))