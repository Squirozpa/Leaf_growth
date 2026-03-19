import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

#Particiones de carbono en la planta
x_time = np.array([26, 44, 66, 86])  # Días después de la siembra
leaf_partition = np.array([0.71, 0.70, 0.49, 0.20])
leaf_area_partition = np.array([0.57, 0.56, 0.42, 0.12])
poly_degree = 2
interp_kind = 'quadratic'

# Realizar Ajuste de Curva (Tiempo vs. Partición de Hoja)
poly_coeffs_leaf_partition = np.polyfit(x_time, leaf_partition, poly_degree)
poly_fit_function_leaf_partition = np.poly1d(poly_coeffs_leaf_partition)
poly_coeffs_leaf_area_partition = np.polyfit(x_time, leaf_area_partition, poly_degree)
poly_fit_function_leaf_area_partition = np.poly1d(poly_coeffs_leaf_area_partition)

print(f"Coeficientes polinómicos (grado {poly_degree}) para Tiempo vs. Partición de Hoja: {poly_coeffs_leaf_partition}")
# Realizar Interpolación (Tiempo vs. Partición de Hoja)
interp_function_leaf_partition = interp1d(x_time, leaf_partition, kind=interp_kind, bounds_error=False, fill_value="extrapolate")
interp_function_leaf_area_partition = interp1d(x_time, leaf_area_partition, kind=interp_kind, bounds_error=False, fill_value="extrapolate")

def leaf_area_partition_over_time(day, method='interpolation'):
    """Estimate leaf area partition over time using polynomial fit or interpolation."""
    if method == 'polynomial':
        return poly_fit_function_leaf_area_partition(day)
    elif method == 'interpolation':
        return interp_function_leaf_area_partition(day)
    else:
        raise ValueError("Método no reconocido. Usa 'polinómico' o 'interpolación'.")
    
def leaf_partition_over_time(day, method='polynomial'):
    """Estimate leaf partition over time using polynomial fit or interpolation."""
    if method == 'polynomial':
        return poly_fit_function_leaf_partition(day)
    elif method == 'interpolation':
        return interp_function_leaf_partition(day)
    else:
        raise ValueError("Método no reconocido. Usa 'polinómico' o 'interpolación'.")
    
if __name__ == "__main__":
    
    plt.figure(figsize=(12, 6))
    
    # Calculate common y-axis limits
    x_interp = np.linspace(min(x_time), max(x_time), 100)
    y_interp_leaf_partition = interp_function_leaf_partition(x_interp)
    y_interp_leaf_area_partition = interp_function_leaf_area_partition(x_interp)
    
    all_y_values = np.concatenate([leaf_partition, leaf_area_partition, 
                                    y_interp_leaf_partition, y_interp_leaf_area_partition])
    y_min = np.min(all_y_values)
    y_max = np.max(all_y_values)
    y_margin = (y_max - y_min) * 0.1
    
    # Plot 1: Leaf Weight Partition
    plt.subplot(1, 2, 1)
    plt.scatter(x_time, leaf_partition, color='blue', label='Puntos de Datos Originales', s=50, zorder=3)
    plt.plot(x_interp, y_interp_leaf_partition, color='green', linestyle='-', linewidth=2, label='Interpolación Cuadrática')
    plt.title('Días después de la siembra vs. Partición de Peso de Hoja')
    plt.xlabel('Días después de la siembra')
    plt.ylabel('Partición de Peso de Hoja')
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Plot 2: Leaf Area Partition
    plt.subplot(1, 2, 2)
    plt.scatter(x_time, leaf_area_partition, color='blue', label='Puntos de Datos Originales', s=50, zorder=3)
    plt.plot(x_interp, y_interp_leaf_area_partition, color='orange', linestyle='-', linewidth=2, label='Interpolación Cuadrática')
    plt.title('Días después de la siembra vs. Partición de Área de Hoja')
    plt.xlabel('Días después de la siembra')
    plt.ylabel('Partición de Área de Hoja')
    plt.ylim(y_min - y_margin, y_max + y_margin)
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()

    # Note: Only interpolation is used because polynomial fit can give values greater than 1