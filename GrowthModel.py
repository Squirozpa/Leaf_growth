import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt

"""PARAMETERS"""
PR = 7742  # Photosynthetic rate
SNAR = 21400  # Specific nitrogen assimilation rate
mu = 20 #Nitrogen to carbon ratio
TR = 1123.2 #transpiration rate

beta_leaf = 302 #Maintnance leaf respiration rate (carbon)
beta_root = 1382.4 #Maintenance root respiration rate (carbon)
beta_stem = 6.054 #Maintenance stem respiration rate (carbon)

gamma_root = 900
 #Maintenance respiration rate (nitrogen)
gamma_leaf = 32 #Maintenance respiration rate (nitrogen)
gamma_stem = 2

r_rwr = 0.00296 #Leaf to root ratio
r_carbon = 375000 #carbon umol /g leaf
r_leaf = 375 # cm2 of leaf area / g of leaf
k = r_leaf/r_carbon #Leaf area to carbon ratio
r_swr = 1/50

overlap = 0.9 #Leaf area overlap factor
"""Functions"""
A_eff = lambda A: A**overlap
RW_t = lambda A:  r_rwr * A_eff(A)
SW_t = lambda A:  r_swr * A

C_uptake = lambda A: A_eff(A)*PR/2 - A*TR/2
N_uptake = lambda A: RW_t(A)*SNAR
C_maint = lambda A: beta_leaf * A + beta_root * RW_t(A) + beta_stem * SW_t(A)
N_maint = lambda A: gamma_leaf * A + gamma_root * RW_t(A) + gamma_stem * SW_t(A)

C_available = lambda A: C_uptake(A) - C_maint(A)
N_available = lambda A: N_uptake(A) - N_maint(A)

C_growth = lambda A: (C_available(A) + mu * N_available(A) - abs(C_available(A) - mu * N_available(A))) / 2

"""ODEs"""
dA_dt = lambda A: C_growth(A) *k
"""Simulation"""

# Time settings
dt = 0.1  # Time step (days)
T = 100 # Total simulation duration (days)
time = np.arange(0, T, dt)

# Initial conditions
A = np.zeros(len(time))  # Array to store leaf area over time
A[0] = 1  # Initial leaf area (cm²)

# Simulation loop
for i in range(1, len(time)):
    dA = dA_dt(A[i-1])  # Compute growth rate
    print(C_available(A[i-1]), N_available(A[i-1]), C_growth(A[i-1]), A[i-1])
    A[i] = A[i-1] + dA * dt  # Euler's method update

# Plot results

plt.plot(time, A, label="Leaf Area (Euler)")
plt.xlabel("Time (days)")
plt.ylabel("Leaf Area (cm²)")
plt.legend()
plt.show()

