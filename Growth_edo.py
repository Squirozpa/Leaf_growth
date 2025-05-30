import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parameters
LA= 3.9e-3  # Leaf area (m^2)
a = 0.19
b = 67.74
c = 28.78
T_crit = 12
T_opt = 30
dl = 1.37e-2
T_avg = 33

# Helper functions
T_eff = lambda T_avg: T_avg - T_crit
T_sl = lambda T_avg: (T_opt - T_crit) / (T_avg - T_crit)

# Differential equation
def dA_dt(t, A):
    return LA * a * T_eff(T_avg)* np.exp(-((t - b) / c) ** 2) - (dl * T_sl(T_avg)*A) 

# Time range and initial condition
t_span = (0, 50)  # Time range (e.g., 0 to 150 days)
t_eval = np.linspace(t_span[0], t_span[1], 100)  # Time points for evaluation
A0 = LA  # Initial leaf area

# Solve the differential equation
sol = solve_ivp(dA_dt, t_span, [A0], t_eval=t_eval)
