import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Days After Sowing for data points (approximate from Figure 3)
days_after_sowing = np.array([5, 44, 66, 86])

# Leaf dry mass (g) - approximated from Figure 3B 
x_leaf_mass = np.array([1.87e-5, 8.86e-2 , 3.94e-1, 5.17e-1])

# Shoot dry mass (g)
y_shoot_mass = np.array([1.31e-10,3.39e-7,  1.58e-2, 8.57e-2])
y_shoot_mass_log = np.log(y_shoot_mass)

poly_degree = 1
interp_kind = 'quadratic'

poly_coeffs_leaf_shoot = np.polyfit(x_leaf_mass, y_shoot_mass_log, poly_degree)

# Crear una función polinómica a partir de los coeficientes
poly_fit_function_leaf_shoot = np.poly1d(poly_coeffs_leaf_shoot)
# Realizar Interpolación (Hoja vs. Vástago)
interp_function_leaf_shoot = interp1d(x_leaf_mass, y_shoot_mass_log, kind=interp_kind, bounds_error=False, fill_value="extrapolate")

def shoot_mass_from_leaf_mass(leaf_mass, method='interpolation'):
    """Estimate shoot mass from leaf mass using polynomial fit."""
    if method == 'polynomial':
        return np.exp(poly_fit_function_leaf_shoot(leaf_mass))  # Invertir logaritmo
    elif method == 'interpolation':
        return np.exp(interp_function_leaf_shoot(leaf_mass))
    else:
        raise ValueError("Método no reconocido. Usa 'polinómico' o 'interpolación'.")

if __name__ == "__main__":
    print(shoot_mass_from_leaf_mass(0.557))
    plt.figure(figsize=(6, 6))
    plt.scatter(x_leaf_mass, y_shoot_mass, color='blue', label='Puntos de Datos Originales')
    x_interp_leaf_shoot = np.linspace(min(x_leaf_mass), max(x_leaf_mass), 100)
    y_interp_leaf_shoot = np.exp(interp_function_leaf_shoot(x_interp_leaf_shoot))
    plt.plot(x_interp_leaf_shoot, y_interp_leaf_shoot, color='green', linestyle='--', label=f'Interpolación Cuadrática')
    plt.title('Masa Seca de Hoja vs. Masa Seca de Tallo/inflorescencia')
    plt.xlabel('Masa Seca de Hoja (g)')
    plt.ylabel('Masa Seca de Tallo/inflorescencia (g)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()