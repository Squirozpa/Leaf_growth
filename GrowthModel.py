import numpy as np
from scipy.integrate import solve_ivp, odeint
import matplotlib.pyplot as plt

"""PARAMETERS"""
PR = 7742  # Photosynthetic rate
SNAR = 21400  # Specific nitrogen assimilation rate
mu = 20 #Nitrogen to carbon ratio
TR = 2123.2 #transpiration rate

beta_leaf = 1150 #Maintnance leaf respiration rate (carbon)
beta_root = 50082.4 #Maintenance root respiration rate (carbon)
beta_stem = 6.054 #Maintenance stem respiration rate (carbon)

gamma_leaf = 55 #Maintenance respiration rate (nitrogen)
gamma_root = 900 #Maintenance respiration rate (nitrogen)
gamma_stem = 2

r_rwr = 0.00296 #Leaf to root ratio
r_carbon = 605000 #carbon umol /g leaf (esto solo considera el carbono de la hoja y no el de la planta completa)
r_leaf = 375 # cm2 of leaf area / g of leaf
k = r_leaf/r_carbon #Leaf area to carbon ratio
r_swr = 1/50

overlap = 0.9 #Leaf area overlap factor
"""Functions"""
A_eff = lambda A: A**overlap
RW_t = lambda A:  r_rwr * A
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
plt.figure(figsize=(10, 8))

# Subplot 1: Leaf Area Growth
plt.subplot(2, 1, 1)
plt.plot(time, A, label="Leaf Area (Euler Method)", color='blue')
plt.title("Leaf Area Growth Over Time")
plt.xlabel("Time (days)")
plt.ylabel("Leaf Area (cm²)")
plt.legend()
plt.grid()  

# Subplot 2: Available Resources
plt.subplot(2, 1, 2)
plt.plot(time, C_available(A), label="Carbon Available", color='green')
plt.plot(time, N_available(A), label="Nitrogen Available", color='orange')
plt.xlabel("Time (days)")
plt.ylabel("Available Resources")
plt.legend()
plt.grid()  

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
