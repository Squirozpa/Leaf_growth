import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from effective_area import effective_area_function
from params import *
from rw_calculation import root_mass_from_leaf_mass
from sw_calculation import shoot_mass_from_leaf_mass
from pr_nitrogen import nitrogen_effect_on_photosynthesis
from k_over_time import leaf_partition_over_time, leaf_area_partition_over_time
from leaf_root_ratio_nitrogen import adjusted_L_R
from michaelis_menten_nitrogen import michaelis_menten
from lma_calculation import calculate_lma

C_mant_day = lambda alpha_raiz, RW, alpha_tallo, SW, P: (alpha_raiz * RW + alpha_tallo * SW) * P
C_mant_night = lambda alpha_hoja, LW, alpha_raiz, RW, alpha_tallo, SW, P: (alpha_hoja * LW + alpha_raiz * RW + alpha_tallo * SW) * (1-P)

C_out = lambda alpha_hoja, LW, alpha_raiz, RW, alpha_tallo, SW, P: C_mant_day(alpha_raiz, RW, alpha_tallo, SW, P) + C_mant_night(alpha_hoja, LW, alpha_raiz, RW, alpha_tallo, SW, P)

C_in = lambda PR, A, P: PR * effective_area_function(A) * P

C_disp = lambda PR, A, LW, P, alpha_raiz, RW, alpha_tallo, SW, alpha_hoja,: C_in(PR, A, P) - C_out(alpha_hoja, LW, alpha_raiz, RW, alpha_tallo, SW, P)
C_hojas = lambda k, C_disp: C_disp * k

dLW_dt = lambda C_hojas: C_hojas / (beta_leaf + RHO)

rgr = lambda dA_dt, A_hojas: dA_dt / A_hojas

RW = lambda LW: root_mass_from_leaf_mass(LW)
SW = lambda LW: shoot_mass_from_leaf_mass(LW)

PR_adjusted = lambda N_area, N_max=0.9: nitrogen_effect_on_photosynthesis(N_area, N_max)
k = lambda t: leaf_partition_over_time(t)
k_area = lambda t: leaf_area_partition_over_time(t)
actual_L_R = lambda LW: LW / root_mass_from_leaf_mass(LW)
L_R_adjusted = lambda SAR, leaf_weight: adjusted_L_R(SAR, actual_L_R(leaf_weight / RW(leaf_weight)))

SNAR_adjusted = lambda S, SNAR_max: michaelis_menten(S, SNAR_max, Km)


N_area = lambda A, LW, RW, SW, SAR: ((LW / (LW + RW + SW)) * (SAR*RW))/A

def growth_carbon(t, dt, LW, A):
    RW = root_mass_from_leaf_mass(LW)
    SW = shoot_mass_from_leaf_mass(LW)

    carbon_disp = C_disp(PR, A, LW, P, alpha_root, RW, alpha_stem, SW, alpha_leaf)
    carbon_leaf = C_hojas(k(t), carbon_disp)
    dLW = carbon_leaf / (beta_leaf + RHO) * dt
    carbon_leaf_area = carbon_disp * k_area(t)
    dA = (carbon_leaf_area / ((beta_leaf + RHO) * calculate_lma(t))) * dt
    print(f"Time: {t}, LW: {LW}, A: {A}, RW: {RW}, SW: {SW}, carbon_disp: {carbon_disp}, carbon_leaf: {carbon_leaf}, dLW: {dLW}, dA: {dA}")
    if dA < 0:
        print(f"Warning: dA is negative ({dA}) at time {t}. Check parameters and calculations.")
        print(f"LW: {LW}, RW: {RW}, SW: {SW}, A: {A}, carbon_disp: {carbon_disp}, carbon_leaf_area: {carbon_leaf_area}")
        print(f"C_in: {C_in(PR, A, P)}, C_out: {C_out(alpha_leaf, LW, alpha_root, RW, alpha_stem, SW, P)}")

    if dLW < 0:
        print(f"Warning: dLW is negative ({dLW}) at time {t}. Check parameters and calculations.")
        print(f"LW: {LW}, RW: {RW}, SW: {SW}, A: {A}, carbon_disp: {carbon_disp}, carbon_leaf: {carbon_leaf}")
        print(f"C_in: {C_in(PR, A, P)}, C_out: {C_out(alpha_leaf, LW, alpha_root, RW, alpha_stem, SW, P)}")
        raise ValueError("dLW is negative, which is not physically meaningful.")
    return dLW, dA, SW, RW

def growth_nitrogen(t, dt, LW, A, S):
    SW = shoot_mass_from_leaf_mass(LW)

    SAR = SNAR_adjusted(S, SNAR)
    L_R = L_R_adjusted(SAR, LW)
    adjusted_RW = LW / L_R

    N_area_value = N_area(A, LW, adjusted_RW, SW, SAR)
    adjusted_PR = PR_adjusted(N_area_value)
    carbon_disp = C_disp(adjusted_PR, A, LW, P, alpha_root, adjusted_RW, alpha_stem, SW, alpha_leaf)
    carbon_leaf = C_hojas(k(t), carbon_disp)
    dLW = (carbon_leaf / (beta_leaf + RHO)) * dt
    carbon_leaf_area = carbon_disp * k_area(t)
    dA = (carbon_leaf_area / ((beta_leaf + RHO) * calculate_lma(t))) * dt
    print(f"Time: {t}, LW: {LW}, A: {A}, RW: {adjusted_RW}, SW: {SW}, SAR: {SAR}, N_area: {N_area_value}, adjusted_PR: {adjusted_PR}, carbon_disp: {carbon_disp}, SAR: {S}, dA : {dA}")
    return dLW, dA, SW, adjusted_RW

def growth_system(t, y, *args):
    """
    Define the system of ODEs for solve_ivp.
    y[0]: Leaf weight (LW).
    y[1]: Leaf area (A).
    """
    LW = y[0]
    A = y[1]
    dLW, dA = growth_carbon(t, dt, LW)
    return [dLW, dA]

if __name__ == "__main__":
    dt = 1/24  # Time step in days
    total_time = 89  # Total simulation time in days
    time_steps = int(total_time / dt)
    times = np.linspace(5, total_time, time_steps)
    starting_leaf_area = 0.05
    starting_leaf_weight = starting_leaf_area * calculate_lma(5)  # Initial leaf weight based on LMA at day 5
    current_leaf_weight = starting_leaf_weight
    current_leaf_area = starting_leaf_area
    current_t = 5  # Current time in days
    test_SAR_low = 1500
    test_SAR_med = 2500
    test_SAR_high = 3500
    
    leaf_weights = [starting_leaf_weight]
    leaf_areas = [starting_leaf_area]
    weight_nit_low =[starting_leaf_weight]
    weight_nit_med = [starting_leaf_weight]
    weight_nit_high = [starting_leaf_weight]
    area_nit_low = [starting_leaf_area]
    area_nit_med = [starting_leaf_area]
    area_nit_high = [starting_leaf_area]

    current_leaf_weight_nit_low = starting_leaf_weight
    current_leaf_area_nit_low = starting_leaf_area
    current_leaf_area_nit_med = starting_leaf_area
    current_leaf_weight_nit_med = starting_leaf_weight    
    current_leaf_area_nit_high = starting_leaf_area
    current_leaf_weight_nit_high = starting_leaf_weight

    sws_low = [shoot_mass_from_leaf_mass(starting_leaf_weight)]
    rws_low = [root_mass_from_leaf_mass(starting_leaf_weight)]
    sws_med = [shoot_mass_from_leaf_mass(starting_leaf_weight)]
    rws_med = [root_mass_from_leaf_mass(starting_leaf_weight)]
    sws_high = [shoot_mass_from_leaf_mass(starting_leaf_weight)]
    rws_high = [root_mass_from_leaf_mass(starting_leaf_weight)]
    sws = [shoot_mass_from_leaf_mass(starting_leaf_weight)]
    rws = [root_mass_from_leaf_mass(starting_leaf_weight)]

    for time_step in times:
        dLW, dA, sw, rw = growth_carbon(current_t, dt, current_leaf_weight, current_leaf_area)
        dLW_nit_low, dA_nit_low, sw_low, rw_low = growth_nitrogen(current_t, dt, current_leaf_weight_nit_low, current_leaf_area_nit_low, test_SAR_low)
        dLW_nit_med, dA_nit_med, sw_med, rw_med = growth_nitrogen(current_t, dt, current_leaf_weight_nit_med, current_leaf_area_nit_med, test_SAR_med)
        dLW_nit_high, dA_nit_high, sw_high, rw_high = growth_nitrogen(current_t, dt, current_leaf_weight_nit_high, current_leaf_area_nit_high, test_SAR_high)

        current_leaf_area_nit_low += dA_nit_low
        current_leaf_weight_nit_low += dLW_nit_low
        weight_nit_low.append(current_leaf_weight_nit_low)
        area_nit_low.append(current_leaf_area_nit_low)
        sws_low.append(sw_low)
        rws_low.append(rw_low)

        current_leaf_area_nit_med += dA_nit_med
        current_leaf_weight_nit_med += dLW_nit_med
        weight_nit_med.append(current_leaf_weight_nit_med)
        area_nit_med.append(current_leaf_area_nit_med)
        sws_med.append(sw_med)
        rws_med.append(rw_med)

        current_leaf_area_nit_high += dA_nit_high
        current_leaf_weight_nit_high += dLW_nit_high
        weight_nit_high.append(current_leaf_weight_nit_high)
        area_nit_high.append(current_leaf_area_nit_high)
        sws_high.append(sw_high)
        rws_high.append(rw_high)
        sws.append(sw)
        rws.append(rw)
        current_leaf_weight += dLW
        current_leaf_area += dA
        leaf_weights.append(current_leaf_weight)
        leaf_areas.append(current_leaf_area)
        
        
        current_t += dt

    print(f"Day {current_t:.2f}: Leaf Weight Nitrogen Medium = {current_leaf_weight_nit_med:.4f} g, Leaf Area Nitrogen Medium = {current_leaf_area_nit_med:.4f} cm² L_R = {actual_L_R(current_leaf_weight_nit_med):.4f}, LR = {adjusted_L_R(test_SAR_med, actual_L_R(current_leaf_weight_nit_med)):.4f}")
    print(f"Day {current_t:.2f}: Leaf Weight Nitrogen High = {current_leaf_weight_nit_high:.4f} g, Leaf Area Nitrogen High = {current_leaf_area_nit_high:.4f} cm² L_R = {actual_L_R(current_leaf_weight_nit_high):.4f}, LR = {adjusted_L_R(test_SAR_high, actual_L_R(current_leaf_weight_nit_high)):.4f}")
    print(f"Day {current_t:.2f}: Leaf Weight Nitrogen Low = {current_leaf_weight_nit_low:.4f} g, Leaf Area Nitrogen Low = {current_leaf_area_nit_low:.4f} cm² L_R = {actual_L_R(current_leaf_weight_nit_low):.4f}, LR = {adjusted_L_R(test_SAR_low, actual_L_R(current_leaf_weight_nit_low)):.4f}")
    print(f"Day {current_t:.2f}: Leaf Weight = {current_leaf_weight:.4f} g, Leaf Area = {current_leaf_area:.4f} cm² L_R = {actual_L_R(current_leaf_weight):.4f}")
    df = pd.read_csv("Data Sheet 2 model.csv")
    df["Area cm2"] = df["area"] * 10000
    df.columns = df.columns.str.strip()
    measured_daily = df["Area cm2"].groupby(df.index // 24).mean()
    measured_days = range(len(measured_daily))
    actual_measured_days = [5,26, 44, 66, 86]
    actual_measured_area = [0.05, 1.74e-1, 32.3, 148, 190]
    actual_measured_weight = [2.57e-3, 5.98e-2, 3.41e-1, 5.58e-1]
    plt.figure(figsize=(10, 6))
    plt.plot(measured_days, measured_daily, label='Área foliar modelo de Wruduwage et al., 2014', color='black')
    plt.plot(np.linspace(5, total_time, len(actual_measured_days)), actual_measured_area, 'ro', label='Área foliar medida (Wruduwage et al., 2014)', markersize=8)
    plt.plot(np.linspace(5, total_time, time_steps + 1), leaf_areas, label='Área foliar modelo de carbono', color='orange')
    plt.plot(np.linspace(5, total_time, len(area_nit_low)), area_nit_low, label='Área foliar Modelo de nitrógeno bajo', color='blue', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(area_nit_med)), area_nit_med, label='Área foliar Modelo de nitrógeno medio', color='purple', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(area_nit_high)), area_nit_high, label='Área foliar Modelo de nitrógeno alto', color='green', linestyle='--')
    plt.xlabel('Tiempo (días)')
    plt.ylabel('Área Foliar (cm²)')
    plt.title('Área Foliar a lo Largo del Tiempo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.close()
    plt.figure(figsize=(10, 6))
    plt.title('Relative Growth Rate Over Time')
    x_measured = [44, 66, 80] 
    y_measured = [5.36e-02, 3.30e-2, 7.91e-3]
    plt.scatter(x_measured, y_measured, color='red', label='(Weraduwage, et al., 2014) RGR Leaf Area estimation (cm²/day)', zorder=5)
    plt.plot(np.linspace(5, total_time, time_steps), [rgr((leaf_areas[i+1]-leaf_areas[i])/dt, leaf_areas[i]) for i in range(len(leaf_areas)-1)], label='Carbon Model RGR Leaf Area', color='orange')
    plt.plot(np.linspace(5, total_time, len(measured_daily)-1), [rgr((measured_daily[i+1]-measured_daily[i]), measured_daily[i]) for i in range(len(measured_daily)-1)], label='(Weraduwage, et al., 2014) RGR Leaf Area', color='black')
    plt.plot(np.linspace(5, total_time, len(area_nit_low)-1), [rgr((area_nit_low[i+1]-area_nit_low[i])/dt, area_nit_low[i]) for i in range(len(area_nit_low)-1)], label='RGR Leaf Area Nitrogen Low', color='blue', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(area_nit_med)-1), [rgr((area_nit_med[i+1]-area_nit_med[i])/dt, area_nit_med[i]) for i in range(len(area_nit_med)-1)], label='RGR Leaf Area Nitrogen Medium', color='purple', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(area_nit_high)-1), [rgr((area_nit_high[i+1]-area_nit_high[i])/dt, area_nit_high[i]) for i in range(len(area_nit_high)-1)], label='RGR Leaf Area Nitrogen High', color='green', linestyle='--')
    plt.xlabel('Tiempo (días)')
    plt.ylabel('Tasa de Crecimiento Relativa de Área a lo Largo del Tiempo (cm²/cm² día)')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 0.25)
    plt.tight_layout()
    plt.show()
    plt.close()

    weights_carbon = [leaf_weights[i] + sws[i] + rws[i] for i in range(len(leaf_weights))]
    weights_nit_low = [weight_nit_low[i] + sws_low[i]+ rws_low[i] for i in range(len(weight_nit_low))]
    weights_nit_med = [weight_nit_med[i] + sws_med[i]+ rws_med[i] for i in range(len(weight_nit_med))]
    weights_nit_high = [weight_nit_high[i] + sws_high[i]+ rws_high[i] for i in range(len(weight_nit_high))]
    x_measured_wt = [44, 66, 86] 
    y_measured_wt = [5.24e-2, 3.63e-2, 2.16e-2]

    plt.figure(figsize=(6, 6))
    plt.title("Tasa de Crecimiento Relativa de Peso a lo Largo del Tiempo")

    # Skip the first value in the data by slicing with [1:]
    plt.scatter(x_measured_wt, y_measured_wt, color='red', label='RGR modelo Weraduwage, et al., 2014', zorder=5)
    plt.plot(np.linspace(5, total_time, time_steps)[1:], 
            [rgr((weights_carbon[i+1]-weights_carbon[i])/dt, weights_carbon[i]) for i in range(len(weights_carbon)-1)][1:], 
            label='RGR modelo de carbono', color='orange')
    plt.plot(np.linspace(5, total_time, len(weights_nit_low)-1)[1:], 
            [rgr((weights_nit_low[i+1]-weights_nit_low[i])/dt, weights_nit_low[i]) for i in range(len(weights_nit_low)-1)][1:], 
            label='RGR modelo de nitrógeno bajo', color='blue', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(weights_nit_med)-1)[1:], 
            [rgr((weights_nit_med[i+1]-weights_nit_med[i])/dt, weights_nit_med[i]) for i in range(len(weights_nit_med)-1)][1:], 
            label='RGR modelo de nitrógeno medio', color='purple', linestyle='--')
    plt.plot(np.linspace(5, total_time, len(weights_nit_high)-1)[1:], 
            [rgr((weights_nit_high[i+1]-weights_nit_high[i])/dt, weights_nit_high[i]) for i in range(len(weights_nit_high)-1)][1:], 
            label='RGR modelo de nitrógeno alto', color='green', linestyle='--')

    print(max([rgr((weights_carbon[i+1]-weights_carbon[i])/dt, weights_carbon[i]) for i in range(len(weights_carbon)-1)][1:]))
    print(max([rgr((weights_nit_low[i+1]-weights_nit_low[i])/dt, weights_nit_low[i]) for i in range(len(weights_nit_low)-1)][1:]))
    print(max([rgr((weights_nit_med[i+1]-weights_nit_med[i])/dt, weights_nit_med[i]) for i in range(len(weights_nit_med)-1)][1:]))
    print(max([rgr((weights_nit_high[i+1]-weights_nit_high[i])/dt, weights_nit_high[i]) for i in range(len(weights_nit_high)-1)][1:]))

    plt.xlabel('Tiempo (días)')
    plt.ylabel('Tasa de Crecimiento Relativa de Peso a lo Largo del Tiempo (g/g día)')
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 0.25)
    plt.tight_layout()
    plt.show()
    plt.close()