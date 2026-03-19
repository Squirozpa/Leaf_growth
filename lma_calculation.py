import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

x_das = np.array([ 5, 46, 66, 86])
leaf_area = np.array([3.52e-2, 60.5, 171, 189])
leaf_weight = np.array([1.87e-5, 8.86e-2, 3.74e-1,5.17e-1])
leaf_mass_per_area = leaf_weight / leaf_area  # g/cm²

def root_function(x, L, k, x0):
    """Logistic growth function."""
    return L / (1 + np.exp(-k * (x - x0)))

initial_guesses = [max(leaf_mass_per_area), 0.1, np.median(x_das)]
params, covariance = curve_fit(root_function, x_das, leaf_mass_per_area, p0=initial_guesses)
A_fit, k_fit, x0_fit = params

x_fit = np.linspace(min(x_das), max(x_das), 100)
y_fit = root_function(x_fit, A_fit, k_fit, x0_fit)

poly_degree = 2
interp_kind = 'quadratic'
# Realizar Ajuste de Curva (Días después de la siembra vs. Masa por Área de Hoja)
poly_coeffs_LMA = np.polyfit(x_das, leaf_mass_per_area, poly_degree)
poly_fit_function_LMA = np.poly1d(poly_coeffs_LMA)
print(f"Coeficientes polinómicos (grado {poly_degree}) para Días después de la siembra vs. Masa por Área de Hoja: {poly_coeffs_LMA}")
# Realizar Interpolación (Días después de la siembra vs. Masa por Área
interp_function_LMA = interp1d(x_das, leaf_mass_per_area, kind=interp_kind, bounds_error=False, fill_value="extrapolate")

def calculate_lma(day, method='inverse'):
    """Estimate leaf mass per area (LMA) over time using polynomial fit or interpolation."""
    if method == 'polynomial':
        return poly_fit_function_LMA(day)
    elif method == 'interpolation':
        return interp_function_LMA(day)
    elif method == 'inverse':
        return root_function(day, A_fit, k_fit, x0_fit)
    else:
        raise ValueError("Método no reconocido. Usa 'polinómico' o 'interpolación'.")
    
if __name__ == "__main__":
    
    plt.figure(figsize=(8, 6))
    plt.scatter(x_das, leaf_mass_per_area, color='blue', label='Puntos de Datos Originales')
    print(f"Area de peso 0.532 cm²/g en {0.532/calculate_lma(87)} días después de la siembra")
    x_interp_lma = np.linspace(min(x_das), max(x_das), 100)
    y_interp_lma = calculate_lma(x_interp_lma, method='interpolation')
    plt.plot(x_interp_lma, y_interp_lma, color='green', linestyle='--', label=f'Ajuste por Interpolación')
    plt.title('Días después de la siembra vs. Masa por Área de Hoja ')
    plt.xlabel('Días después de la siembra')
    plt.ylabel('Masa por Área de Hoja (g/cm²)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()