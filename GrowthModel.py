import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

"""PARAMETERS"""
PR = 7776  # Photosynthetic rate
SNAR = 21400  # Specific nitrogen assimilation rate
mu = 0.05 #Nitrogen to carbon ratio
alpha = 1123.2 #transpiration rate

beta_leaf = 302 #Maintnance leaf respiration rate (carbon)
beta_root = 1382.4 #Maintenance root respiration rate (carbon)
beta_stem = 6.054 #Maintenance stem respiration 1rate (carbon)

gamma_root = 1000
 #Maintenance respiration rate (nitrogen)
gamma_leaf = 6 #Maintenance respiration rate (nitrogen)

r_root = 0.000296 #Leaf to root ratio
r_carbon = 37500 #carbon umol /g leaf
r_area = 375 # cm2 of leaf area / g of leaf
r_leaf = r_area /r_carbon #Leaf area to carbon ratio
"""Functions"""
C_in = lambda A: PR * A
N_in = lambda RW: SNAR * RW
N_eff = lambda N:  N /mu # Effective nitrogen

C_out = lambda A, RW: alpha * A + beta_leaf * A + beta_root * RW
N_out = lambda A, RW: gamma_leaf * A + gamma_root * RW

U_t = lambda C, N: min(C, N_eff(N)) #Available carbon and nitrogen
RW_t = lambda A: A * r_root #Root weight

"""ODEs"""
dC_dt = lambda A, RW, C, N: C_in(A) - C_out(A, RW) - U_t(C, N) #Carbon balance
dN_dt = lambda A, RW, C, N: N_in(RW) - N_out(A, RW) - U_t(C,N)*mu #Nitrogen balance
dA_dt = lambda C, N: r_leaf * U_t(C,N)

"""ODE system"""
def growth_model(t, state):
    A, C, N = state
    RW = RW_t(A)  # Calculate root weight based on leaf area
    dA = dA_dt(C, N)
    dC = dC_dt(A, RW, C, N)
    dN = dN_dt(A, RW, C, N)
    return [dA, dC, dN]

A0 = 1  # Initial leaf area (cm²)
N0 = 10  # Initial nitrogen (g)
C0 = 0  # Initial carbon (g)

t_span = (0, 10)  # Time span for the simulation (days)
t_eval = np.linspace(t_span[0], t_span[1], 100)  # Time points to evaluate the solution

sol = solve_ivp(growth_model, t_span, [A0, C0, N0], t_eval=t_eval)

"Plotting the results"
plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
plt.plot(sol.t, sol.y[0], label='Leaf Area (A)', color='green')
plt.xlabel('Time (days)')
plt.ylabel('Leaf Area (cm²)')
plt.title('Leaf Area Growth Over Time')
plt.legend()
plt.grid()
plt.subplot(3, 1, 2)
plt.plot(sol.t, sol.y[1], label='Carbon (C)', color='blue')
plt.xlabel('Time (days)')
plt.ylabel('Carbon (umol)')
plt.title('Carbon Growth Over Time')
plt.legend()
plt.grid()
plt.subplot(3, 1, 3)
plt.plot(sol.t, sol.y[2], label='Nitrogen (N)', color='orange')
plt.xlabel('Time (days)')
plt.ylabel('Nitrogen (umol)')
plt.title('Nitrogen Growth Over Time')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

