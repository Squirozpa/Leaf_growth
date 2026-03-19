import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Days After Sowing for data points (approximate from Figure 3)
days_after_sowing = np.array([5, 44, 66, 86])

# Leaf dry mass (g) - approximated from Figure 3B
x_leaf_mass = np.array([2.45e-5, 8.86e-2, 3.94e-1, 5.17e-1])

# Root dry mass (g) - approximated from Figure 3E
z_root_mass = np.array([0.000001, 0.005516, 0.038069, 0.061947]) # Approximated from Figure 3E

poly_degree = 2
interp_kind = 'quadratic'

# Realizar Ajuste de Curva (Hoja vs. Raíz)
poly_coeffs_leaf_root = np.polyfit(x_leaf_mass, z_root_mass, poly_degree)
poly_fit_function_leaf_root = np.poly1d(poly_coeffs_leaf_root)
print(f"Coeficientes polinómicos (grado {poly_degree}) para Hoja vs. Raíz: {poly_coeffs_leaf_root}")
# Realizar Interpolación (Hoja vs. Raíz)
interp_function_leaf_root = interp1d(x_leaf_mass, z_root_mass, kind=interp_kind, bounds_error=False, fill_value="extrapolate")

def root_mass_from_leaf_mass(leaf_mass, method='interpolation'):
    """Estimate root mass from leaf mass using polynomial fit."""
    if method == 'polynomial':
        return poly_fit_function_leaf_root(leaf_mass)
    elif method == 'interpolation':
        return interp_function_leaf_root(leaf_mass)
    else:
        raise ValueError("Método no reconocido. Usa 'polinómico' o 'interpolación'.")

if __name__ == "__main__":
    
    plt.figure(figsize=(6, 6))
    plt.scatter(x_leaf_mass, z_root_mass, color='blue', label='Puntos de Datos Originales')
    x_interp_leaf_root = np.linspace(min(x_leaf_mass), max(x_leaf_mass), 100)
    y_interp_leaf_root = interp_function_leaf_root(x_interp_leaf_root)
    plt.plot(x_interp_leaf_root, y_interp_leaf_root, color='green', linestyle='--', label=f'Interpolación cuadrática')
    plt.title('Masa Seca de Hoja vs. Masa Seca de Raíz ')
    plt.xlabel('Masa Seca de Hoja (g)')
    plt.ylabel('Masa Seca de Raíz (g)')

    plt.grid(True)
    plt.legend()

    plt.tight_layout() # Ajustar parámetros de subtrama para un diseño ajustado
    plt.show()

    leaf_mass_test = np.linspace(0, 0.51, 51)
    root_mass_poly = root_mass_from_leaf_mass(leaf_mass_test, method='polynomial')
    root_mass_interp = root_mass_from_leaf_mass(leaf_mass_test, method='interpolation')
    total_nitrogen = root_mass_poly*3360
    leaf_area = leaf_mass_test/0.00267
    nitrogen_per_area = total_nitrogen*0.21/leaf_area
    plt.figure(figsize=(8, 6))
    plt.plot(leaf_mass_test, nitrogen_per_area, label='Polinómico', color='red')
    plt.ylabel('N (g cm$^{-2}$)')
    plt.xlabel('Masa seca de hoja (g)')
    plt.ylim(0, 0.25)
    plt.xlim(0, 0.51)
    plt.grid(True)
    plt.legend()
    plt.show()

    ##Si bien el interpolación técnicamente ajusta mejor los puntos, el ajuste polinómico es más suave y probablemente más útil para modelar.