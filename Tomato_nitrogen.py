import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


r, p, u, t = 30, 100, 0.22, 0.29
R3, R5, R7 = 0.0002, 0.00002, 0.00004
a, b, alpha, beta = 200, 1, 0.08, 1.6

def f(C, N, Zn):
    return (alpha * C * N *Zn) / (1 + (beta * C * N * Zn))

R1 = lambda W: a - (b * W)  # R1 es una función de W, que es la razon de binding energy to total energy 

#R1*V(t)*f(C, N, Zn) corresponde a la cantidad de binding energy en el tiempo t
# dado que V(t) es peso / densidad :

dW_dt = lambda W, C, N, Zn: ((r * R1(W) )/p)*W*f(C, N, Zn) #Ecuacion diferencial del peso p(densidad) se trata como constante

dWc_dt = lambda W, C, N, Zn: (p* R3 *W) - W * f(C, N, Zn) #Ecuacion diferencial del peso en Carbono
dWn_dt = lambda W, C, N, Zn: (p* R5 *W) - u*  W * f(C, N, Zn) #Ecuacion diferencial del peso en Nitrogeno donde 1:u:t es la proporcion de C:N:Zn
dWz_dt = lambda W, C, N, Zn: (p* R7 *W) - t*  W * f(C, N, Zn) #Ecuacion diferencial del peso en Zinc donde 1:u:t es la proporcion de C:N:Zn

def tomato_growth(t, state):
    W, C, N, Zn = state
    dW = dW_dt(W, C, N, Zn)
    dWc = dWc_dt(W, C, N, Zn)
    dWn = dWn_dt(W, C, N, Zn)
    dWz = dWz_dt(W, C, N, Zn)
    return [dW, dWc, dWn, dWz]

def solve_tomato_growth(t_span, W0, C0, N0, Zn0):
    sol = solve_ivp(tomato_growth, t_span, [W0, C0, N0, Zn0], t_eval=np.linspace(t_span[0], t_span[1], 100))
    return sol.t, sol.y

def plot_growth(t, W, C, N, Zn):
    plt.figure(figsize=(10, 6))
    plt.plot(t, W, label='Weight (W)')
    plt.plot(t, C, label='Carbon (C)')
    plt.plot(t, N, label='Nitrogen (N)')
    plt.plot(t, Zn, label='Zinc (Zn)')
    plt.xlabel('Time')
    plt.ylabel('Amount')
    plt.title('Tomato Growth Model')
    plt.legend()
    plt.grid()
    plt.show() 

W0 = 5
Wc = 0.01
Wn = 2
Wz= 2
t_span = (0, 55) 
t, (W, C, N, Zn) = solve_tomato_growth(t_span, W0, Wc, Wn, Wz)
plot_growth(t, W, C, N, Zn)