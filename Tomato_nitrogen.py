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
    W_t, WC_t, WN_t, WZn_t = state
    C_t = WC_t / W_t
    N_t = WN_t / W_t
    Zn_t = WZn_t / W_t

    dW = dW_dt(W_t, C_t, N_t, Zn_t)
    dWc = dWc_dt(W_t, C_t, N_t, Zn_t)
    dWn = dWn_dt(W_t, C_t, N_t, Zn_t)
    dWz = dWz_dt(W_t, C_t, N_t, Zn_t)
    return [dW, dWc, dWn, dWz]

def solve_tomato_growth(t_span, W0, C0, N0, Zn0):
    sol = solve_ivp(tomato_growth, t_span, [W0, C0, N0, Zn0], t_eval=np.linspace(t_span[0], t_span[1], 100))
    return sol.t, sol.y

def plot_growth(t, W, C, N, Zn):
    plt.figure(figsize=(12, 10))

    # Subplot for Weight (W)
    plt.subplot(4, 1, 1)
    plt.plot(t, W, label='Weight (W)', color='blue')
    plt.xlabel('Time')
    plt.ylabel('Weight (W)')
    plt.title('Weight Over Time')
    plt.grid()

    # Subplot for Carbon (C)
    plt.subplot(4, 1, 2)
    plt.plot(t, C, label='Carbon (C)', color='green')
    plt.xlabel('Time')
    plt.ylabel('Carbon (C)')
    plt.title('Carbon Over Time')
    plt.grid()

    # Subplot for Nitrogen (N)
    plt.subplot(4, 1, 3)
    plt.plot(t, N, label='Nitrogen (N)', color='orange')
    plt.xlabel('Time')
    plt.ylabel('Nitrogen (N)')
    plt.title('Nitrogen Over Time')
    plt.grid()

    # Subplot for Zinc (Zn)
    plt.subplot(4, 1, 4)
    plt.plot(t, Zn, label='Zinc (Zn)', color='red')
    plt.xlabel('Time')
    plt.ylabel('Zinc (Zn)')
    plt.title('Zinc Over Time')
    plt.grid()

    plt.tight_layout()
    plt.show()

W0 = 5
Wc = 0.01
Wn = 2
Wz= 2
t_span = (0, 50) 
t, (W, C, N, Zn) = solve_tomato_growth(t_span, W0, Wc, Wn, Wz)
