import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from growth import growth_carbon, growth_nitrogen, A_hojas
from params import *
from lma_calculation import calculate_lma
def growth_system(t, y, dt, *args):
    """
    Define the system of ODEs for solve_ivp.
    y[0]: Leaf weight (LW).
    """
    LW = y[0]
    dLW, dA = growth_carbon(t, dt, LW)
    return dLW

def growth_system_nitrogen(t, y, dt, S, *args):
    """
    Define the system of ODEs for solve_ivp with nitrogen consideration.
    y[0]: Leaf weight (LW).
    y[1]: Leaf area (A).
    S: Soil nitrogen content.
    """
    LW = y[0]
    dLW, dA = growth_nitrogen(t, dt, LW, S)
    return dLW


def range_kutta_carbon(t0, tf, dt, LW0):
    """
    Implement the 4th order Runge-Kutta method for the carbon growth system.
    """
    times = np.arange(t0, tf, dt)
    LW_values = [LW0]
    A_values = [A_hojas(calculate_lma(t0), LW0)]

    y = [LW0]

    for t in times[:-1]:
        k1 = np.array(growth_system(t, y, dt))
        k2 = np.array(growth_system(t + dt / 2, y + dt * k1 / 2, dt))
        k3 = np.array(growth_system(t + dt / 2, y + dt * k2 / 2, dt))
        k4 = np.array(growth_system(t + dt, y + dt * k3, dt))

        y = y + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        LW_values.append(y[0])
        A_values.append(A_hojas(calculate_lma(t), y[0]))

    return times, np.array(LW_values), np.array(A_values)

def range_kutta_nitrogen(t0, tf, dt, LW0, S):
    """
    Implement the 4th order Runge-Kutta method for the nitrogen growth system.
    """
    times = np.arange(t0, tf, dt)
    LW_values = [LW0]
    A_values = [A_hojas(calculate_lma(t0), LW0)]

    y = [LW0]

    for t in times[:-1]:
        k1 = np.array(growth_system_nitrogen(t, y, dt, S))
        k2 = np.array(growth_system_nitrogen(t + dt / 2, y + dt * k1 / 2, dt, S))
        k3 = np.array(growth_system_nitrogen(t + dt / 2, y + dt * k2 / 2, dt, S))
        k4 = np.array(growth_system_nitrogen(t + dt, y + dt * k3, dt, S))

        y = y + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        LW_values.append(y[0])
        A_values.append(A_hojas(calculate_lma(t), y[0]))

    return times, np.array(LW_values), np.array(A_values)

if __name__ == "__main__":
    dt = 1/24  # Time step in days
    total_time = 85  # Total simulation time in days

    starting_leaf_area = 0.05
    starting_leaf_weight = starting_leaf_area * calculate_lma(1)
    current_leaf_weight = starting_leaf_weight
    starting = 5  # Current time in days
    test_SAR = 3000
    leaf_weights = [starting_leaf_weight]
    leaf_areas = [A_hojas(calculate_lma(starting), starting_leaf_weight)]

    results_carbon = range_kutta_carbon(starting, total_time, dt, starting_leaf_weight)
    times, leaf_weights, leaf_areas = results_carbon
    # Nitrogen scenario
    results_nitrogen = range_kutta_nitrogen(starting, total_time, dt, starting_leaf_weight, test_SAR)
    times_nitrogen, leaf_weights_nitrogen, leaf_areas_nitrogen = results_nitrogen

    # Load and process measured data


    df = pd.read_csv("Data Sheet 2 model.csv")
    df["Area cm2"] = df["area"] * 10000
    df.columns = df.columns.str.strip()
    measured_daily = df["Area cm2"].groupby(df.index // 24).mean()
    measured_days = range(len(measured_daily))

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(times, leaf_weights, label='Leaf Weight (g) - Carbon Only', color='green')
    plt.plot(times_nitrogen, leaf_weights_nitrogen, label='Leaf Weight (g) - With Nitrogen', color='blue')
    plt.xlabel('Time (days)')
    plt.ylabel('Leaf Weight (g)')
    plt.title('Leaf Weight Over Time')
    plt.grid(True)
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(measured_days, measured_daily, label='Measured Leaf Area', color='black')
    plt.plot(times, leaf_areas, label='Leaf Area (cm²) - Carbon Only', color='orange')
    plt.plot(times_nitrogen, leaf_areas_nitrogen, label='Leaf Area (cm²) - With Nitrogen', color='red')
    plt.xlabel('Time (days)')
    plt.ylabel('Leaf Area (cm²)')
    plt.title('Leaf Area Over Time')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
