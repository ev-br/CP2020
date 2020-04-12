# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:52:05 2020

@author: Тиннелла о Каллинике
"""


import numpy as np
import matplotlib.pyplot as plt

def euler_solve(lam, u0, T, dt):
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    y = np.empty(num_steps+1)
    y[0] = u0
    for k in range(num_steps):
        y[k+1] = y[k] + dt*lam*y[k]
    return tt, y

#############################################################################################################

lam = - 0.5
dt = 0.5
plt.figure()
for i in range(12, int(12.5 / abs(lam)), 3):
    tt, y = euler_solve(lam, u0=1.0, T=5, dt = dt)
    plt.plot(tt, y, 'o--', label=r'dt = %s' % np.round(dt, 2))
    dt = 0.1 * i
tt = euler_solve(lam, u0=1.0, T=5, dt = 0.05)[0]
plt.plot(tt, np.exp(lam*tt), '-', lw=2, label='ground truth')
plt.title('Euler explicit')
plt.legend()
plt.grid()
plt.show()

#############################################################################################################

def euler_implicit_solve(lam, u0, T, dt):
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    y = np.empty(num_steps+1)
    y[0] = u0
    for k in range(num_steps):
        y[k+1] = y[k] / (1 - dt * lam)
    return tt, y

lam = - 0.5
u0 = 1
T = 5
dt = 0.4

plt.figure()
for i in range(12, int(12.5 / abs(lam)), 3):
    tt1, y1 = euler_implicit_solve(lam, u0, T, dt)
    plt.plot(tt1, y1, 'o--', label=r'dt = %s' % np.round(dt, 2))
    dt = 0.1 * i
tt1 = euler_implicit_solve(lam, u0, T, 0.01)[0]
plt.plot(tt1, np.exp(lam*tt1), '-', lw=2, label='ground truth')
plt.title('Euler implicit')
plt.legend()
plt.grid()
plt.show()

print('Как видно из графика, "Euler implicit" метод более устойчив к изменению dt')

###########################################################################################################

def euler_system_solve_explicit(A, u0, T, dt):
    A = np.atleast_1d(A)
    u0 = np.atleast_1d(u0)
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    y = np.empty((u0.shape[0], num_steps+1)) # y - матрица, каждый столбец которой есть вектор u  в точке x_n
    y[:, 0] = u0
    for k in range(num_steps):
        y[:, k+1] = y[:, k] + dt*(A @ y[:, k]) # Последовательно строю значение u в точке x_n для всех элементов вектора
    return tt, y

A = np.array([[-10, 10], [32, -499]])
u0 = np.array([1,0])
T = 5
dt = 0.01

t = euler_system_solve_explicit(A, u0, T, dt)[0]
y0 = euler_system_solve_explicit(A, u0, T, dt)[1][0]
y1 = euler_system_solve_explicit(A, u0, T, dt)[1][1]
plt.figure()
plt.plot(y0, y1, label = 'Решение системы ОДУ')
plt.legend()
plt.grid()
plt.xlabel('U[0]')
plt.ylabel('U[1]')
plt.title('explicit')
plt.show()

eig = np.linalg.eigvals(A)

s = np.max(abs(np.real(eig))) / np.min(abs(np.real(eig)))
print('\n', r'Stiffnes S = ', s)
if s>19: #Я немного поигрался с S и на 19 explicit метод начинает плохо работать
    print(r'S >> 1', '\n', 'Диагонализуя матрицу А можно прийти к соотношению d/dt(w) = Lw, где w = Q^(-1)u, L = Q^(-1)AQ. Таким образом, так как собственные значения матрицы A имеют разный порядок величины, на больших временах решение системы определяется уравнением с большим собственным значением, а шаг метода dt ~ 1/lam_min, что приводит к расхождению метода при заданном dt', '\n')

###########################################################################################################
    
def euler_system_solve_implicit(A, u0, T, dt):
    A = np.atleast_1d(A)
    u0 = np.atleast_1d(u0)
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    y = np.empty((u0.shape[0], num_steps+1)) # y - матрица, каждый столбец которой есть вектор u  в точке x_n
    y[:, 0] = u0
    for k in range(num_steps):
        y[:, k+1] = np.linalg.solve((np.eye(2) - dt*A),y[:, k])
    return tt, y

t = euler_system_solve_implicit(A, u0, T, dt)[0]
y0 = euler_system_solve_implicit(A, u0, T, dt)[1][0]
y1 = euler_system_solve_implicit(A, u0, T, dt)[1][1]
plt.figure()
plt.plot(y0, y1, label = 'Решение системы ОДУ')
plt.legend()
plt.grid()
plt.xlabel('U[0]')
plt.ylabel('U[1]')
plt.title('Implicit')
plt.show()

#Как говорилось на лекции emplicit метод работает для s >> 1 хорошо

###########################################################################################################

#U'' = -w^2U, {u':=v, v' = -w^2}. В терминах прошлой задачи имеем d/dt([u', v']) = [A_11*U + A_12 * v,
#A_21 * U + A_22 * v]. То есть A_11 = 0, A_12 = 1, A_21 - -w^2, A_22 = 0

w = 5

A = np.array([[0, 1],  [-w**2, 0]])
T = 2 * np.pi / w
dt = 0.005
u0 = np.array([1,0])

t = euler_system_solve_explicit(A, u0, 4 * T, dt)[0]
u = euler_system_solve_explicit(A, u0, 4 * T, dt)[1][0]

plt.figure()
plt.plot(t, u, label=r'u(t), $dt = $ %s' % dt, color = 'midnightblue')
plt.plot(t, u0[0] * np.cos(w * t) + u0[1] * np.sin(w * t), label = 'truth', lw = 3, color = 'crimson')
plt.xlabel('t')
plt.ylabel('u')
plt.legend()
plt.grid()
plt.title('Second order ODE. Explicit method')
plt.show()

plt.figure()
for i in range(4):
    dt = 10**(-i-1)
    t = euler_system_solve_explicit(A, u0, 4 * T, dt)[0]
    u = euler_system_solve_explicit(A, u0, 4 * T, dt)[1][0]
    v = euler_system_solve_explicit(A, u0, 4 * T, dt)[1][1]
    E = v**2  + u**2 * w**2
    plt.plot(t, E, label = r'$dt = $ %s' % dt)
plt.legend()
plt.ylim((23,45))
plt.grid()
plt.title('E(t). Explicit method')

##########################################################################################################

def runge_kutta_system_solve(A, u0, T, dt):
    A = np.atleast_1d(A)
    u0 = np.atleast_1d(u0)
    num_steps = int(T/dt)
    tt = np.arange(num_steps+1)*dt
    y = np.empty((u0.shape[0], num_steps+1)) # y - матрица, каждый столбец которой есть вектор u  в точке x_n
    y[:, 0] = u0
    for k in range(num_steps):
        y[:, k+1] = y[:, k] + dt*(A @ (y[:, k] + dt / 2 * A @ y[:, k]))
    return tt, y

A = np.array([[0, 1],  [-w**2, 0]])
T = 2 * np.pi / w
dt = 0.005
u0 = np.array([1,0])

t = runge_kutta_system_solve(A, u0, 4 * T, dt)[0]
u = runge_kutta_system_solve(A, u0, 4 * T, dt)[1][0]

plt.figure()
plt.plot(t, u, label=r'u(t), $dt = $ %s' % dt, color = 'midnightblue')
plt.plot(t, u0[0] * np.cos(w * t) + u0[1] * np.sin(w * t), label = 'truth', lw = 3, color = 'crimson')
plt.xlabel('t')
plt.ylabel('u')
plt.legend()
plt.grid()
plt.title('Second order ODE. Runge-Kutta method')
plt.show()

plt.figure()
for i in range(1, 4):
    dt = 10**(-i-1)
    t = runge_kutta_system_solve(A, u0, 4 * T, dt)[0]
    u = runge_kutta_system_solve(A, u0, 4 * T, dt)[1][0]
    v = runge_kutta_system_solve(A, u0, 4 * T, dt)[1][1]
    E = v**2  + u**2 * w**2
    plt.plot(t, E, label = r'$dt = $ %s' % dt)
plt.legend()
plt.ylim((24.995, 25.03))
plt.grid()
plt.title('E(t). Runge-Kutta method')
plt.show()

print('Как видно из графиков, метод Рунге - Кутта более устойчив к изменению шага, так как ошибка метода квадратична по dt, в отличие от линейной ошибки explicit метода')




    